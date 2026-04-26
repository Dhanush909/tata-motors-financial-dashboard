-- ============================================================
-- TATA MOTORS LTD — Financial Analysis SQL Queries
-- Author: Bonthu Raj Dhanush
-- Database: SQLite | Data Source: Screener.in
-- ============================================================


-- ── QUERY 1: Revenue & Profitability Trend ──────────────────
SELECT
    year,
    revenue,
    operating_profit,
    pat,
    ROUND(opm_pct, 2)                                    AS ebitda_margin_pct,
    ROUND(pat_margin_pct, 2)                             AS pat_margin_pct,
    ROUND(revenue - LAG(revenue) OVER (ORDER BY year), 0) AS revenue_yoy_change,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY year)) * 100.0
        / LAG(revenue) OVER (ORDER BY year), 2
    )                                                    AS revenue_yoy_pct
FROM profit_loss
ORDER BY year;


-- ── QUERY 2: Revenue CAGR (10 Year) ─────────────────────────
WITH base AS (
    SELECT
        MIN(year)    AS start_year,
        MAX(year)    AS end_year,
        FIRST_VALUE(revenue) OVER (ORDER BY year)        AS base_revenue,
        LAST_VALUE(revenue)  OVER (ORDER BY year
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND UNBOUNDED FOLLOWING)                     AS latest_revenue,
        COUNT(*) - 1                                     AS num_years
    FROM profit_loss
)
SELECT
    start_year,
    end_year,
    ROUND(base_revenue, 0)                               AS base_revenue_cr,
    ROUND(latest_revenue, 0)                             AS latest_revenue_cr,
    ROUND(
        (POWER(latest_revenue * 1.0 / base_revenue, 1.0 / num_years) - 1) * 100,
        2
    )                                                    AS revenue_cagr_pct
FROM base
LIMIT 1;


-- ── QUERY 3: Cost Structure Analysis ────────────────────────
SELECT
    year,
    revenue,
    expenses,
    ROUND(expenses * 100.0 / revenue, 2)                 AS total_cost_pct,
    ROUND(depreciation * 100.0 / revenue, 2)             AS depreciation_pct,
    ROUND(interest * 100.0 / revenue, 2)                 AS interest_pct,
    ROUND(operating_profit * 100.0 / revenue, 2)         AS ebitda_margin_pct
FROM profit_loss
ORDER BY year;


-- ── QUERY 4: PAT Turnaround Analysis ────────────────────────
SELECT
    year,
    pat,
    eps,
    CASE
        WHEN pat > 0 THEN 'PROFITABLE'
        ELSE 'LOSS-MAKING'
    END                                                  AS profitability_status,
    ROUND(pat - LAG(pat) OVER (ORDER BY year), 0)        AS pat_yoy_change,
    SUM(pat) OVER (ORDER BY year)                        AS cumulative_pat
FROM profit_loss
ORDER BY year;


-- ── QUERY 5: Operating Leverage Analysis ────────────────────
WITH growth AS (
    SELECT
        year,
        revenue,
        operating_profit,
        ROUND(
            (revenue - LAG(revenue) OVER (ORDER BY year)) * 100.0
            / NULLIF(LAG(revenue) OVER (ORDER BY year), 0), 2
        )                                                AS rev_growth_pct,
        ROUND(
            (operating_profit - LAG(operating_profit) OVER (ORDER BY year)) * 100.0
            / NULLIF(ABS(LAG(operating_profit) OVER (ORDER BY year)), 0), 2
        )                                                AS ebitda_growth_pct
    FROM profit_loss
)
SELECT
    year,
    rev_growth_pct,
    ebitda_growth_pct,
    ROUND(ebitda_growth_pct / NULLIF(rev_growth_pct, 0), 2) AS operating_leverage
FROM growth
WHERE rev_growth_pct IS NOT NULL
ORDER BY year;


-- ── QUERY 6: 3-Year Rolling Average Margins ─────────────────
SELECT
    year,
    ROUND(opm_pct, 2)                                    AS ebitda_margin,
    ROUND(AVG(opm_pct) OVER (
        ORDER BY year
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2)                                                AS rolling_3yr_ebitda_margin,
    ROUND(pat_margin_pct, 2)                             AS pat_margin,
    ROUND(AVG(pat_margin_pct) OVER (
        ORDER BY year
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2)                                                AS rolling_3yr_pat_margin
FROM profit_loss
ORDER BY year;


-- ── QUERY 7: Peak Loss & Recovery Summary ───────────────────
SELECT
    'Peak Loss Year'                                     AS metric,
    year,
    pat                                                  AS value_cr
FROM profit_loss
WHERE pat = (SELECT MIN(pat) FROM profit_loss)

UNION ALL

SELECT
    'Peak Revenue Year',
    year,
    revenue
FROM profit_loss
WHERE revenue = (SELECT MAX(revenue) FROM profit_loss)

UNION ALL

SELECT
    'Best Profit Year',
    year,
    pat
FROM profit_loss
WHERE pat = (SELECT MAX(pat) FROM profit_loss);
