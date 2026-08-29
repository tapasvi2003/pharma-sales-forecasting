# Pharma Sales Time Series Forecasting

End-to-end data engineering and forecasting pipeline for pharmaceutical sales, built to help pharmacies balance stockout risk against excess inventory cost.

---

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Scikit-Learn](https://img.shields.io/badge/Library-Scikit--Learn-orange)
![License](https://img.shields.io/badge/License-MIT-purple)

## Project Overview

Pharmacies need reliable demand forecasts to avoid two costly mistakes: running out of high-demand drugs like Paracetamol, or over-stocking seasonal drugs like respiratory medications that only sell during flu season. This project builds a complete pipeline — from raw transactional data to a trained forecasting model — that predicts monthly drug sales across 8 drug categories.

---

## Dataset

- **Source:** [Kaggle Pharma Sales Dataset](https://www.kaggle.com/datasets/milanzdravkovic/pharma-sales-data)
- **Granularities:** Hourly, Daily, Weekly, Monthly
- **Time range:** 2014 – 2019 (~6 years)
- **Drug categories:** M01AB, M01AE, N02BA, N02BE, N05B, N05C, R03, R06

> Raw and processed CSVs are excluded from this repository (see `.gitignore`). Download the dataset from Kaggle and place it in `data/raw/` to reproduce this project.

---

## Project Architecture

Raw CSV Data (4 granularities)
│
▼
[ src/ingestion/ingest.py ] ──▶ Extract raw files
│
▼
[ src/cleaning/clean.py ] ──▶ Transform: datetime conversion, feature
│ extraction, validation
▼
data/processed/ (clean CSVs) ──▶ Load
│
▼
[ notebooks/05_feature_engineering ] ──▶ Lag, rolling, cyclical features
│
▼
[ notebooks/06_modeling ] ──▶ Naive → ARIMA → SARIMA → Random Forest
│
▼
Model Comparison & Evaluation (MAE, RMSE, MAPE)


---

## Tech Stack

- **Core:** Python 3.12, Pandas, NumPy
- **Time Series & Stats:** Statsmodels (ADF test, seasonal_decompose, ARIMA, SARIMAX, ACF/PACF)
- **Machine Learning:** Scikit-learn (RandomForestRegressor, evaluation metrics)
- **Visualization:** Matplotlib, Seaborn
- **Environment:** venv, Jupyter Notebook

---

## Project Structure

pharma-sales-forecasting/
├── data/
│ ├── raw/ # Original Kaggle CSVs (gitignored)
│ └── processed/ # Cleaned & feature-engineered CSVs (gitignored)
├── notebooks/
│ ├── 01_data_ingestion.ipynb
│ ├── 02_data_cleaning.ipynb
│ ├── 03_eda.ipynb
│ ├── 04_timeseries_analysis.ipynb
│ ├── 05_feature_engineering.ipynb
│ └── 06_modeling.ipynb
├── src/
│ ├── cleaning/clean.py # Reusable cleaning functions (4 granularities)
│ └── ingestion/ingest.py # Full ETL pipeline, runnable via CLI
├── reports/
├── requirements.txt
└── README.md


---

## Key Findings

**Data Quality:** January 2017 showed every drug column at 0 — a complete data-logging failure, not a real business event (confirmed by comparing to surrounding months). Fixed using time-based interpolation between December 2016 and February 2017.

**Seasonality:** Sales consistently peak October–March (cold/flu season) and dip June–August, driven mainly by N02BE (Paracetamol) and R03 (respiratory drugs). Confirmed via seasonal decomposition and monthly groupby analysis.

**Operational patterns:** Hourly data reveals the pharmacy operates ~7 AM–8 PM with lunch (11–12) and closing-time (19–20) sales peaks; Saturday has the highest average daily sales, Thursday the lowest.

**Feature Importance:** In the winning Random Forest model, `rolling_mean_3` (recent 3-month trend) was by far the most predictive feature — more important than `lag_12` (same month last year). This suggests recent business momentum is a stronger signal than historical seasonal memory for this dataset.

---

## Model Results

| Model         | MAE     | RMSE    | MAPE   |
|---------------|---------|---------|--------|
| Naive         | 377.13  | 623.81  | 41.23% |
| ARIMA(1,0,1)  | 365.49  | 543.36  | 36.49% |
| SARIMA(1,0,1)(1,1,1,12) | 525.72 | 851.97 | 46.44% |
| **Random Forest** | **298.50** | **396.89** | **26.59%** |

Random Forest, using engineered lag/rolling/cyclical features, outperformed both classical statistical models — largely because SARIMA's seasonal coefficients were statistically unreliable given only 5 complete yearly cycles of training data.

---

## Key Decisions & Trade-offs

- **Kept zero-value hours** (pharmacy closed overnight) rather than removing them — they carry real business signal for forecasting.
- **Excluded `venv/`, `data/raw/`, `data/processed/`** from version control — regenerable via `requirements.txt` and documented data source, keeping the repo lightweight and git history meaningful.
- **Chose interpolation over row-deletion** for the January 2017 anomaly, since forecasting models need a continuous, unbroken time series.
- **Modularized cleaning logic** into `src/cleaning/clean.py`, separate from the ETL orchestration in `src/ingestion/ingest.py`, so cleaning functions are independently reusable and testable.

---

## How to Run

```bash
# 1. Clone the repository
git clone https://github.com/tapasvi2003/pharma-sales-forecasting.git
cd pharma-sales-forecasting

# 2. Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate      # Windows PowerShell

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download the dataset from Kaggle and place CSVs in data/raw/

# 5. Run the ETL pipeline
python src/ingestion/ingest.py

# 6. Explore analysis and modeling notebooks in order (01 → 06)
```

---

## Limitations

- Only 60 months of training data — insufficient for SARIMA's seasonal components to be statistically reliable.
- Dataset ends abruptly in October 2019 with a partial/incomplete final month, which no model could correctly anticipate.
- Forecasts are at the aggregate `total_sales` level; per-drug forecasting was not modeled separately.

---

## Author

Taraka Tapasvi
