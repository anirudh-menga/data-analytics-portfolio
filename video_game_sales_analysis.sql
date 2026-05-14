-- ============================================================
-- Video Game Sales Analytics — SQL Analysis
-- Author: Anirudh Kumar Menga
-- Description: Comprehensive SQL analysis of global video game
--              sales across platforms, genres, and regions.
-- Dataset: vgsales.csv from Kaggle
-- ============================================================

-- ─── SECTION 1: DATABASE SETUP ───────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS vg_sales (
    rank          INTEGER,
    name          VARCHAR(200),
    platform      VARCHAR(50),
    year          INTEGER,
    genre         VARCHAR(50),
    publisher     VARCHAR(100),
    na_sales      DECIMAL(10,2),   -- North America sales (millions)
    eu_sales      DECIMAL(10,2),   -- Europe sales (millions)
    jp_sales      DECIMAL(10,2),   -- Japan sales (millions)
    other_sales   DECIMAL(10,2),   -- Other regions (millions)
    global_sales  DECIMAL(10,2)    -- Global total (millions)
);

-- Load data (PostgreSQL syntax)
-- COPY vg_sales FROM '/path/to/vgsales.csv' DELIMITER ',' CSV HEADER;


-- ─── SECTION 2: DATA QUALITY CHECKS ─────────────────────────────────────────

-- Check total records
SELECT COUNT(*) AS total_records FROM vg_sales;

-- Check for nulls in key columns
SELECT
    COUNT(*) FILTER (WHERE name IS NULL)         AS null_names,
    COUNT(*) FILTER (WHERE platform IS NULL)     AS null_platforms,
    COUNT(*) FILTER (WHERE year IS NULL)         AS null_years,
    COUNT(*) FILTER (WHERE global_sales IS NULL) AS null_sales
FROM vg_sales;

-- Check year range
SELECT
    MIN(year) AS earliest_year,
    MAX(year) AS latest_year,
    COUNT(DISTINCT year) AS unique_years
FROM vg_sales
WHERE year IS NOT NULL;

-- Check distinct platforms and genres
SELECT COUNT(DISTINCT platform) AS platforms,
       COUNT(DISTINCT genre)    AS genres,
       COUNT(DISTINCT publisher) AS publishers
FROM vg_sales;


-- ─── SECTION 3: GLOBAL SALES OVERVIEW ────────────────────────────────────────

-- Total global sales by region
SELECT
    ROUND(SUM(na_sales), 2)     AS total_na_sales_m,
    ROUND(SUM(eu_sales), 2)     AS total_eu_sales_m,
    ROUND(SUM(jp_sales), 2)     AS total_jp_sales_m,
    ROUND(SUM(other_sales), 2)  AS total_other_sales_m,
    ROUND(SUM(global_sales), 2) AS total_global_sales_m
FROM vg_sales;

-- Regional market share
SELECT
    ROUND(SUM(na_sales)    / SUM(global_sales) * 100, 1) AS na_pct,
    ROUND(SUM(eu_sales)    / SUM(global_sales) * 100, 1) AS eu_pct,
    ROUND(SUM(jp_sales)    / SUM(global_sales) * 100, 1) AS jp_pct,
    ROUND(SUM(other_sales) / SUM(global_sales) * 100, 1) AS other_pct
FROM vg_sales;


-- ─── SECTION 4: PLATFORM ANALYSIS ────────────────────────────────────────────

-- Top 10 platforms by global sales
SELECT
    platform,
    COUNT(*)                        AS num_games,
    ROUND(SUM(global_sales), 2)     AS total_sales_m,
    ROUND(AVG(global_sales), 3)     AS avg_sales_per_game,
    ROUND(MAX(global_sales), 2)     AS best_selling_game_sales
FROM vg_sales
GROUP BY platform
ORDER BY total_sales_m DESC
LIMIT 10;

-- Platform performance by decade
SELECT
    platform,
    CASE
        WHEN year BETWEEN 1980 AND 1989 THEN '1980s'
        WHEN year BETWEEN 1990 AND 1999 THEN '1990s'
        WHEN year BETWEEN 2000 AND 2009 THEN '2000s'
        WHEN year BETWEEN 2010 AND 2020 THEN '2010s'
        ELSE 'Unknown'
    END AS decade,
    ROUND(SUM(global_sales), 2) AS total_sales_m,
    COUNT(*) AS num_games
FROM vg_sales
WHERE year IS NOT NULL
GROUP BY platform, decade
ORDER BY decade, total_sales_m DESC;


-- ─── SECTION 5: GENRE ANALYSIS ───────────────────────────────────────────────

-- Genre performance globally and by region
SELECT
    genre,
    COUNT(*)                                          AS num_games,
    ROUND(SUM(global_sales), 2)                       AS global_sales_m,
    ROUND(SUM(na_sales), 2)                           AS na_sales_m,
    ROUND(SUM(eu_sales), 2)                           AS eu_sales_m,
    ROUND(SUM(jp_sales), 2)                           AS jp_sales_m,
    ROUND(SUM(global_sales) / SUM(SUM(global_sales))
          OVER() * 100, 2)                            AS market_share_pct
FROM vg_sales
GROUP BY genre
ORDER BY global_sales_m DESC;

