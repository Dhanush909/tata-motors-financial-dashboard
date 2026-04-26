"""
database.py — SQLite setup and query execution
Tata Motors Financial Dashboard Project
Author: Bonthu Raj Dhanush
"""

import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "tata_motors.db")
CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "tata_motors_pl.csv")


def create_database():
    """Load CSV into SQLite database."""
    df = pd.read_csv(CSV_PATH)
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("profit_loss", conn, if_exists="replace", index=False)
    conn.close()
    print(f"Database created at {DB_PATH}")
    print(f"Loaded {len(df)} rows into profit_loss table")
    return df


def run_query(sql: str) -> pd.DataFrame:
    """Run a SQL query and return a DataFrame."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df


def run_all_queries() -> dict:
    """Run all analysis queries and return results dict."""
    results = {}

    # Q1 — Revenue & Profitability Trend
    results["trend"] = run_query("""
        SELECT year, revenue, operating_profit, pat,
               ROUND(opm_pct, 2) AS ebitda_margin_pct,
               ROUND(pat_margin_pct, 2) AS pat_margin_pct,
               ROUND(revenue - LAG(revenue) OVER (ORDER BY year), 0) AS revenue_yoy_change,
               ROUND((revenue - LAG(revenue) OVER (ORDER BY year)) * 100.0
                   / LAG(revenue) OVER (ORDER BY year), 2) AS revenue_yoy_pct
        FROM profit_loss ORDER BY year
    """)

    # Q2 — Revenue CAGR
    results["cagr"] = run_query("""
        SELECT
            MIN(year) AS start_year, MAX(year) AS end_year,
            MIN(revenue) AS base_revenue, MAX(revenue) AS peak_revenue,
            ROUND(
                (POWER(
                    (SELECT revenue FROM profit_loss ORDER BY year DESC LIMIT 1) * 1.0
                    / (SELECT revenue FROM profit_loss ORDER BY year ASC LIMIT 1),
                    1.0 / (COUNT(*) - 1)
                ) - 1) * 100, 2
            ) AS revenue_cagr_pct
        FROM profit_loss
    """)

    # Q3 — Cost Structure
    results["costs"] = run_query("""
        SELECT year, revenue, expenses,
               ROUND(expenses * 100.0 / revenue, 2) AS total_cost_pct,
               ROUND(depreciation * 100.0 / revenue, 2) AS depreciation_pct,
               ROUND(interest * 100.0 / revenue, 2) AS interest_pct,
               ROUND(operating_profit * 100.0 / revenue, 2) AS ebitda_margin_pct
        FROM profit_loss ORDER BY year
    """)

    # Q4 — PAT Turnaround
    results["pat"] = run_query("""
        SELECT year, pat, eps,
               CASE WHEN pat > 0 THEN 'PROFITABLE' ELSE 'LOSS-MAKING' END AS status,
               ROUND(pat - LAG(pat) OVER (ORDER BY year), 0) AS pat_yoy_change,
               SUM(pat) OVER (ORDER BY year) AS cumulative_pat
        FROM profit_loss ORDER BY year
    """)

    # Q5 — Rolling Margins
    results["rolling"] = run_query("""
        SELECT year,
               ROUND(opm_pct, 2) AS ebitda_margin,
               ROUND(AVG(opm_pct) OVER (
                   ORDER BY year ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
               ), 2) AS rolling_3yr_ebitda,
               ROUND(pat_margin_pct, 2) AS pat_margin,
               ROUND(AVG(pat_margin_pct) OVER (
                   ORDER BY year ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
               ), 2) AS rolling_3yr_pat
        FROM profit_loss ORDER BY year
    """)

    # Q6 — Key milestones
    results["milestones"] = run_query("""
        SELECT 'Peak Loss Year' AS metric, year, pat AS value_cr
        FROM profit_loss WHERE pat = (SELECT MIN(pat) FROM profit_loss)
        UNION ALL
        SELECT 'Peak Revenue Year', year, revenue
        FROM profit_loss WHERE revenue = (SELECT MAX(revenue) FROM profit_loss)
        UNION ALL
        SELECT 'Best Profit Year', year, pat
        FROM profit_loss WHERE pat = (SELECT MAX(pat) FROM profit_loss)
    """)

    print("All queries executed successfully.")
    return results


if __name__ == "__main__":
    create_database()
    results = run_all_queries()
    for name, df in results.items():
        print(f"\n--- {name.upper()} ---")
        print(df.to_string(index=False))
