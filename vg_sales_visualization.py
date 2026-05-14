"""
Video Game Sales Analytics — Python Visualization Layer
Author: Anirudh Kumar Menga
Description: Python-based visualization and analysis companion
             to the SQL analysis script.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import sqlite3
import warnings
warnings.filterwarnings('ignore')

sns.set_theme(style="whitegrid")
plt.rcParams.update({'figure.dpi': 150, 'figure.figsize': (12, 6)})
COLORS = ['#1F4E79', '#2E74B5', '#5BA3D9', '#9DC3E6', '#BDD7EE']


# ─── 1. LOAD DATA ─────────────────────────────────────────────────────────────
def load_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.lower()
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df = df[df['year'].between(1980, 2020)]
    print(f"Loaded {len(df):,} records | {df['platform'].nunique()} platforms | {df['genre'].nunique()} genres")
    return df


# ─── 2. LOAD INTO SQLITE FOR SQL QUERIES ─────────────────────────────────────
def load_to_sqlite(df: pd.DataFrame) -> sqlite3.Connection:
    conn = sqlite3.connect(':memory:')
    df.to_sql('vg_sales', conn, if_exists='replace', index=False)
    print("Data loaded into in-memory SQLite database")
    return conn


# ─── 3. EXECUTIVE DASHBOARD ───────────────────────────────────────────────────
def create_dashboard(df: pd.DataFrame, conn: sqlite3.Connection) -> None:
    fig = plt.figure(figsize=(18, 12))
    fig.suptitle('Video Game Sales Analytics Dashboard', fontsize=18, fontweight='bold', y=1.01)

    # ── Plot 1: Annual Sales Trend ──
    ax1 = fig.add_subplot(3, 3, 1)
    yearly = df.groupby('year')['global_sales'].sum().reset_index()
    yearly = yearly[yearly['year'].between(1990, 2016)]
    ax1.fill_between(yearly['year'], yearly['global_sales'], alpha=0.4, color='#2E74B5')
    ax1.plot(yearly['year'], yearly['global_sales'], color='#1F4E79', linewidth=2)
    ax1.set_title('Annual Global Sales (1990-2016)', fontweight='bold')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Sales (Millions)')

    # ── Plot 2: Top 10 Platforms ──
    ax2 = fig.add_subplot(3, 3, 2)
    top_platforms = df.groupby('platform')['global_sales'].sum().nlargest(10)
    ax2.barh(top_platforms.index[::-1], top_platforms.values[::-1], color='#2E74B5')
    ax2.set_title('Top 10 Platforms by Sales', fontweight='bold')
    ax2.set_xlabel('Global Sales (Millions)')

    # ── Plot 3: Genre Distribution ──
    ax3 = fig.add_subplot(3, 3, 3)
    genre_sales = df.groupby('genre')['global_sales'].sum().sort_values(ascending=True)
    ax3.barh(genre_sales.index, genre_sales.values, color='#5BA3D9')
    ax3.set_title('Sales by Genre', fontweight='bold')
    ax3.set_xlabel('Global Sales (Millions)')

    # ── Plot 4: Regional Sales Breakdown ──
    ax4 = fig.add_subplot(3, 3, 4)
    regions = {'North America': df['na_sales'].sum(),
               'Europe': df['eu_sales'].sum(),
               'Japan': df['jp_sales'].sum(),
               'Other': df['other_sales'].sum()}
    ax4.pie(regions.values(), labels=regions.keys(),
            autopct='%1.1f%%', colors=COLORS[:4], startangle=90)
    ax4.set_title('Regional Market Share', fontweight='bold')

    # ── Plot 5: Top 10 Publishers ──
    ax5 = fig.add_subplot(3, 3, 5)
    top_pubs = df.groupby('publisher')['global_sales'].sum().nlargest(10)
    ax5.barh(top_pubs.index[::-1], top_pubs.values[::-1], color='#1F4E79')
    ax5.set_title('Top 10 Publishers', fontweight='bold')
    ax5.set_xlabel('Global Sales (Millions)')

    # ── Plot 6: Genre Preference by Region ──
    ax6 = fig.add_subplot(3, 3, 6)
    top_genres = df.groupby('genre')['global_sales'].sum().nlargest(6).index
    genre_region = df[df['genre'].isin(top_genres)].groupby('genre')[
        ['na_sales', 'eu_sales', 'jp_sales']].sum()
    genre_region.plot(kind='bar', ax=ax6, color=COLORS[:3])
    ax6.set_title('Top Genre Sales by Region', fontweight='bold')
    ax6.set_xlabel('Genre')
    ax6.set_ylabel('Sales (Millions)')
    ax6.legend(['NA', 'EU', 'JP'], loc='upper right')
    ax6.tick_params(axis='x', rotation=30)

    # ── Plot 7: Games Released Per Year ──
    ax7 = fig.add_subplot(3, 3, 7)
    releases = df.groupby('year').size().reset_index(name='count')
    releases = releases[releases['year'].between(1990, 2016)]
    ax7.bar(releases['year'], releases['count'], color='#5BA3D9', alpha=0.8)
    ax7.set_title('Games Released Per Year', fontweight='bold')
    ax7.set_xlabel('Year')
    ax7.set_ylabel('Number of Releases')

    # ── Plot 8: Top 15 Best-Selling Games ──
    ax8 = fig.add_subplot(3, 3, 8)
    top_games = df.nlargest(15, 'global_sales')[['name', 'global_sales']]
    top_games['name'] = top_games['name'].str[:20]
    ax8.barh(top_games['name'][::-1], top_games['global_sales'][::-1], color='#2E74B5')
    ax8.set_title('Top 15 Best-Selling Games', fontweight='bold')
    ax8.set_xlabel('Global Sales (Millions)')

    # ── Plot 9: Sales Distribution ──
    ax9 = fig.add_subplot(3, 3, 9)
    sales_data = df[df['global_sales'] <= 5]['global_sales']
    ax9.hist(sales_data, bins=50, color='#2E74B5', edgecolor='white', alpha=0.8)
    ax9.axvline(sales_data.mean(), color='#1F4E79', linestyle='--',
                linewidth=2, label=f'Mean: {sales_data.mean():.2f}M')
    ax9.set_title('Sales Distribution (≤5M)', fontweight='bold')
    ax9.set_xlabel('Global Sales (Millions)')
    ax9.set_ylabel('Frequency')
    ax9.legend()

    plt.tight_layout()
    plt.savefig('vg_sales_dashboard.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Dashboard saved as 'vg_sales_dashboard.png'")


# ─── 4. SQL QUERY EXAMPLES ────────────────────────────────────────────────────
def run_sql_examples(conn: sqlite3.Connection) -> None:
    print("\n" + "="*60)
    print("SQL QUERY RESULTS")
    print("="*60)

    queries = {
        "Top 5 Platforms": """
            SELECT platform, ROUND(SUM(global_sales),2) AS total_sales_m
            FROM vg_sales GROUP BY platform
            ORDER BY total_sales_m DESC LIMIT 5
        """,
        "Top 5 Genres": """
            SELECT genre, ROUND(SUM(global_sales),2) AS total_sales_m
            FROM vg_sales GROUP BY genre
            ORDER BY total_sales_m DESC LIMIT 5
        """,
        "Top 5 Publishers": """
            SELECT publisher, COUNT(*) AS games,
                   ROUND(SUM(global_sales),2) AS total_sales_m
            FROM vg_sales GROUP BY publisher
            ORDER BY total_sales_m DESC LIMIT 5
        """,
        "Peak Year": """
            SELECT year, ROUND(SUM(global_sales),2) AS total_sales_m
            FROM vg_sales WHERE year BETWEEN 1990 AND 2016
            GROUP BY year ORDER BY total_sales_m DESC LIMIT 1
        """
    }

    for title, query in queries.items():
        print(f"\n📊 {title}:")
        result = pd.read_sql_query(query, conn)
        print(result.to_string(index=False))


# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Download from Kaggle:
    # https://www.kaggle.com/datasets/gregorut/videogamesales
    # Save as 'vgsales.csv'
    try:
        df = load_data("vgsales.csv")
        conn = load_to_sqlite(df)
        run_sql_examples(conn)
        create_dashboard(df, conn)
    except FileNotFoundError:
        print("Dataset not found. Download from:")
        print("https://www.kaggle.com/datasets/gregorut/videogamesales")
        print("Save as 'vgsales.csv' in this directory.")
