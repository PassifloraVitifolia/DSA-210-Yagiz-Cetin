# -*- coding: utf-8 -*-
"""Merged_Airbnb_Crime_Analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1m-8XJkpbHrpq-LNZ5ggsC2h0AERSSE5B

# 📘 Comprehensive Analysis: Airbnb Pricing and Crime Data
This notebook merges two analyses covering:
- Individual Airbnb listing data from six U.S. states
- Master dataset with average prices
- Crime statistics (robbery, assault per 100k residents)

We explore the data using descriptive statistics, visualizations, and correlation analysis.

## 📊 Initial Data Exploration
We'll start by examining the merged dataset: Airbnb prices and crime rates per state.
"""

import pandas as pd
merged_data = pd.read_csv("/mnt/data/merged_crime_airbnb_data.csv")

merged_data.head()

merged_data.info()

merged_data.describe()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr

merged_data = pd.read_csv("/mnt/data/merged_crime_airbnb_data.csv")

sns.set_style("whitegrid")

fig, ax1 = plt.subplots(figsize=(14,8))

crime_scores = (merged_data['Robbery_per_100k'] + merged_data['Assault_per_100k']) / 2
ax1.bar(merged_data['State'], crime_scores, color='red', width=0.4, label='Average Crime Rate', align='center')

ax2 = ax1.twinx()
ax2.bar(merged_data['State'], merged_data['Average_Price'], color='blue', width=0.4, label='Average Airbnb Price', align='edge')

ax1.set_xlabel('State')
ax1.set_ylabel('Crime Rate (per 100k)', color='red')
ax2.set_ylabel('Average Airbnb Price (USD)', color='blue')

plt.title('Crime Rate and Airbnb Price by State')
fig.tight_layout()
plt.show()

pearson_robbery = pearsonr(merged_data['Robbery_per_100k'], merged_data['Average_Price'])
pearson_assault = pearsonr(merged_data['Assault_per_100k'], merged_data['Average_Price'])

spearman_robbery = spearmanr(merged_data['Robbery_per_100k'], merged_data['Average_Price'])
spearman_assault = spearmanr(merged_data['Assault_per_100k'], merged_data['Average_Price'])

print("--- Pearson Correlations ---")
print(f"Robbery vs Airbnb Price: r = {pearson_robbery[0]:.3f}, p-value = {pearson_robbery[1]:.4f}")
print(f"Assault vs Airbnb Price: r = {pearson_assault[0]:.3f}, p-value = {pearson_assault[1]:.4f}\n")

print("--- Spearman Correlations ---")
print(f"Robbery vs Airbnb Price: rho = {spearman_robbery.correlation:.3f}, p-value = {spearman_robbery.pvalue:.4f}")
print(f"Assault vs Airbnb Price: rho = {spearman_assault.correlation:.3f}, p-value = {spearman_assault.pvalue:.4f}")

correlation_results = pd.DataFrame({
    'Metric': ['Pearson Robbery', 'Pearson Assault', 'Spearman Robbery', 'Spearman Assault'],
    'Correlation': [
        pearson_robbery[0],
        pearson_assault[0],
        spearman_robbery.correlation,
        spearman_assault.correlation
    ]
})

plt.figure(figsize=(10,6))
sns.barplot(data=correlation_results, x='Metric', y='Correlation', palette='coolwarm')
plt.title('Correlation between Crime Rates and Airbnb Prices')
plt.ylabel('Correlation Coefficient')
plt.ylim(-1, 1)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

"""## 🔄 Merged Notebook: Additional Airbnb and Crime Analysis

# 📊 Airbnb and Crime Data Analysis
This notebook explores Airbnb pricing and crime statistics across various U.S. states. It includes:
- Visual analysis of Airbnb listings in six cities
- Aggregated Airbnb prices from a master dataset
- Crime rate comparisons (robbery and assault) by state
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='whitegrid')

# File paths and data loading
files = {
    'California': '/mnt/data/final_airbnb_california_cleaned.csv',
    'New York': '/mnt/data/final_airbnb_newyork_cleaned.csv',
    'Oregon': '/mnt/data/final_airbnb_oregon_cleaned.csv',
    'Rhode Island': '/mnt/data/final_airbnb_rhodeisland_cleaned.csv',
    'Texas': '/mnt/data/final_airbnb_texas_cleaned.csv',
    'Washington': '/mnt/data/final_airbnb_washington_cleaned.csv',
    'Master Airbnb': '/mnt/data/master_airbnb_prices.csv',
    'Crime': '/mnt/data/final_crime_data.csv'
}

# Load city-level Airbnb data
city_dfs = {city: pd.read_csv(path) for city, path in files.items() if city not in ['Master Airbnb', 'Crime']}
master_airbnb_df = pd.read_csv(files['Master Airbnb'])
crime_df = pd.read_csv(files['Crime'])

"""## 🗂 Dataset Descriptions
- **City-level Airbnb datasets**: Contain listing-level pricing and metadata.
- **Master Airbnb dataset**: Average prices aggregated per state.
- **Final crime dataset**: State-level crime rates per 100,000 people.

## 📉 Airbnb Price Distributions by City
"""

# Plot Airbnb price distributions for each city
for city, df in city_dfs.items():
    plt.figure(figsize=(10, 5))
    sns.histplot(df['price'], kde=True, bins=30)
    plt.title(f'Price Distribution in Airbnb Listings - {city}')
    plt.xlabel('Price (USD)')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()

"""## 📊 Master Airbnb Dataset"""

master_airbnb_df.head()

plt.figure(figsize=(12, 6))
sns.barplot(data=master_airbnb_df, x='State', y='Average_Price', palette='Blues_d')
plt.title('Average Airbnb Price by State (Master Data)')
plt.ylabel('Average Price (USD)')
plt.xlabel('State')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

"""## 🕵️‍♂️ Final Crime Dataset"""

crime_df.head()

# Plot Crime Rates by State (Robbery and Assault only)
available_crime_cols = [col for col in ['Robbery_per_100k', 'Assault_per_100k'] if col in crime_df.columns]
plt.figure(figsize=(12, 6))
crime_long = crime_df.melt(id_vars='State', value_vars=available_crime_cols,
                           var_name='Crime_Type', value_name='Rate_per_100k')
sns.barplot(data=crime_long, x='State', y='Rate_per_100k', hue='Crime_Type')
plt.title('Crime Rates per 100k People by State')
plt.xlabel('State')
plt.ylabel('Rate per 100,000 People')
plt.xticks(rotation=45)
plt.legend(title='Crime Type')
plt.tight_layout()
plt.show()