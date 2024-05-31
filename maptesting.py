import streamlit as st
import folium
from streamlit_folium import folium_static

# Judul aplikasi
st.title('Visualisasi Sungai Citarum')

# Data koordinat Sungai Citarum (ini adalah contoh, Anda perlu koordinat yang lebih tepat dan detail)
citarum_coordinates = [
    [-6.900292, 107.618601],
    [-6.899883, 107.618671],
    [-6.899469, 107.618773],
    [-6.899123, 107.618825],
    [-6.898742, 107.618862],
    # Tambahkan koordinat lainnya sesuai kebutuhan
]

# Membuat peta Folium
m = folium.Map(location=[-6.900292, 107.618601], zoom_start=14)  # Sesuaikan lokasi dan zoom awal

# Menambahkan polyline untuk Sungai Citarum
folium.PolyLine(
    citarum_coordinates,
    color='blue',  # Warna garis
    weight=5  # Ketebalan garis
).add_to(m)

# Menampilkan peta di Streamlit
folium_static(m)
