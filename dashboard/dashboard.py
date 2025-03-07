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
    st.image("https://raw.githubusercontent.com/jasmineknsh/submission-AnalisisData/master/dashboard/pnyewaSepeda.jpg")
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

# Pola penyewaan sepeda terhadap kondisi cuaca
st.header("📈 Pola Penyewaan Sepeda per Kondisi Cuaca")

plt.figure(figsize=(15, 6))
sns.lineplot(x='date', y='count', hue='weathersit', data=hour_df)
plt.title('Pola Penyewaan Sepeda per Kondisi Cuaca')
plt.xlabel('Waktu')
plt.ylabel('Jumlah Penyewaan')
plt.grid(True)
st.pyplot(plt)

st.write("Bagaimana pengaruh kondisi cuaca dan musim terhadap pola penyewaan sepeda?")
with st.expander("ℹ️ Penjelasan"):
    st.write(
     """
     Analisis data menunjukkan bahwa kondisi cuaca dan musim memiliki pengaruh signifikan terhadap pola penyewaan sepeda.
     Cuaca cerah terbukti menjadi kondisi paling populer, dengan jumlah penyewaan tertinggi. Musim gugur mencatat jumlah penyewaan tertinggi (1,061,129)
     menunjukkan popularitasnya. Sebaliknya, kondisi cuaca buruk seperti hujan ringan/salju secara signifikan mengurangi jumlah penyewaan. Pola musiman menunjukkan puncak penyewaan di musim gugur dan penurunan di musim semi. Berdasarkan data analisis sebelumnya kondisi cuaca yang nyaman di musim gugur (temperatur hangat, angin tenang) 
     kemungkinan besar menjadi faktor utama yang mendorong jumlah penyewaan sepeda yang tinggi. Kondisi cuaca yang kurang nyaman di musim semi (temperatur sejuk, angin kencang) dapat menghambat aktivitas bersepeda dan mengurangi jumlah penyewaan.
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

st.header("📊 Pola waktu penyewaan")
g = sns.FacetGrid(hour_df, row='weekday', height=2, aspect=4)
g.map(sns.pointplot, 'hour', 'count')
g.set_axis_labels('Jam', 'Jumlah Penyewaan')
plt.show()
st.pyplot(plt)

st.write("Bagaimana pola penyewaan sepeda bervariasi berdasarkan hari dalam seminggu dan jam dalam sehari?")
with st.expander("ℹ️ Penjelasan"):
    st.write(
        """
        Berdasarkan grafik yang ditampilkan dari analisis dataframe pada hari kerja senin-jumat dapat diketahui pada 08.00 AM, 05.00 PM, 06.00 PM merupakan 3 puncak penyewaan sepeda tertinggi. secara jelas mengindikasikan pola perjalanan komuter. 
        Ini menegaskan bahwa sepeda banyak digunakan sebagai modal transportasi untuk berangkat dan pulang kerja. Pola ini memberikan peluang untuk menargetkan promosi dan layanan khusus bagi para komuter, seperti paket berlangganan bulanan atau diskon untuk penyewaan di jam-jam sibuk.
        Penyewaan di akhir pekan menunjukkan pola yang berbeda, dengan puncak yang lebih tersebar dari jam 08.00 AM - 08.00 PM. Untuk meningkatkan penyewaan di akhir pekan perusahaan dapat memberikan promosi khusus akhir pekan, seperti diskon untuk penyewaan keluarga, tur sepeda kelompok,
        atau acara komunitas. Dengan mengetahui jam-jam sibuk, perusahaan penyewaan sepeda dapat mengoptimalkan inventaris dan distribusi sepeda.
        """
    )

st.caption('Copyright © 2025 Jasmine Kinasih')
