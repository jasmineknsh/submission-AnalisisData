import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Helper function untuk menyiapkan berbagai DataFrame
def create_daily_rent_df(hour_df):
    hour_df['date'] = pd.to_datetime(hour_df['date'])
    daily_rent_df = hour_df.resample(rule='D', on='date').agg({"count": "sum"}).reset_index()
    daily_rent_df.rename(columns={"count": "total_rentals"}, inplace=True)
    return daily_rent_df

def get_total_rentals(daily_rent_df, start_date, end_date):
    start_date, end_date = pd.to_datetime(start_date), pd.to_datetime(end_date)
    filtered_df = daily_rent_df[(daily_rent_df["date"] >= start_date) & (daily_rent_df["date"] <= end_date)]
    return filtered_df["total_rentals"].sum()

def create_by_season_df(hour_df):
    season_df = hour_df.groupby(by='season', observed=True).agg({
        "count": "sum"
    }).reset_index() 
    return season_df

def create_bywheatersit_df(hour_df):
    weather_by_season = hour_df.groupby('season', observed=True)[['temp', 'atemp', 'hum', 'windspeed']].agg([
        'mean', 'sum']).reset_index()
    return weather_by_season

def create_hourly_df(hour_df):
    hourly_df = hour_df.groupby(by='hour').agg({'count': 'sum'}).reset_index()
    return hourly_df

# Load dataset
hour_df = pd.read_csv("https://raw.githubusercontent.com/jasmineknsh/submission-AnalisisData/master/dashboard/main_data.csv")

hour_df["date"] = pd.to_datetime(hour_df["date"])

# Dataframe
daily_rent_df = create_daily_rent_df(hour_df)
byseason_df = create_by_season_df(hour_df)
daily_hourly_df = create_hourly_df(hour_df)
weather_by_season = create_by_season_df(hour_df)
hourly_df = create_hourly_df(hour_df)

# filter
min_date = daily_rent_df["date"].min().date()
max_date = daily_rent_df["date"].max().date()

# Sidebar 
with st.sidebar:
    st.image("pnyewaSepeda.jpg")
    st.sidebar.header("Filter:")
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter dataset berdasarkan tanggal yang dipilih
hour_df = hour_df[(hour_df["date"] >= str(start_date)) & (hour_df["date"] <= str(end_date))]

# Hitung total rentals berdasarkan filter tanggal
total_rentals_selected = get_total_rentals(daily_rent_df, start_date, end_date)



st.title('📊 Dashboard Penyewaan Sepeda')

col1, col2 = st.columns([1, 2])

with col1:
    st.metric("Total Rental dalam Rentang Waktu", value=f"{total_rentals_selected:,}")

with col2:
    st.subheader("📈 Tren Penyewaan Harian")
    filtered_df = daily_rent_df[
        (daily_rent_df["date"] >= pd.to_datetime(start_date)) &
        (daily_rent_df["date"] <= pd.to_datetime(end_date))
    ]
    st.line_chart(filtered_df.set_index("date")["total_rentals"], use_container_width=True)


# --- STATISTIK PENYEWAAN PER MUSIM ---
st.subheader('🌦 Statistik Penyewaan per Musim')

with st.container():
    
    season_df = create_by_season_df(hour_df)

    plt.figure(figsize=(10, 6))
    sns.barplot(x='season', y='count', data=season_df) 
    plt.title('Total Penyewaan Sepeda per Musim') 
    plt.xlabel('Musim')
    plt.ylabel('Total Jumlah Penyewaan') 

    st.pyplot(plt)

# --- VISUALISASI CUACA PER MUSIM ---
st.subheader('🌡️ Statistik Cuaca Rata-rata per Musim')

with st.container():
    
    weather_by_season = create_bywheatersit_df(hour_df)

    sum_data = weather_by_season.xs('mean', level=1, axis=1)

    plt.figure(figsize=(12, 6)) 
    sum_data.plot(kind='bar', figsize=(12, 6), ax=plt.gca())  

    plt.title('Rata-rata Nilai Cuaca per Musim') 
    plt.xlabel('Musim')
    plt.ylabel('Nilai Rata-rata')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)
    st.write(
    """
    Keterangan :   
    0 = Musim Semi
    1 = Musim Panas
    2 = Musim Gugur
    3 = Musim Dingin 
    """
)

with st.expander("ℹ️ Penjelasan"):
    st.write(
        """
        **1. 🌱 Musim Semi (Spring):**  
        - Temperatur lebih tinggi dibanding musim dingin  
        - Kecepatan angin tertinggi, menunjukkan kondisi angin lebih kencang  

        **2. ☀️ Musim Panas (Summer):**  
        - Temperatur tinggi, tetapi sedikit lebih rendah dari musim gugur  
        - Kecepatan angin sedikit lebih tinggi dari musim gugur  

        **3. 🍂 Musim Gugur (Fall):**  
        - Temperatur tertinggi, menunjukkan kondisi paling hangat  
        - Kecepatan angin terendah, menunjukkan kondisi angin paling tenang  

        **4. ❄️ Musim Dingin (Winter):**  
        - Temperatur terendah, menunjukkan kondisi paling dingin  
        - Kecepatan angin rendah, tetapi lebih tinggi dari musim gugur  
        """
    )

# Visualisasi Persebaran Jam Penyewaan
st.header("🕰️ Puncak waktu penyewaan")
hourly_df = create_hourly_df(hour_df)
    
plt.figure(figsize=(12, 6))
plt.bar(hourly_df['hour'], hourly_df['count'])
plt.xlabel('Jam')
plt.ylabel('Jumlah Penyewaan')
plt.title('Distribusi Penyewaan Sepeda per Jam')
plt.xticks(range(24))
st.pyplot(plt)

st.write(
    """
    Berdasarkan grafik yang ditampilkan dari analisis dataframe pada kolom hour dapat diketahui pada 08.00 AM, 05.00 PM, 06.00 PM merupakan 3 puncak penyewaan sepeda tertinggi.
    secara jelas mengindikasikan pola perjalanan komuter. Ini menegaskan bahwa sepeda banyak digunakan sebagai moda transportasi untuk berangkat dan pulang kerja.
    """
)

st.caption('Copyright © 2025 Jasmine Kinasih')
