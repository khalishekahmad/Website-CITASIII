import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk


# Inisialisasi session_state
if 'loggedin' not in st.session_state:
    st.session_state.loggedin = False

st.set_page_config(page_title="Website CITASI", page_icon="https://raw.githubusercontent.com/khalishekahmad/test1/main/Logo%20Web%20Citasi.png", layout="centered")

def main():
    if st.session_state.loggedin:
        dashboard_page()
    else:
        login_page()

def login_page():
    st.title("LOGIN")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("https://raw.githubusercontent.com/khalishekahmad/test1/main/Logo%20Web%20Citasi.png", width=200)
        st.text("CITASI\nCitarum Quality\nWater Classification")
    
    with col2:
        email = st.text_input("Email")
        password = st.text_input("Password", type='password')
        
        if st.button("Lanjut"):
            if email and password:  # Tambahkan logika otentikasi Anda di sini
                st.success(f"Selamat datang, {email}!")
                st.session_state.loggedin = True
                st.rerun()
            else:
                st.warning("Harap isi kolomnya!.")
                
        if not email and not password:
            signup_text = "Belum Punya Akun? Sign-Up"
            if st.button(signup_text):
                # Anda dapat mengarahkan pengguna ke halaman pendaftaran atau menampilkan formulir pendaftaran di sini
                pass

def dashboard_page():
    st.title("Dashboard Page")
    # Tambahkan elemen dashboard di sini
    df = pd.DataFrame({
        'lat': [-6.9175],  # Koordinat latitude Bandung
        'lon': [107.6191]  # Koordinat longitude Bandung
    })

    # Menggunakan PyDeck untuk mengubah warna peta dan menambahkan label
    view_state = pdk.ViewState(
        latitude=df['lat'].mean(),
        longitude=df['lon'].mean(),
        zoom=10,
        pitch=0)

    # Membuat layer peta
    layer = pdk.Layer(
        'ScatterplotLayer',
        df,
        get_position='[lon, lat]',
        get_fill_color='[200, 30, 0, 160]',
        get_radius=200,
    )

    # Menampilkan peta dengan layer yang telah dibuat
    r = pdk.Deck(layers=[layer], initial_view_state=view_state,
                 map_style='mapbox://styles/mapbox/light-v9')
    st.pydeck_chart(r)

    st.map(df)

if __name__ == "__main__":
    main()

