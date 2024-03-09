import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')
plt.style.use('dark_background')
# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

def create_casual_register_df(df):
    casual_year_df = df.groupby("yr")["casual"].sum().reset_index()
    casual_year_df.columns = ["yr", "total_casual"]
    reg_year_df = df.groupby("yr")["registered"].sum().reset_index()
    reg_year_df.columns = ["yr", "total_registered"]  
    casual_register_df = casual_year_df.merge(reg_year_df, on="yr")
    return casual_register_df

def create_monthly_df(df):
    monthly_df = df.groupby(by=["mnth","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return monthly_df

def create_hourly_df(df):
    hourly_df = df.groupby(by=["hr","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return hourly_df

def create_byholiday_df(df):
    holiday_df = df.groupby(by=["holiday","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return holiday_df

def create_byworkingday_df(df):
    workingday_df = df.groupby(by=["workingday","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return workingday_df

def create_byseason_df(df):
    season_df = df.groupby(by=["season","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return season_df

def create_byweather_df(df):
    weather_df = df.groupby(by=["weathersit","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return weather_df

# Load cleaned data
bike_day = pd.read_csv("day.csv", encoding="utf-8")
bike_hour = pd.read_csv("hour.csv")

# Filter data
bike_day["dteday"] = pd.to_datetime(bike_day["dteday"])
bike_hour["dteday"] = pd.to_datetime(bike_hour["dteday"])
min_date = bike_day["dteday"].min()
max_date = bike_day["dteday"].max()

with st.sidebar:
    # Menambahkan logo 
    st.image("logoBike.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = bike_day[(bike_day["dteday"] >= str(start_date)) & 
                    (bike_day["dteday"] <= str(end_date))]

second_df = bike_hour[(bike_hour["dteday"] >= str(start_date)) & 
                    (bike_hour["dteday"] <= str(end_date))]


# # Menyiapkan berbagai dataframe
casual_register_df = create_casual_register_df(main_df)
monthly_df = create_monthly_df(main_df)
hourly_df = create_hourly_df(second_df)
holiday_df = create_byholiday_df(main_df)
workingday_df = create_byworkingday_df(main_df)
season_df = create_byseason_df(main_df)
weather_df = create_byweather_df(main_df)
hourly_df = hourly_df.replace({
    "yr": {0: 2011, 1: 2012}
})

# Menggabungkan kedua data
bike_df = bike_hour.merge(bike_day, on='dteday', how='inner', suffixes=('_hour', '_day'))

# Mendefinisikan label cuaca
weather_labels = {
    1: 'Jernih',
    2: 'Kabut',
    3: 'Curah Hujan Ringan',
    4: 'Curah Hujan Lebat'
}
bike_df['weather_label'] = bike_df['weathersit_day'].map(weather_labels)

st.header('PedalPulse : Bike Sharing Insights')
# Membuat visualisasi rata-rata sewa sepeda per jam
st.subheader("Statistik Rata - Rata Penyewaan Sepeda Berdasarkan Variasi Sepanjang Hari")
rental_hr = bike_df.groupby('hr')['cnt_hour'].mean()
fig, ax = plt.subplots()
ax.bar(rental_hr.index, rental_hr.values, color='#1E6EB6')
ax.set_title('Rata - Rata Sewa Sepeda per Jam')
ax.set_xlabel('Jam')
ax.set_ylabel('Rata - Rata Sewa')
plt.tight_layout()
st.pyplot(fig)
with st.expander('Keterangan'):
    st.write(
        """
        Rata rata Sewa Sepeda paling banyak terjadi jam 17.00 dan 18.00 atau jam 5 PM dan 6 PM. Dengan jumlah rata-rata sewa sepeda melebihi angka 400. 
        Namun rata rata sewa sepeda paling sedikit terjadi jam 04.00 atau jam 4 AM. Dengan jumlah rata-rata sewa sepeda kurang lebih 10.
        """
    )

# Membuat visualisasi rata-rata sewa sepeda berdasarkan kondisi cuaca
st.subheader("Statistik Rata - Rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
avg_weather = bike_df.groupby('weather_label')['cnt_hour'].mean().reset_index().sort_values("cnt_hour")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='weather_label', y='cnt_hour', data=avg_weather, hue='weather_label', palette='magma', legend=False)
ax.set_title('Rata - Rata Sewa Sepeda berdasarkan Kondisi Cuaca')
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Rata - Rata Sewa')
plt.tight_layout()
st.pyplot(fig)
with st.expander('Keterangan'):
    st.write(
        """
        Rata rata sewa sepeda paling banyak terjadi pada kondisi cuaca jernih mencapai angka 4500 lebih. 
        Namun rata rata sewa sepeda paling sedikit terjadi yakni saat kondisi cuaca hujan ringan hanya mencapai angka 2000 saja. 
        Dari visualisasi data diatas terlihat bahwa kondisi cuaca sangat berpengaruh terhadap jumlah rata rata penyewaan sepeda.
        """
    )