-- Genre preferences by region (which genre dominates each market)
WITH genre_region AS (
    SELECT
        genre,
        ROUND(SUM(na_sales), 2) AS na_sales,
        ROUND(SUM(eu_sales), 2) AS eu_sales,
        ROUND(SUM(jp_sales), 2) AS jp_sales
    FROM vg_sales
    GROUP BY genre
)
SELECT
    genre,
    na_sales,
    eu_sales,
    jp_sales,
    CASE
        WHEN na_sales >= eu_sales AND na_sales >= jp_sales THEN 'NA-Dominant'
        WHEN eu_sales >= na_sales AND eu_sales >= jp_sales THEN 'EU-Dominant'
        ELSE 'JP-Dominant'
    END AS dominant_region
FROM genre_region
ORDER BY (na_sales + eu_sales + jp_sales) DESC;


-- ─── SECTION 6: PUBLISHER ANALYSIS ───────────────────────────────────────────

-- Top 15 publishers by global sales
SELECT
    publisher,
    COUNT(*)                        AS num_games,
    ROUND(SUM(global_sales), 2)     AS total_sales_m,
    ROUND(AVG(global_sales), 3)     AS avg_sales_per_title,
    COUNT(DISTINCT platform)        AS platforms_covered,
    COUNT(DISTINCT genre)           AS genres_covered
FROM vg_sales
WHERE publisher IS NOT NULL
GROUP BY publisher
ORDER BY total_sales_m DESC
LIMIT 15;

-- Publisher market concentration (HHI-style)
WITH publisher_sales AS (
    SELECT
        publisher,
        SUM(global_sales) AS sales,
        SUM(global_sales) / SUM(SUM(global_sales)) OVER() AS market_share
    FROM vg_sales
    GROUP BY publisher
)
SELECT
    publisher,
    ROUND(sales, 2) AS total_sales_m,
    ROUND(market_share * 100, 2) AS market_share_pct,
    ROUND(SUM(market_share * 100) OVER (ORDER BY market_share DESC
          ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS cumulative_share_pct
FROM publisher_sales
ORDER BY market_share DESC
LIMIT 20;


-- ─── SECTION 7: YEARLY TRENDS ────────────────────────────────────────────────

-- Annual global sales trend
SELECT
    year,
    COUNT(*)                        AS num_releases,
    ROUND(SUM(global_sales), 2)     AS total_sales_m,
    ROUND(AVG(global_sales), 3)     AS avg_sales_per_game,
    ROUND(SUM(global_sales) - LAG(SUM(global_sales))
          OVER (ORDER BY year), 2)  AS yoy_change_m
FROM vg_sales
WHERE year BETWEEN 1990 AND 2016
GROUP BY year
ORDER BY year;

-- Rolling 3-year average sales
SELECT
    year,
    ROUND(SUM(global_sales), 2) AS annual_sales,
    ROUND(AVG(SUM(global_sales))
          OVER (ORDER BY year ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS rolling_3yr_avg
FROM vg_sales
WHERE year BETWEEN 1990 AND 2016
GROUP BY year
ORDER BY year;


-- ─── SECTION 8: TOP PERFORMING GAMES ─────────────────────────────────────────

-- All-time top 20 games globally
SELECT
    rank,
    name,
    platform,
    year,
    genre,
    publisher,
    global_sales AS global_sales_m
FROM vg_sales
ORDER BY global_sales DESC
LIMIT 20;

-- Top game per genre
SELECT DISTINCT ON (genre)
    genre,
    name,
    platform,
    year,
    publisher,
    ROUND(global_sales, 2) AS global_sales_m
FROM vg_sales
ORDER BY genre, global_sales DESC;

-- Top game per platform
SELECT DISTINCT ON (platform)
    platform,
    name,
    year,
    genre,
    publisher,
    ROUND(global_sales, 2) AS global_sales_m
FROM vg_sales
ORDER BY platform, global_sales DESC;


-- ─── SECTION 9: ADVANCED ANALYTICS ───────────────────────────────────────────

-- Sales performance percentiles
SELECT
    name,
    platform,
    global_sales,
    NTILE(4)  OVER (ORDER BY global_sales) AS sales_quartile,
    PERCENT_RANK() OVER (ORDER BY global_sales) AS percentile_rank,
    CASE
        WHEN NTILE(4) OVER (ORDER BY global_sales) = 4 THEN 'Top Performer'
        WHEN NTILE(4) OVER (ORDER BY global_sales) = 3 THEN 'Above Average'
        WHEN NTILE(4) OVER (ORDER BY global_sales) = 2 THEN 'Below Average'
        ELSE 'Low Performer'
    END AS performance_tier
FROM vg_sales
ORDER BY global_sales DESC
LIMIT 50;

-- Identify publishers with consistent multi-platform success
SELECT
    publisher,
    COUNT(DISTINCT platform) AS platforms,
    COUNT(DISTINCT genre)    AS genres,
    COUNT(*)                 AS total_titles,
    ROUND(SUM(global_sales), 2) AS total_sales_m,
    ROUND(AVG(global_sales), 3) AS avg_sales
FROM vg_sales
GROUP BY publisher
HAVING COUNT(DISTINCT platform) >= 5
   AND COUNT(*) >= 20
ORDER BY total_sales_m DESC
LIMIT 10;
