"""
Electric Vehicle Population Analysis - Washington State
Author: Anirudh Kumar Menga
Description: End-to-end data analysis and visualization of BEV/PHEV
             registration trends, geographic distribution, and CAFV eligibility.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# ─── CONFIGURATION ────────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="Blues_d")
plt.rcParams.update({'figure.dpi': 150, 'figure.figsize': (12, 6)})

# ─── 1. LOAD & INSPECT DATA ───────────────────────────────────────────────────
def load_data(filepath: str) -> pd.DataFrame:
    """Load EV population dataset and perform initial inspection."""
    df = pd.read_csv(filepath)
    print(f"Dataset Shape: {df.shape}")
    print(f"\nColumn Names:\n{df.columns.tolist()}")
    print(f"\nMissing Values:\n{df.isnull().sum()}")
    print(f"\nData Types:\n{df.dtypes}")
    return df


# ─── 2. DATA CLEANING & PREPROCESSING ────────────────────────────────────────
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the EV dataset."""
    df = df.copy()

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # Drop rows with critical missing values
    critical_cols = ['make', 'model', 'model_year', 'electric_vehicle_type']
    df.dropna(subset=critical_cols, inplace=True)

    # Convert model year to integer
    df['model_year'] = pd.to_numeric(df['model_year'], errors='coerce')
    df.dropna(subset=['model_year'], inplace=True)
    df['model_year'] = df['model_year'].astype(int)

    # Clean electric range
    if 'electric_range' in df.columns:
        df['electric_range'] = pd.to_numeric(df['electric_range'], errors='coerce').fillna(0)

    # Standardize EV type labels
    df['ev_type_short'] = df['electric_vehicle_type'].apply(
        lambda x: 'BEV' if 'Battery' in str(x) else 'PHEV'
    )

    print(f"\nCleaned Dataset Shape: {df.shape}")
    return df


# ─── 3. EXPLORATORY DATA ANALYSIS ────────────────────────────────────────────
def run_eda(df: pd.DataFrame) -> None:
    """Run comprehensive EDA with visualizations."""

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('Washington State EV Population Analysis', fontsize=16, fontweight='bold', y=1.02)

    # Plot 1: EV Type Distribution
    ev_counts = df['ev_type_short'].value_counts()
    axes[0, 0].pie(ev_counts, labels=ev_counts.index, autopct='%1.1f%%',
                   colors=['#1F4E79', '#2E74B5'], startangle=90)
    axes[0, 0].set_title('BEV vs PHEV Distribution')

    # Plot 2: Top 10 Makes
    top_makes = df['make'].value_counts().head(10)
    axes[0, 1].barh(top_makes.index[::-1], top_makes.values[::-1], color='#2E74B5')
    axes[0, 1].set_title('Top 10 EV Manufacturers')
    axes[0, 1].set_xlabel('Number of Registrations')

    # Plot 3: Registrations by Model Year
    yearly = df.groupby('model_year').size().reset_index(name='count')
    yearly = yearly[yearly['model_year'] >= 2010]
    axes[0, 2].plot(yearly['model_year'], yearly['count'], marker='o',
                    color='#1F4E79', linewidth=2)
    axes[0, 2].fill_between(yearly['model_year'], yearly['count'], alpha=0.3, color='#2E74B5')
    axes[0, 2].set_title('EV Registrations by Model Year')
    axes[0, 2].set_xlabel('Model Year')
    axes[0, 2].set_ylabel('Registrations')

    # Plot 4: CAFV Eligibility
    if 'clean_alternative_fuel_vehicle_(cafv)_eligibility' in df.columns:
        cafv_col = 'clean_alternative_fuel_vehicle_(cafv)_eligibility'
    elif 'cafv_eligibility' in df.columns:
        cafv_col = 'cafv_eligibility'
    else:
        cafv_col = df.columns[df.columns.str.contains('cafv', case=False)][0] if any(df.columns.str.contains('cafv', case=False)) else None

    if cafv_col:
        cafv = df[cafv_col].value_counts()
        axes[1, 0].bar(range(len(cafv)), cafv.values, color=['#1F4E79', '#2E74B5', '#5BA3D9'])
        axes[1, 0].set_xticks(range(len(cafv)))
        axes[1, 0].set_xticklabels([x[:20] for x in cafv.index], rotation=15, ha='right', fontsize=8)
        axes[1, 0].set_title('CAFV Eligibility Distribution')
        axes[1, 0].set_ylabel('Count')

    # Plot 5: Electric Range Distribution
    if 'electric_range' in df.columns:
        range_data = df[df['electric_range'] > 0]['electric_range']
        axes[1, 1].hist(range_data, bins=40, color='#2E74B5', edgecolor='white', alpha=0.8)
        axes[1, 1].axvline(range_data.mean(), color='#1F4E79', linestyle='--',
                           linewidth=2, label=f'Mean: {range_data.mean():.0f} mi')
        axes[1, 1].set_title('Electric Range Distribution')
        axes[1, 1].set_xlabel('Electric Range (miles)')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].legend()

    # Plot 6: Top Counties
    if 'county' in df.columns:
        top_counties = df['county'].value_counts().head(8)
        axes[1, 2].bar(top_counties.index, top_counties.values, color='#2E74B5')
        axes[1, 2].set_title('Top 8 Counties by EV Registrations')
        axes[1, 2].set_xlabel('County')
        axes[1, 2].set_ylabel('Registrations')
        axes[1, 2].tick_params(axis='x', rotation=30)

    plt.tight_layout()
    plt.savefig('ev_analysis_dashboard.png', bbox_inches='tight', dpi=150)
    plt.show()
    print("\nDashboard saved as 'ev_analysis_dashboard.png'")


# ─── 4. KEY METRICS SUMMARY ───────────────────────────────────────────────────
def print_summary(df: pd.DataFrame) -> None:
    """Print key business insights."""
    print("\n" + "="*60)
    print("KEY INSIGHTS — Washington State EV Analysis")
    print("="*60)
    print(f"Total EV Registrations:     {len(df):,}")
    print(f"Unique Makes:               {df['make'].nunique()}")
    print(f"Unique Models:              {df['model'].nunique()}")
    print(f"Most Popular Make:          {df['make'].value_counts().index[0]}")
    print(f"Most Popular Model Year:    {df['model_year'].mode()[0]}")

    bev_pct = (df['ev_type_short'] == 'BEV').mean() * 100
    print(f"BEV Share:                  {bev_pct:.1f}%")
    print(f"PHEV Share:                 {100 - bev_pct:.1f}%")

    if 'electric_range' in df.columns:
        avg_range = df[df['electric_range'] > 0]['electric_range'].mean()
        print(f"Avg Electric Range:         {avg_range:.0f} miles")

    if 'county' in df.columns:
        top_county = df['county'].value_counts().index[0]
        print(f"Top County:                 {top_county}")
    print("="*60)


# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Download dataset from:
    # https://data.wa.gov/Transportation/Electric-Vehicle-Population-Data/f6w7-q2d2
    # Save as 'Electric_Vehicle_Population_Data.csv' in the same directory

    print("Loading EV Population Data...")
    try:
        df = load_data("Electric_Vehicle_Population_Data.csv")
        df = clean_data(df)
        print_summary(df)
        run_eda(df)
    except FileNotFoundError:
        print("Dataset not found. Please download from:")
        print("https://data.wa.gov/Transportation/Electric-Vehicle-Population-Data/f6w7-q2d2")
        print("Save as 'Electric_Vehicle_Population_Data.csv' in this directory.")
