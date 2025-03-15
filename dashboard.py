import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime

st.title('Dashboard Analysis Bike Sharing')
    
all_df = pd.read_csv("merged_df.csv")
all_df['dteday'] = pd.to_datetime(all_df['dteday'])

all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True, drop=True)

min_date = all_df['dteday'].min().date()
max_date = all_df['dteday'].max().date()

def create_sum_sharing_hr(df):
    # Hitung total penyewaan
    total_sharing = df['cnt_x'].sum()
    return total_sharing

def create_sum_casual_hr(df):
    # Hitung total penyewaan casual
    total_casual = df['casual_x'].sum()
    return total_casual

def create_daily_rides_day(df):
    # Hitung total penyewaan by status
    daily_rides = df.groupby(by='dteday').agg({
    'casual_y': 'sum',
    'registered_y': 'sum'
    })
    daily_rides = daily_rides.reset_index()
    daily_rides.rename(columns={
    'casual_y': 'Tidak Terdaftar',
    'registered_y': 'Terdaftar'
    }, inplace=True)
    
    return daily_rides
    
def create_sum_byseason_day(df):
    # Hitung total penyewaan by season
    sum_byseason = df.groupby(by='season_y').agg({
        'cnt_y': 'mean'
    })
    sum_byseason = sum_byseason.reset_index()
    
    # Memetakan nilai numerik season ke nama season
    season_names = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
    sum_byseason['season_name'] = sum_byseason['season_y'].map(season_names)
    
    return sum_byseason

def create_persebaran_cust(df):
    # Hitung persebaran penyewaan by customer type
    casual_cnt = df['casual_y'].sum()
    registered_cnt = df['registered_y'].sum()
    
    combine = [casual_cnt,registered_cnt]
    
    return combine

def create_persebaran_byweathersit(df):
    # Hitung persebaran penyewaan by weather
    weather_cnt = df.groupby(by='weathersit_x').agg({
        'cnt_x': 'mean'
        
    })
    weather_cnt = weather_cnt.reset_index()
    
    weather_names = {1: 'Cerah', 2: 'Berawan', 3: 'Hujan Ringan', 4: 'Hujan Deras'}
    weather_cnt['weather_name'] = weather_cnt['weathersit_x'].map(weather_names)
    
    return weather_cnt

def create_hourbusy_hr(df):
    # Hitung total penyewaan by hour
    hourbusy = df.groupby(by='hr').agg({
        'cnt_x': 'mean'
    })
    hourbusy = hourbusy.reset_index()
    
    return hourbusy

with st.sidebar:
    st.image('bike.png')
    
    # Perbaikan pada date_input
    start_date = st.date_input(
        label='Tanggal Awal',
        value=min_date,
        min_value=min_date,
        max_value=max_date
    )
    
    end_date = st.date_input(
        label='Tanggal Akhir',
        value=max_date,
        min_value=start_date,
        max_value=max_date
    )

# Konversi tanggal ke string format YYYY-MM-DD
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

# Filter data
main_df = all_df[(all_df["dteday"].dt.strftime('%Y-%m-%d') >= start_date_str) & 
                (all_df["dteday"].dt.strftime('%Y-%m-%d') <= end_date_str)]


# Mengaplikasikan Fungsi
sum_sharing_hr_df = create_sum_sharing_hr(main_df)
sum_casual_hr_df = create_sum_casual_hr(main_df)
daily_rides_df = create_daily_rides_day(main_df)
sum_byseason_df = create_sum_byseason_day(main_df)
perbandingan_customer_df = create_persebaran_cust(main_df)
perbandingan_weathersit_df = create_persebaran_byweathersit(main_df)
perbandingan_hour_df = create_hourbusy_hr(main_df)

st.subheader('Jumlah Penyewa')

col1, col2 = st.columns(2)
 
with col1:
    total_sharing = sum_sharing_hr_df
    st.metric("Total Sharing", value= total_sharing)
    
with col2:
    total_casual = sum_casual_hr_df
    st.metric("Jumlah Pelanggan tidak Terdaftar", value= total_casual)
    
# Visualisasi Line Chart
st.subheader('Tren Penggunaan Sepeda Berdasarkan Tipe Pelanggan')

