# Nama       : Zidan Fadlurorhman               |
# Email      : fadlurrohman.zidan@gmail.com     |
# ID Dicoding: zidan_fad                        |
#================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator
sns.set(style='dark')

#load dataset
@st.cache_resource
# def load_hour_data():
#     dataset = pd.read_csv("hour_data.csv")
#     return dataset

hour_dataset = pd.read_csv("hour_data.csv")

@st.cache_resource
# def load_day_data():
#     dataset = pd.read_csv("day_data.csv")
#     return dataset

day_dataset = pd.read_csv("day_data.csv")

#title
st.title("Bike Share Dashboard")

#Author Information
st.write("""
    **Author Information**
    - Name       : Zidan Fadlurrohman
    - Email      : fadlurrohman.zidan@gmail.com 
    - Dicoding ID: zidan_fad    
""")
st.write('*5 March 2024*')


st.subheader("Description")
st.write(
    """
    Bike sharing systems are a new generation of traditional bike rentals, automating the membership, rental, and return process. 
    With over 500 programs worldwide, these systems play a crucial role in traffic, environmental, and health issues. 
    They generate data that can be used as a virtual sensor network, allowing for the detection of important city events and improving urban mobility.
    """
)

st.subheader("Raw Data")
st.markdown("""
        **Dataset Characterization**
        - **instant**: Record index
        - **dteday**: Date
        - **season**: Season (springer, summer, fall, winter)
        - **yr**: Year (Jan 2011 - Dec 2012)
        - **mnth**: Month (January - December)
        - **hr**: Hour (0 to 23)
        - **holiday**: Weather day is holiday or not. [Holiday Schedule](http://dchr.dc.gov/page/holiday-schedule)
        - **weekday**: Day of the week
        - **workingday**: If day is neither weekend nor holiday is 1, otherwise is 0.
        - **weathersit**: 
            - Good: Clear, Few clouds, Partly cloudy, Partly cloudy
            - Moderate: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
            - Bad: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
            - Severe: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog
        - **temp**: Normalized temperature in Celsius. The values are divided to 41 (max)
        - **atemp**: Normalized feeling temperature in Celsius. The values are divided to 50 (max)
        - **hum**: Normalized humidity. The values are divided to 100 (max)
        - **windspeed**: Normalized wind speed. The values are divided to 67 (max)
        - **casual**: Count of casual users
        - **registered**: Count of registered users
        - **cnt**: Count of total rental bikes including both casual and registered
    """)
st.write('**Dataset**')
st.write(hour_dataset)   

# Display summary statistics
st.subheader("Summary")
st.write(hour_dataset.describe())


st.subheader('Trend of Bike Rentals Over Time')
fig, ax = plt.subplots(figsize=(20, 6))
sns.lineplot(x='dteday', y='cnt', data=hour_dataset, ax=ax)  # 'hour' instead of 'dataset'
ax.set_ylabel('Count', fontsize=20)  # Adjust as needed
ax.set_xlabel('Date', fontsize=20) 
ax.xaxis.set_major_locator(MaxNLocator(nbins=12, prune='both')) 
plt.xticks(rotation=45, fontsize=10)
st.pyplot(fig)


st.subheader('Bike Rentals by Month and Year')
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x="mnth", y="cnt", data=hour_dataset, hue="yr", ax=ax)
plt.xlabel('Month', fontsize=16)  
plt.ylabel('Count of Rental Bikes', fontsize=16) 
st.pyplot(fig)


def plot_bar_graphs(column):
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    sns.barplot(x=column, y='cnt', data=hour_dataset, ax=axs[0])
    axs[0].set_title(f'Bar Plot of {column}')
    sns.barplot(x=column, y='cnt', data=day_dataset, hue='yr', palette='Set3', ax=axs[1])
    axs[1].set_title(f'Bar Plot of {column} in 2011 and 2012')
    axs[1].legend(title='yr', labels=['2011', '2012'])
    fig.tight_layout()
    st.pyplot(fig)


st.subheader('Bar Plots by Month')
plot_bar_graphs('mnth')


st.subheader('Bar Plots by Season')
plot_bar_graphs('season')

#Q1 scatter plot
st.subheader('Q1 Bike Rental by Weather Condition')
q1_2011_data = hour_dataset[hour_dataset['mnth'].str.lower().isin(['jan', 'feb', 'mar'])]
fig, ax = plt.subplots(figsize=(20, 6))
sns.lineplot(
    x='dteday', y='cnt', data=q1_2011_data, hue='weathersit', style='weathersit',
    linewidth=2, markers=True, ci=None, err_kws={'zorder': 0}, legend='full', ax=ax
)

plt.title('Q1 Bike Rentals 2011 by Weather Condition')
plt.xlabel('Date')
plt.ylabel('Number of Rental Bikes')
ax.xaxis.set_major_locator(MaxNLocator(nbins=12, prune='both')) 
plt.xticks(rotation=45, fontsize=10)
plt.tight_layout()
st.pyplot(fig)

#Q1 scatter plot
q1_good = q1_2011_data[(q1_2011_data['weathersit'] == 'good')]
q1_moderate = q1_2011_data[(q1_2011_data['weathersit'] == 'moderate')]
q1_bad = q1_2011_data[(q1_2011_data['weathersit'] == 'bad')]
q1_severe = q1_2011_data[(q1_2011_data['weathersit'] == 'severe')]

fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(data=q1_good, x="dteday", y="cnt", facecolor="blue", label="Good", ax=ax)
sns.scatterplot(data=q1_moderate, x="dteday", y="cnt", facecolor="lightgreen", label="Moderate", ax=ax)
sns.scatterplot(data=q1_bad, x="dteday", y="cnt", facecolor="orange", label="Bad", ax=ax)
sns.scatterplot(data=q1_severe, x="dteday", y="cnt", facecolor="crimson", label="Severe", ax=ax)
ax.xaxis.set_major_locator(MaxNLocator(nbins=12, prune='both')) 
plt.xticks(rotation=45, fontsize=10)
plt.legend(title="Weather Condition")
plt.xlabel('Date')
plt.ylabel('Count of Rental Bikes')
st.pyplot(fig)


st.subheader('Bike Sharing by Hour per Day')
fig, ax = plt.subplots(figsize=(15, 6))
sns.pointplot(x="hr", y="cnt", hue="weekday", data=hour_dataset, ax=ax)

plt.title('Bike Sharing by Hour per Day')
plt.xlabel('Hour of the Day')
plt.ylabel('Count of Rental Bikes')
st.pyplot(fig)


st.subheader('Bar Plots by Workingday')
plot_bar_graphs('workingday')
