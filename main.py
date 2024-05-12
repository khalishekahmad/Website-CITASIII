import streamlit as st
from streamlit_option_menu import option_menu

import account, kalkulator, metode, penjelasan

st.set_page_config(
    page_title="Citasi",
    page_icon="https://github.com/ardhien50/Website-Citasi_coba/blob/main/WebsiteCitasi/Gambar/Logo%20Web%20Citasi.png?raw=true",  # Ganti dengan URL logo Anda
    layout="centered"  # Layout halaman
)

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    @staticmethod
    def run():
        with st.sidebar:        
            app = option_menu(
                menu_title='Citasi',
                options=['Account', 'Kalkulator', 'Metode', 'Penjelasan'],
                icons=['person-circle', 'calculator', 'globe', 'info-circle'],
                menu_icon='water',  # Ubah dengan ikon yang sesuai dari FontAwesome
                default_index=1,
                styles={
                    "container": {"padding": "5!important", "background-color": 'grey'},
                    "icon": {"color": "white", "font-size": "23px"}, 
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "black"},
                    "nav-link-selected": {"background-color": "black"}
                }
            )

        if app == "Account":
            account.app()
        if app == "Kalkulator":
            kalkulator.app()
        if app == "Metode":
            metode.app()
        if app == "Penjelasan":
            penjelasan.app()

# Instansiasi MultiApp
multi_app = MultiApp()

# Tambahkan aplikasi ke MultiApp
multi_app.add_app("Account", account.app)
multi_app.add_app("Kalkulator", kalkulator.app)
multi_app.add_app("Metode", metode.app)
multi_app.add_app("Penjelasan", penjelasan.app)

# Jalankan aplikasi
multi_app.run()
