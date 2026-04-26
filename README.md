# Tata Motors — Financial Performance Dashboard

**Author:** Bonthu Raj Dhanush  
**LinkedIn:** [linkedin.com/in/raj-dhanush-6a1010322](https://www.linkedin.com/in/raj-dhanush-6a1010322)  
**Tools:** Python · SQL (SQLite) · Excel · Power BI  
**Data Source:** Screener.in — Tata Motors Annual Reports (FY2016–FY2025)

---

## Project Overview

An end-to-end financial analytics pipeline built to replicate corporate FP&A reporting on Tata Motors Ltd (NSE: TATAMOTORS) — one of India's largest automotive conglomerates.

The project covers:
- 10 years of P&L analysis (FY2016–FY2025)
- Revenue & profitability trend analysis
- Cost driver decomposition
- PAT turnaround analysis (from -₹34,153 Cr in FY2022 to +₹27,391 Cr in FY2025)
- EPS recovery tracking
- SQL-based analytical queries with CTEs and window functions
- Management scorecard with KPI summary

---

## Project Structure

```
tata_dashboard/
│
├── data/
│   └── tata_motors_pl.csv          # Clean P&L dataset (FY2016–FY2025)
│
├── sql/
│   └── analysis_queries.sql        # All analytical SQL queries
│
├── outputs/
│   └── tata_motors_dashboard.xlsx  # Full Excel dashboard
│
├── charts/
│   └── *.png                       # Exported chart images
│
├── main.py                         # Main pipeline script
├── database.py                     # SQLite database setup & queries
├── visualise.py                    # Chart generation
└── README.md
```

---

## Key Findings

| Metric | FY2016 | FY2022 (Low) | FY2025 (Latest) |
|---|---|---|---|
| Revenue (₹ Cr) | 2,69,194 | 2,78,454 | 4,86,483 |
| EBITDA Margin % | 3.3% | 0.5% | 9.4% |
| PAT (₹ Cr) | -1,181 | -34,153 | +27,391 |
| EPS (₹) | -3.53 | -99.45 | +71.64 |
| Debt (₹ Cr) | High | Peak | Declining |

**Key Insight:** Tata Motors executed one of India's largest corporate turnarounds — from a ₹34,153 Cr net loss in FY2022 to a ₹27,391 Cr profit in FY2025, driven by JLR recovery, EV launches, and cost restructuring.

---

## How to Run

```bash
# Install dependencies
pip install pandas matplotlib seaborn openpyxl sqlite3

# Run full pipeline
python main.py
```

Outputs will be saved to `/outputs` and `/charts` folders.

---

## SQL Queries Included

1. Revenue CAGR calculation using window functions
2. Year-on-year profitability trend
3. Cost structure analysis (expenses as % of revenue)
4. PAT turnaround analysis
5. EPS recovery tracking
6. Operating leverage analysis

---

## Skills Demonstrated

- Financial data analysis and modelling
- SQL — CTEs, window functions, aggregations
- Python — Pandas, Matplotlib, Seaborn
- Excel — multi-sheet dashboard with KPI cards and charts
- FP&A reporting — management scorecard format
- Corporate financial storytelling