fig, ax = plt.subplots(figsize=(16, 8))

# Plot data
ax.plot(
    daily_rides_df["dteday"],
    daily_rides_df["Tidak Terdaftar"],
    label="Penyewa Tidak Terdaftar",
    linewidth=2,
    marker='o',
    markersize=4
)
ax.plot(
    daily_rides_df["dteday"],
    daily_rides_df["Terdaftar"],
    label="Penyewa Terdaftar",
    linewidth=2,
    marker='o',
    markersize=4
)

# Mempercantik plot
ax.set_xlabel('Tanggal', fontsize=14)
ax.set_ylabel('Jumlah Penyewa', fontsize=14)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=10, rotation=45)
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend(fontsize=12)

plt.title('Perbandingan Jumlah Penyewa Terdaftar dan Tidak Terdaftar', fontsize=16)

# Menyesuaikan layout
plt.tight_layout()

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Visualisasi Bar Chart untuk Season
st.subheader('Rata - Rata Penyewa Berdasarkan Musim (Harian)')

# Menggunakan matplotlib untuk bar chart
fig, ax= plt.subplots(figsize=(12, 6))

# Membuat bar chart
bars = ax.bar(
    sum_byseason_df['season_name'], 
    sum_byseason_df['cnt_y'],
    color='skyblue',
    edgecolor='navy'
)

# Menambahkan label pada setiap bar
for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width()/2., 
        height + 5,
        f'{int(height):,}',
        ha='center', 
        va='bottom',
        fontsize=10
    )

# Mempercantik plot
ax.set_xlabel('Musim', fontsize=14)
ax.set_ylabel('Jumlah Penyewa', fontsize=14)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
ax.grid(True, axis='y', linestyle='--', alpha=0.7)

plt.title('Rata - Rata Penyewa Berdasarkan Musim', fontsize=16)
plt.tight_layout()

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Visualisasi Pie Chart
st.subheader('Perbandingan Jumlah Penyewa Berdasarkan Jenis Penyewa')

fig, ax = plt.subplots()
ax.pie(
    perbandingan_customer_df, 
    labels=['casual','registered'], 
    autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100.*(sum(perbandingan_customer_df)))})', 
    colors=sns.color_palette("pastel"),
    startangle=90
)
ax.axis("equal")  # Agar pie chart berbentuk lingkaran sempurna
plt.title('Distribusi Pelanggan berdasarkan Type Pelanggan')
# Tampilkan di Streamlit
st.pyplot(fig)

# Visualisasi Bar Chart
st.subheader('Perbandingan Penyewa Berdasarkan Cuaca (Jam)')

fig, ax= plt.subplots(figsize=(12, 6))

# Membuat bar chart
bars = ax.bar(
    perbandingan_weathersit_df['weather_name'], 
    perbandingan_weathersit_df['cnt_x'],
    color='skyblue',
    edgecolor='navy'
)

# Menambahkan label pada setiap bar
for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width()/2., 
        height + 5,
        f'{int(height):,}',
        ha='center', 
        va='bottom',
        fontsize=10
    )

# Mempercantik plot
ax.set_xlabel('Cuaca', fontsize=14)
ax.set_ylabel('Jumlah Penyewa', fontsize=14)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
ax.grid(True, axis='y', linestyle='--', alpha=0.7)

plt.title('Rata - Rata Penyewa Berdasarkan Cuaca', fontsize=16)
plt.tight_layout()

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Line Chart Ramai Penyewa berdasarkan Jam
st.subheader('Grafik Penyewa Berdasarkan Jam')
# Membuat bar chart
fig, ax = plt.subplots(figsize=(12, 6))

# Plot data
ax.plot(
    perbandingan_hour_df["hr"],
    perbandingan_hour_df["cnt_x"],
    label="Jam",
    linewidth=2,
    marker='o',
    markersize=4
)

# Mempercantik plot
ax.set_xlabel('Jam', fontsize=14)
ax.set_ylabel('Jumlah Penyewa', fontsize=14)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=10, rotation=45)
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend(fontsize=12)

plt.title('Grafik Penyewa Berdasarkan Jam', fontsize=16)

# Menyesuaikan layout
plt.tight_layout()

# Menampilkan plot di Streamlit
st.pyplot(fig)
