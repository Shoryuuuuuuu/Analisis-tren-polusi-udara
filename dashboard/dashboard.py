import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
# Load dataset yang sudah di-merge
file_path = "dashboard/Merged_PRSA_Data.csv"
df = pd.read_csv(file_path)

# Konversi kolom tanggal menjadi datetime
columns_datetime = ["year", "month", "day", "hour"]
df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])

# Drop kolom yang tidak diperlukan
df.drop(columns=columns_datetime, inplace=True)

# Sidebar untuk filter tanggal
st.sidebar.header("Filter Data")
start_date, end_date = st.sidebar.date_input("Pilih Rentang Waktu", [df['datetime'].min(), df['datetime'].max()])

df_filtered = df[(df['datetime'] >= str(start_date)) & (df['datetime'] <= str(end_date))]

# Analisis Tren PM2.5
st.header("Dashboard Analisis Kualitas Udara")
st.subheader("Tren PM2.5 di 4 Stasiun (2014-2017)")

# Ambil rata-rata PM2.5 per tahun untuk setiap stasiun
stations = ["Aotizhongxin", "Changping", "Dingling", "Dongsi"]
df_filtered['year'] = df_filtered['datetime'].dt.year
avg_pm25_per_year = df_filtered.groupby(['year', 'station'])['PM2.5'].mean().unstack()

fig, ax = plt.subplots(figsize=(10, 5))
for station in stations:
    ax.plot(avg_pm25_per_year.index, avg_pm25_per_year[station], marker='o', label=station)
ax.set_xlabel("Tahun")
ax.set_ylabel("Rata-rata PM2.5")
ax.set_title("Tren PM2.5 di 4 Stasiun (2014-2017)")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Analisis Pengaruh Cuaca
st.subheader("Korelasi PM2.5 dengan Faktor Cuaca")
corr_matrix = df_filtered[['PM2.5', 'TEMP', 'PRES', 'WSPM']].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt='.2f', ax=ax)
st.pyplot(fig)

# Kesimpulan
st.subheader("Kesimpulan")
st.write("- **Tren PM2.5**: Terjadi fluktuasi polusi udara sepanjang waktu.")
st.write("- **Pengaruh Faktor Cuaca**:")
st.write("  - **Suhu (TEMP)** memiliki korelasi negatif dengan PM2.5, artinya saat suhu meningkat, polusi udara cenderung menurun.")
st.write("  - **Tekanan Udara (PRES)** menunjukkan korelasi positif, yang berarti bahwa ketika tekanan meningkat, PM2.5 juga meningkat.")
st.write("  - **Kecepatan Angin (WSPM)** berkorelasi negatif dengan PM2.5, menunjukkan bahwa angin membantu menyebarkan polutan dan mengurangi konsentrasi PM2.5.")

st.caption("Dashboard ini dibuat untuk analisis kualitas udara berdasarkan data pemantauan.")
