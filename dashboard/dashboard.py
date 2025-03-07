import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
# import datetime

sns.set(style='dark')
#Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
# byseason_df = create_byseason_df(main_df)
def create_byseason_df(hour_df):
    season_df = hour_df.groupby(by='season', observed=True).agg({
        "count": "sum"
    }).reset_index() 
    return season_df

# daily_hourly_df = create_daily_hourly_df(main_df)
# daily_weekday_df = create_daily_weekday_df(main_df)
# bywheathersit_df = create_bywheathersit_df(main_df)
# byholiday_df = create_byholiday(main_df)
# weather_by_season_df = create_weather_by_season_df (main_df)

# Upload clean data
hour_df = pd.read_csv("main_data.csv")

#komponen filter
min_date = hour_df["date"].min()
max_date = hour_df["date"].max()

with st.sidebar:
    # add capital bikeshare logo
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    st.sidebar.header("Filter:")

    # mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = hour_df[(hour_df["date"] >= str(start_date)) & 
                (hour_df["date"] <= str(end_date))]


byseason_df = create_byseason_df(main_df)
# daily_hourly_df = create_daily_hourly_df(main_df)
# daily_weekday_df = create_daily_weekday_df(main_df)
# bywheathersit_df = create_bywheathersit_df(main_df)
# byholiday_df = create_byholiday(main_df)
# weather_by_season_df = create_weather_by_season_df (main_df)

# corr_atemp_wheatersit_df = create_rfm_df(main_df)

st.title('Pengembangan Dashboard Bike Sharing')

st.header('Statistik Penyewaan per Musim')

with st.container():
    st.write("Inside the container")
    
    x = np.random.normal(15, 5, 250)
 
    fig, ax = plt.subplots()
    ax.hist(x=x, bins=15)
    st.pyplot(fig) 
 
st.write("Outside the container")

with st.expander("See explanation"):
    st.write(
        """Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
        sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris 
        nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor 
        in reprehenderit in voluptate velit esse cillum dolore eu fugiat 
        nulla pariatur. Excepteur sint occaecat cupidatat non proident, 
        sunt in culpa qui officia deserunt mollit anim id est laborum.
        """
    )

st.caption('Copyright (c) Jasmine Kinasih')
