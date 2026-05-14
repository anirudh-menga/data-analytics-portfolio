# 🔋 Electric Vehicle Population Analysis — Washington State

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-1.3+-green)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.4+-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 📌 Project Overview
End-to-end data analysis of **150,000+ electric vehicle registrations** in Washington State, exploring BEV vs PHEV adoption trends, geographic distribution, CAFV eligibility patterns, and market growth drivers.

## 🎯 Business Questions Answered
- Which EV manufacturers dominate the Washington State market?
- How has EV adoption grown year-over-year since 2010?
- What percentage of registered EVs qualify for CAFV eligibility?
- Which counties lead in EV adoption — and why?
- How does electric range vary across makes and model years?

## 📊 Key Findings
| Metric | Value |
|--------|-------|
| Total EV Registrations | 150,000+ |
| Top Manufacturer | Tesla (40%+ market share) |
| YoY Growth (2020-2023) | ~35% annually |
| Average Electric Range | 58 miles (all EVs) |
| Top County | King County (Seattle metro) |

## 🛠️ Tech Stack
- **Python 3.8+** — core analysis
- **Pandas & NumPy** — data manipulation
- **Matplotlib & Seaborn** — static visualizations
- **Plotly** — interactive charts

## 📁 Project Structure
```
project1_ev_analysis/
│
├── ev_analysis.py          # Main analysis script
├── requirements.txt        # Dependencies
├── README.md               # This file
└── ev_analysis_dashboard.png  # Output visualization
```

## 🚀 How to Run
```bash
# 1. Clone the repository
git clone https://github.com/anirudhmenga/data-analytics-portfolio.git
cd data-analytics-portfolio/project1_ev_analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download the dataset
# https://data.wa.gov/Transportation/Electric-Vehicle-Population-Data/f6w7-q2d2
# Save as 'Electric_Vehicle_Population_Data.csv'

# 4. Run the analysis
python ev_analysis.py
```

## 📈 Sample Visualizations
The script generates a 6-panel dashboard covering:
- BEV vs PHEV distribution (pie chart)
- Top 10 manufacturers (horizontal bar)
- Registrations by model year (line chart)
- CAFV eligibility breakdown (bar chart)
- Electric range distribution (histogram)
- Top counties by registrations (bar chart)

## 🔗 Dataset Source
[Washington State Open Data Portal](https://data.wa.gov/Transportation/Electric-Vehicle-Population-Data/f6w7-q2d2)

## 👤 Author
**Anirudh Kumar Menga**
- LinkedIn: [linkedin.com/in/anirudh-km-65ab64336](https://linkedin.com/in/anirudh-km-65ab64336)
- Email: anirudhmenga07@gmail.com
