# 🎮 Video Game Sales Analytics — SQL + Python

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![SQL](https://img.shields.io/badge/SQL-PostgreSQL-blue?logo=postgresql)
![Pandas](https://img.shields.io/badge/Pandas-1.3+-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 📌 Project Overview
Comprehensive **SQL + Python analysis** of 16,500+ video game titles across platforms, genres, publishers, and global regions — uncovering market trends, top performers, and regional preferences.

## 🎯 Business Questions Answered
- Which platforms generated the most revenue globally?
- Which genres dominate different regional markets (NA, EU, JP)?
- Who are the top publishers by market share and consistency?
- How has the gaming industry grown over the decades?
- What makes a top-selling game?

## 📊 Key Findings
| Metric | Value |
|--------|-------|
| Total Games Analyzed | 16,598 |
| Total Global Sales | $8.9 Billion |
| North America Market Share | 49.3% |
| Peak Year | 2008 ($678M in sales) |
| #1 Platform | PS2 ($1.26B total) |
| #1 Genre | Action (19.7% market share) |
| #1 Publisher | Nintendo (1,789 titles) |

## 🛠️ Tech Stack
- **SQL (PostgreSQL)** — core data analysis and aggregations
- **Python** — data loading, SQLite integration, visualization
- **Pandas** — data manipulation
- **Matplotlib & Seaborn** — 9-panel dashboard

## 📁 Project Structure
```
project3_videogame_sql/
│
├── video_game_sales_analysis.sql   # Full SQL analysis (9 sections)
├── vg_sales_visualization.py       # Python dashboard + SQLite queries
├── requirements.txt                # Dependencies
├── README.md                       # This file
└── vg_sales_dashboard.png          # 9-panel output dashboard
```

## 🗃️ SQL Analysis Sections
1. **Database Setup** — table creation and data loading
2. **Data Quality Checks** — nulls, ranges, cardinality
3. **Global Sales Overview** — regional breakdown and market share
4. **Platform Analysis** — top platforms by decade
5. **Genre Analysis** — genre preferences by region
6. **Publisher Analysis** — market concentration (HHI-style)
7. **Yearly Trends** — YoY growth and rolling averages
8. **Top Performing Games** — all-time leaderboards
9. **Advanced Analytics** — percentile rankings, window functions

## 🚀 How to Run

**Option A: SQL (PostgreSQL)**
```sql
-- 1. Create database and table (see video_game_sales_analysis.sql)
-- 2. Load data: COPY vg_sales FROM '/path/to/vgsales.csv' DELIMITER ',' CSV HEADER;
-- 3. Run queries section by section
```

**Option B: Python (SQLite in-memory)**
```bash
pip install -r requirements.txt
# Download vgsales.csv from Kaggle (link below)
python vg_sales_visualization.py
```

## 💡 Key Insights
- **Action** is the #1 genre globally but **Role-Playing** dominates Japan
- **Nintendo** has the highest average sales per title ($0.82M vs industry avg $0.54M)
- The industry peaked in **2008-2009** before declining due to mobile gaming
- **North America** represents ~49% of global game sales
- Top 20 games account for ~8% of all global sales revenue

## 🔗 Dataset Source
[Kaggle — Video Game Sales](https://www.kaggle.com/datasets/gregorut/videogamesales)

## 👤 Author
**Anirudh Kumar Menga**
- LinkedIn: [linkedin.com/in/anirudh-km-65ab64336](https://linkedin.com/in/anirudh-km-65ab64336)
- Email: anirudhmenga07@gmail.com
