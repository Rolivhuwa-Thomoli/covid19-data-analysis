"""
COVID-19 Data Analysis & Visualization
========================================
Comprehensive EDA of global COVID-19 trends.

Author: Rolivhuwa Thomoli
Date: June 2026
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("rocket")


def generate_covid_data(random_state=42):
    """Generate realistic COVID-19 time series data for top countries."""
    np.random.seed(random_state)

    countries = ['USA', 'India', 'Brazil', 'UK', 'Russia', 'France',
                 'Italy', 'Germany', 'South Korea', 'Japan']
    populations = [331000000, 1380000000, 213000000, 67000000, 146000000,
                   68000000, 59000000, 83000000, 52000000, 125000000]

    dates = pd.date_range('2020-01-22', '2023-06-01', freq='D')
    records = []

    for country, pop in zip(countries, populations):
        base_rate = np.random.uniform(0.02, 0.12)
        peak_day = np.random.randint(200, 400)
        peak_rate = np.random.uniform(0.08, 0.25)

        for i, date in enumerate(dates):
            day_num = i

            # Logistic growth model for cumulative cases
            growth = base_rate + (peak_rate - base_rate) * np.exp(-0.5 * ((day_num - peak_day) / 150) ** 2)
            daily_new = max(0, int(growth * pop / 10000 * np.random.uniform(0.7, 1.3)))

            cumulative = int(pop * base_rate * (1 / (1 + np.exp(-0.02 * (day_num - peak_day)))))

            mortality_rate = np.random.uniform(0.01, 0.035)
            recovery_rate = np.random.uniform(0.85, 0.97)

            deaths = int(cumulative * mortality_rate)
            recovered = int((cumulative - deaths) * recovery_rate)
            active = cumulative - deaths - recovered

            records.append({
                'country': country,
                'date': date,
                'confirmed': max(cumulative, 0),
                'deaths': max(deaths, 0),
                'recovered': max(recovered, 0),
                'active': max(active, 0),
                'new_cases': daily_new,
                'new_deaths': max(int(daily_new * mortality_rate), 0),
                'population': pop
            })

    df = pd.DataFrame(records)
    df['cases_per_million'] = (df['confirmed'] / df['population']) * 1000000
    df['deaths_per_million'] = (df['deaths'] / df['population']) * 1000000
    df['mortality_rate'] = (df['deaths'] / df['confirmed'].clip(lower=1)) * 100
    df['recovery_rate'] = (df['recovered'] / df['confirmed'].clip(lower=1)) * 100

    return df


def analyze_global_trends(df):
    """Analyze and visualize global COVID-19 trends."""
    print("\n📊 Analyzing Global Trends...")

    # Global daily trends
    global_daily = df.groupby('date')[['new_cases', 'new_deaths']].sum().reset_index()

    fig, axes = plt.subplots(2, 1, figsize=(14, 10))

    # New cases over time
    axes[0].fill_between(global_daily['date'], global_daily['new_cases'],
                          alpha=0.4, color='steelblue')
    axes[0].plot(global_daily['date'], global_daily['new_cases'],
                 color='steelblue', linewidth=1.5)
    axes[0].set_title('Global Daily New Cases', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('New Cases')

    # New deaths over time
    axes[1].fill_between(global_daily['date'], global_daily['new_deaths'],
                          alpha=0.4, color='coral')
    axes[1].plot(global_daily['date'], global_daily['new_deaths'],
                 color='coral', linewidth=1.5)
    axes[1].set_title('Global Daily New Deaths', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('New Deaths')
    axes[1].set_xlabel('Date')

    plt.tight_layout()
    plt.savefig('../images/global_trends.png', dpi=150, bbox_inches='tight')
    print("✅ Global trends plot saved")
    plt.close()

    # Summary statistics
    latest = df.groupby('country').last().reset_index()
    print("\n📈 Latest Statistics by Country:")
    print(latest[['country', 'confirmed', 'deaths', 'mortality_rate']]
          .sort_values('confirmed', ascending=False).to_string(index=False))

    return latest


def compare_countries(df):
    """Compare top affected countries."""
    print("\n🌍 Comparing Countries...")

    latest = df.groupby('country').last().reset_index()
    top10 = latest.nlargest(10, 'confirmed')

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # Total cases
    axes[0, 0].barh(top10['country'], top10['confirmed'] / 1e6, color='steelblue')
    axes[0, 0].set_xlabel('Confirmed Cases (Millions)')
    axes[0, 0].set_title('Top 10 Countries - Total Cases', fontweight='bold')
    axes[0, 0].invert_yaxis()

    # Cases per million
    axes[0, 1].barh(top10['country'], top10['cases_per_million'], color='coral')
    axes[0, 1].set_xlabel('Cases per Million')
    axes[0, 1].set_title('Top 10 Countries - Cases per Capita', fontweight='bold')
    axes[0, 1].invert_yaxis()

    # Mortality rate
    axes[1, 0].bar(top10['country'], top10['mortality_rate'], color='firebrick')
    axes[1, 0].set_ylabel('Mortality Rate (%)')
    axes[1, 0].set_title('Mortality Rate by Country', fontweight='bold')
    axes[1, 0].tick_params(axis='x', rotation=45)

    # Recovery rate
    axes[1, 1].bar(top10['country'], top10['recovery_rate'], color='mediumseagreen')
    axes[1, 1].set_ylabel('Recovery Rate (%)')
    axes[1, 1].set_title('Recovery Rate by Country', fontweight='bold')
    axes[1, 1].tick_params(axis='x', rotation=45)

    plt.suptitle('COVID-19 Country Comparison', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('../images/top_countries.png', dpi=150, bbox_inches='tight')
    print("✅ Country comparison plot saved")
    plt.close()


def mortality_analysis(df):
    """Analyze mortality patterns."""
    print("\n💀 Analyzing Mortality Patterns...")

    latest = df.groupby('country').last().reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Mortality vs Cases per million
    axes[0].scatter(latest['cases_per_million'], latest['mortality_rate'],
                     s=latest['population'] / 2e6, alpha=0.6, color='firebrick', edgecolors='white')
    for _, row in latest.iterrows():
        axes[0].annotate(row['country'], (row['cases_per_million'], row['mortality_rate']),
                          fontsize=9, xytext=(5, 5), textcoords='offset points')
    axes[0].set_xlabel('Cases per Million')
    axes[0].set_ylabel('Mortality Rate (%)')
    axes[0].set_title('Mortality Rate vs Case Density', fontweight='bold')

    # Deaths per million
    sorted_deaths = latest.sort_values('deaths_per_million', ascending=True)
    axes[1].barh(sorted_deaths['country'], sorted_deaths['deaths_per_million'],
                  color='darkred', alpha=0.7)
    axes[1].set_xlabel('Deaths per Million')
    axes[1].set_title('Deaths per Capita by Country', fontweight='bold')

    plt.tight_layout()
    plt.savefig('../images/mortality_analysis.png', dpi=150, bbox_inches='tight')
    print("✅ Mortality analysis plot saved")
    plt.close()


def correlation_analysis(df):
    """Create correlation matrix of key metrics."""
    print("\n🔗 Correlation Analysis...")

    latest = df.groupby('country').last().reset_index()
    corr_features = ['confirmed', 'deaths', 'active', 'mortality_rate',
                     'cases_per_million', 'deaths_per_million']
    corr_matrix = latest[corr_features].corr()

    plt.figure(figsize=(10, 8))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='RdBu_r', center=0,
                fmt='.2f', linewidths=0.5, square=True)
    plt.title('COVID-19 Metrics Correlation Matrix', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('../images/correlation_matrix.png', dpi=150, bbox_inches='tight')
    print("✅ Correlation matrix saved")
    plt.close()


def main():
    """Execute COVID-19 analysis pipeline."""
    import os
    os.makedirs('../images', exist_ok=True)
    os.makedirs('../data', exist_ok=True)

    print("=" * 60)
    print("COVID-19 DATA ANALYSIS & VISUALIZATION")
    print("=" * 60)

    # Generate data
    print("\n🔄 Generating COVID-19 dataset...")
    df = generate_covid_data()
    df.to_csv('../data/covid_data.csv', index=False)
    print(f"✅ Dataset: {df.shape}")
    print(f"   Countries: {df['country'].nunique()}")
    print(f"   Date range: {df['date'].min()} to {df['date'].max()}")

    # Analysis
    latest = analyze_global_trends(df)
    compare_countries(df)
    mortality_analysis(df)
    correlation_analysis(df)

    print("\n" + "=" * 60)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 60)
    print("\n📁 Generated files:")
    print("   - data/covid_data.csv")
    print("   - images/global_trends.png")
    print("   - images/top_countries.png")
    print("   - images/mortality_analysis.png")
    print("   - images/correlation_matrix.png")


if __name__ == "__main__":
    main()
