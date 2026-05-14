"""
Flight Ticket Price Prediction — Machine Learning Pipeline
Author: Anirudh Kumar Menga
Description: End-to-end ML pipeline to predict flight ticket prices using
             feature engineering, multiple regression models, and model evaluation.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
import warnings
warnings.filterwarnings('ignore')

sns.set_theme(style="whitegrid")
plt.rcParams.update({'figure.dpi': 150})


# ─── 1. DATA LOADING ──────────────────────────────────────────────────────────
def load_data(filepath: str) -> pd.DataFrame:
    """Load and inspect flight price dataset."""
    df = pd.read_csv(filepath)
    print(f"Dataset Shape: {df.shape}")
    print(f"\nFirst 5 rows:\n{df.head()}")
    print(f"\nMissing Values:\n{df.isnull().sum()}")
    return df


# ─── 2. FEATURE ENGINEERING ───────────────────────────────────────────────────
def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create meaningful features from raw flight data."""
    df = df.copy()

    # Parse date/time features if present
    if 'Date_of_Journey' in df.columns:
        df['Date_of_Journey'] = pd.to_datetime(df['Date_of_Journey'], dayfirst=True)
        df['journey_day'] = df['Date_of_Journey'].dt.day
        df['journey_month'] = df['Date_of_Journey'].dt.month
        df['journey_dayofweek'] = df['Date_of_Journey'].dt.dayofweek
        df['is_weekend'] = df['journey_dayofweek'].isin([5, 6]).astype(int)
        df.drop('Date_of_Journey', axis=1, inplace=True)

    # Parse departure time
    if 'Dep_Time' in df.columns:
        df['dep_hour'] = pd.to_datetime(df['Dep_Time'], format='%H:%M').dt.hour
        df['dep_minute'] = pd.to_datetime(df['Dep_Time'], format='%H:%M').dt.minute
        # Time of day buckets
        df['dep_time_bucket'] = pd.cut(
            df['dep_hour'],
            bins=[0, 6, 12, 17, 21, 24],
            labels=['Night', 'Morning', 'Afternoon', 'Evening', 'Late Night'],
            right=False
        )
        df.drop('Dep_Time', axis=1, inplace=True)

    # Parse arrival time
    if 'Arrival_Time' in df.columns:
        df['arr_hour'] = pd.to_datetime(
            df['Arrival_Time'].str.split(' ').str[0], format='%H:%M'
        ).dt.hour
        df.drop('Arrival_Time', axis=1, inplace=True)

    # Parse duration
    if 'Duration' in df.columns:
        def parse_duration(d):
            d = str(d)
            hours = int(d.split('h')[0]) if 'h' in d else 0
            minutes = int(d.split('h')[1].replace('m', '').strip()) if 'h' in d and 'm' in d else (
                int(d.replace('m', '').strip()) if 'm' in d else 0
            )
            return hours * 60 + minutes
        df['duration_minutes'] = df['Duration'].apply(parse_duration)
        df['duration_hours'] = df['duration_minutes'] / 60
        df.drop('Duration', axis=1, inplace=True)

    # Stops feature
    if 'Total_Stops' in df.columns:
        stops_map = {'non-stop': 0, '1 stop': 1, '2 stops': 2, '3 stops': 3, '4 stops': 4}
        df['num_stops'] = df['Total_Stops'].str.lower().map(stops_map).fillna(0).astype(int)
        df.drop('Total_Stops', axis=1, inplace=True)

    print(f"\nFeature engineered dataset shape: {df.shape}")
    print(f"New features: {df.columns.tolist()}")
    return df


# ─── 3. ENCODE CATEGORICAL FEATURES ──────────────────────────────────────────
def encode_features(df: pd.DataFrame, target_col: str = 'Price') -> tuple:
    """Encode categorical features and prepare X, y."""
    df = df.copy()

    # Drop route and additional_info if present (high cardinality)
    for col in ['Route', 'Additional_Info']:
        if col in df.columns:
            df.drop(col, axis=1, inplace=True)

    # Label encode remaining categoricals
    le = LabelEncoder()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    if target_col in cat_cols:
        cat_cols.remove(target_col)

    for col in cat_cols:
        df[col] = le.fit_transform(df[col].astype(str))

    # Split features and target
    if target_col in df.columns:
        X = df.drop(target_col, axis=1)
        y = df[target_col]
    else:
        raise ValueError(f"Target column '{target_col}' not found in dataframe.")

    print(f"\nFeatures shape: {X.shape}")
    print(f"Target shape:   {y.shape}")
    return X, y


