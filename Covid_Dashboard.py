import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")

# Title
st.title("🦠 COVID-19 Data Analysis Dashboard")

# Load data
@st.cache_data
def load_data():
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    df = pd.read_csv(url, parse_dates=['date'])
    return df

df = load_data()

# Sidebar filters
countries = ['United States', 'India', 'Pakistan']
selected_countries = st.sidebar.multiselect("Select countries:", countries, default=countries)

# Filter by selected countries
data = df[df['location'].isin(selected_countries)]

# Global daily new cases plot
st.subheader("📈 Daily New Cases (7-Day Avg)")
data['new_cases_7d'] = data.groupby('location')['new_cases'].transform(lambda x: x.rolling(7).mean())
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=data, x='date', y='new_cases_7d', hue='location', ax=ax)
ax.set_title("Smoothed Daily New COVID-19 Cases")
ax.set_ylabel("New Cases (7-day avg)")
ax.set_xlabel("Date")
st.pyplot(fig)

# Total cases per 100k population
st.subheader("🌍 Total Cases per 100,000 People")
latest = df.sort_values('date').groupby('location').last().reset_index()
latest = latest.dropna(subset=['total_cases', 'population', 'continent'])
latest['cases_per_100k'] = (latest['total_cases'] / latest['population']) * 100000
bar_data = latest[latest['location'].isin(selected_countries)]

fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.barplot(data=bar_data, x='location', y='cases_per_100k', palette='Blues_d', ax=ax2)
ax2.set_title("Cases per 100k People")
ax2.set_ylabel("Cases per 100k")
st.pyplot(fig2)

# Vaccination trend
st.subheader("💉 Total Vaccinations Over Time")
vax_data = data[data['total_vaccinations'].notnull()]
fig3, ax3 = plt.subplots(figsize=(12, 5))
sns.lineplot(data=vax_data, x='date', y='total_vaccinations', hue='location', ax=ax3)
ax3.set_title("Total COVID-19 Vaccinations")
ax3.set_ylabel("Vaccinations")
ax3.set_xlabel("Date")
st.pyplot(fig3)

# Footer
st.markdown("---")
st.markdown("Made by **Zaid Ahmad** | Data Source: [Our World in Data](https://ourworldindata.org/covid-deaths)")
