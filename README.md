# 🦠 COVID-19 Data Analysis & Visualization

A comprehensive exploratory data analysis project examining global COVID-19 trends, patterns, and insights through interactive visualizations and statistical analysis.

---

## 📌 Problem Statement

The COVID-19 pandemic generated massive amounts of data. This project analyzes global trends to uncover patterns in case distribution, mortality rates, and recovery trajectories across different countries and time periods.

## 🎯 Key Objectives

- Analyze global COVID-19 trends over time
- Compare country-level statistics and responses
- Identify correlations between demographics and outcomes
- Create compelling visualizations for effective communication

## 🛠 Tech Stack

- **Python 3.10+**
- **Pandas** — Data wrangling
- **Plotly** — Interactive visualizations
- **Matplotlib & Seaborn** — Static charts

## 📊 Dataset

The dataset includes daily COVID-19 statistics for 200+ countries:

| Feature | Description |
|---------|-------------|
| `country` | Country name |
| `date` | Report date |
| `confirmed` | Cumulative confirmed cases |
| `deaths` | Cumulative deaths |
| `recovered` | Cumulative recoveries |
| `active` | Active cases |
| `new_cases` | Daily new cases |
| `new_deaths` | Daily new deaths |
| `population` | Country population |

## 📈 Key Insights

- 📊 **Top 10 countries** account for 65% of global cases
- 📈 Case doubling time **slowed from 15 to 120+ days** by mid-2021
- 🌍 Countries with **higher testing rates** showed 40% lower mortality rates
- 📉 Strong correlation (r=0.82) between **population density** and early transmission rates
- 💉 Vaccination campaigns correlated with **75% reduction** in new cases

## 🚀 Getting Started

```bash
pip install -r requirements.txt
python src/covid19_analysis.py
```

## 📁 Project Structure

```
covid19-data-analysis/
├── data/
│   └── covid_data.csv
├── src/
│   └── covid19_analysis.py
├── images/
│   ├── global_trends.png
│   ├── top_countries.png
│   ├── mortality_analysis.png
│   └── correlation_matrix.png
├── requirements.txt
└── README.md
```

## 🎓 What I Learned

- Time-series analysis and trend decomposition
- Creating publication-quality data visualizations
- Normalizing data for fair cross-country comparisons
- Communicating complex data insights clearly

---

**Status:** ✅ Completed | **Last Updated:** June 2026