# ─── 4. MODEL TRAINING & EVALUATION ──────────────────────────────────────────
def train_evaluate_models(X_train, X_test, y_train, y_test) -> pd.DataFrame:
    """Train multiple models and compare performance."""

    models = {
        'Linear Regression': LinearRegression(),
        'Ridge Regression': Ridge(alpha=1.0),
        'Lasso Regression': Lasso(alpha=1.0),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
    }

    results = []
    trained_models = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mae  = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2   = r2_score(y_test, y_pred)

        results.append({'Model': name, 'MAE': mae, 'RMSE': rmse, 'R2': r2})
        trained_models[name] = (model, y_pred)
        print(f"{name:<25} | MAE: {mae:,.0f} | RMSE: {rmse:,.0f} | R²: {r2:.4f}")

    return pd.DataFrame(results), trained_models


# ─── 5. FEATURE IMPORTANCE ────────────────────────────────────────────────────
def plot_feature_importance(model, feature_names: list) -> None:
    """Plot feature importances from Random Forest."""
    importances = model.feature_importances_
    fi_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
    fi_df = fi_df.sort_values('Importance', ascending=True).tail(15)

    plt.figure(figsize=(10, 6))
    plt.barh(fi_df['Feature'], fi_df['Importance'], color='#2E74B5')
    plt.title('Top 15 Feature Importances — Random Forest', fontsize=14, fontweight='bold')
    plt.xlabel('Importance Score')
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=150, bbox_inches='tight')
    plt.show()


# ─── 6. MODEL COMPARISON PLOT ─────────────────────────────────────────────────
def plot_model_comparison(results_df: pd.DataFrame) -> None:
    """Visualize model performance comparison."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Model Performance Comparison', fontsize=14, fontweight='bold')

    for i, metric in enumerate(['MAE', 'RMSE', 'R2']):
        sorted_df = results_df.sort_values(metric, ascending=(metric != 'R2'))
        color = ['#1F4E79' if x == sorted_df.iloc[0]['Model'] else '#5BA3D9'
                 for x in sorted_df['Model']]
        axes[i].barh(sorted_df['Model'], sorted_df[metric], color=color)
        axes[i].set_title(f'{metric} Score')
        axes[i].set_xlabel(metric)

    plt.tight_layout()
    plt.savefig('model_comparison.png', dpi=150, bbox_inches='tight')
    plt.show()


# ─── 7. RESIDUAL ANALYSIS ─────────────────────────────────────────────────────
def plot_residuals(y_test, y_pred, model_name: str) -> None:
    """Plot actual vs predicted and residuals."""
    residuals = y_test - y_pred

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f'Residual Analysis — {model_name}', fontsize=13, fontweight='bold')

    # Actual vs Predicted
    axes[0].scatter(y_test, y_pred, alpha=0.4, color='#2E74B5', s=20)
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    axes[0].plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2)
    axes[0].set_xlabel('Actual Price (INR)')
    axes[0].set_ylabel('Predicted Price (INR)')
    axes[0].set_title('Actual vs Predicted')

    # Residuals distribution
    axes[1].hist(residuals, bins=50, color='#2E74B5', edgecolor='white', alpha=0.8)
    axes[1].axvline(0, color='red', linestyle='--', linewidth=2)
    axes[1].set_xlabel('Residuals')
    axes[1].set_ylabel('Frequency')
    axes[1].set_title('Residuals Distribution')

    plt.tight_layout()
    plt.savefig('residual_analysis.png', dpi=150, bbox_inches='tight')
    plt.show()


# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("FLIGHT PRICE PREDICTION — ML PIPELINE")
    print("=" * 60)

    # Download dataset from Kaggle:
    # https://www.kaggle.com/datasets/nikhilmittal/flight-fare-prediction-mh
    # Save as 'flight_data.csv'

    try:
        df = load_data("flight_data.csv")
        df = engineer_features(df)
        X, y = encode_features(df, target_col='Price')

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        print(f"\nTrain size: {X_train.shape[0]:,} | Test size: {X_test.shape[0]:,}")

        # Train & evaluate
        print("\n" + "─" * 60)
        print("MODEL PERFORMANCE SUMMARY")
        print("─" * 60)
        results_df, trained_models = train_evaluate_models(X_train, X_test, y_train, y_test)

        # Best model analysis
        best_model_name = results_df.sort_values('R2', ascending=False).iloc[0]['Model']
        best_model, best_preds = trained_models[best_model_name]
        print(f"\n✅ Best Model: {best_model_name}")

        # Plots
        plot_model_comparison(results_df)

        if hasattr(best_model, 'feature_importances_'):
            plot_feature_importance(best_model, X.columns.tolist())

        plot_residuals(y_test, best_preds, best_model_name)

        print("\n✅ All plots saved successfully!")

    except FileNotFoundError:
        print("Dataset not found. Download from:")
        print("https://www.kaggle.com/datasets/nikhilmittal/flight-fare-prediction-mh")
        print("Save as 'flight_data.csv' in this directory.")
