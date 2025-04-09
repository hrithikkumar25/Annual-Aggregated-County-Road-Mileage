import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 1. Load the dataset
df = pd.read_csv("C:\\Users\\hrith\\Downloads\\cleaned_python_ca2_dataset.csv")
print(df.head())
print(df.tail())
print(df.describe())
print(df.columns)
print(df.dropna())


# 2. Clean column names
df.columns = df.columns.str.strip().str.lower()

# 3. Set correct columns manually
county_col = 'county_name'
mileage_col = 'total_centerline_miles'
year_col = 'calendar_year'
paved_col = 'is_paved'


# 1. County-Wise Road Distribution – Bar Chart

county_mileage = df.groupby(county_col)[mileage_col].sum().sort_values(ascending=False)

plt.figure(figsize=(12,6))
county_mileage.plot(kind='bar', color='skyblue')
plt.title('County-Wise Total Road Mileage')
plt.xlabel('County')
plt.ylabel('Total Centerline Miles')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


# 2. Yearly Road Mileage Trends – Line Chart

yearly_mileage = df.groupby(year_col)[mileage_col].sum()

plt.figure(figsize=(10,5))
yearly_mileage.plot(kind='line', marker='o', color='green')
plt.title('Yearly Road Mileage Trends')
plt.xlabel('Year')
plt.ylabel('Total Centerline Miles')
plt.grid(True)
plt.tight_layout()
plt.show()


# 3. Road Mileage Density per Population – Scatter Plot


# Generate  population data for counties
np.random.seed(42)
population = pd.Series(np.random.randint(10000, 500000, size=df[county_col].nunique()), 
                            index=df[county_col].unique())

# Merge population back to main dataframe
df['population'] = df[county_col].map(population)

# Group by county
county_stats = df.groupby(county_col).agg({
    mileage_col: 'sum',
    'population': 'mean'
}).reset_index()

# Scatter plot
plt.figure(figsize=(8,6))
sns.scatterplot(data=county_stats, x='population', y=mileage_col)
plt.title('Road Mileage vs Population')
plt.xlabel('Population')
plt.ylabel('Total Centerline Miles')
plt.grid(True)
plt.tight_layout()
plt.show()

# 4. Road Type Breakdown (Paved vs Unpaved) – Pie Chart


paved_counts = df[paved_col].value_counts()

plt.figure(figsize=(6,6))
paved_counts.plot(kind='pie', autopct='%1.1f%%', labels=['Paved', 'Unpaved'], colors=['#66b3ff','#ff9999'])
plt.title('Road Type Breakdown (Paved vs Unpaved)')
plt.ylabel('')
plt.tight_layout()
plt.show()

# 5. State vs. County Road Mileage Comparison – Donut Chart


# Assume the "State Total" is sum of all counties
state_total = df[mileage_col].sum()

county_totals = df.groupby(county_col)[mileage_col].sum()

# Create pie (donut) chart
plt.figure(figsize=(8,8))
plt.pie(county_totals, labels=county_totals.index, autopct='%1.1f%%', pctdistance=0.85)
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.title('County Contribution to Total State Road Mileage')
plt.tight_layout()
plt.show()
