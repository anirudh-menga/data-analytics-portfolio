# ✈️ Flight Ticket Price Prediction — ML Pipeline

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-0.24+-orange)
![XGBoost](https://img.shields.io/badge/XGBoost-1.4+-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 📌 Project Overview
An end-to-end machine learning pipeline to **predict flight ticket prices** based on airline, source, destination, stops, duration, and time features. Compares 5 regression models to identify the best performer.

## 🎯 Objectives
- Engineer meaningful features from raw flight booking data
- Train and compare multiple regression models
- Identify the top price drivers using feature importance
- Evaluate model performance with MAE, RMSE, and R² metrics

## 📊 Model Performance Summary

| Model | MAE | RMSE | R² |
|-------|-----|------|-----|
| Linear Regression | ~2,100 | ~3,200 | 0.61 |
| Ridge Regression | ~2,050 | ~3,150 | 0.62 |
| Random Forest | ~1,100 | ~1,850 | **0.87** |
| Gradient Boosting | ~1,200 | ~1,950 | 0.85 |

> ✅ **Best Model: Random Forest (R² = 0.87)**

## 🔧 Feature Engineering
- Extracted journey day, month, and day-of-week from date
- Parsed departure/arrival hours and created time-of-day buckets
- Converted duration strings (e.g., "2h 30m") to total minutes
- Mapped stops to numeric values (non-stop = 0, 1 stop = 1, etc.)
- Label encoded categorical features (airline, source, destination)

## 🛠️ Tech Stack
- **Python 3.8+**
- **Pandas & NumPy** — data manipulation & feature engineering
- **Scikit-Learn** — model training, evaluation, pipeline
- **Matplotlib & Seaborn** — visualizations

## 📁 Project Structure
```
project2_flight_price/
│
├── flight_price_prediction.py   # Main ML pipeline
├── requirements.txt             # Dependencies
├── README.md                    # This file
├── model_comparison.png         # Model performance chart
├── feature_importance.png       # Top features chart
└── residual_analysis.png        # Residual plots
```

## 🚀 How to Run
```bash
# 1. Clone the repo
git clone https://github.com/anirudhmenga/data-analytics-portfolio.git
cd data-analytics-portfolio/project2_flight_price

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download dataset from Kaggle
# https://www.kaggle.com/datasets/nikhilmittal/flight-fare-prediction-mh
# Save as 'flight_data.csv'

# 4. Run the pipeline
python flight_price_prediction.py
```

## 💡 Key Insights
- **Duration** is the strongest price predictor — longer flights cost more
- **Number of stops** significantly impacts price (direct flights are cheaper)
- **Airline brand** is a major factor — premium airlines price 40-60% higher
- **Departure time** affects price — early morning flights tend to be cheaper
- **Journey month** matters — prices peak during holiday seasons

## 🔗 Dataset Source
[Kaggle — Flight Fare Prediction](https://www.kaggle.com/datasets/nikhilmittal/flight-fare-prediction-mh)

## 👤 Author
**Anirudh Kumar Menga**
- LinkedIn: [linkedin.com/in/anirudh-km-65ab64336](https://linkedin.com/in/anirudh-km-65ab64336)
- Email: anirudhmenga07@gmail.com
