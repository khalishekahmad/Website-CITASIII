from asyncio import run
import streamlit as st
from streamlit_option_menu import option_menu

import account,kalkulator,metode,penjelasan
st.set_page_config(
        page_title="Citasi",
        page_icon="https://github.com/ardhien50/Website-Citasi_coba/blob/main/WebsiteCitasi/Gambar/Logo%20Web%20Citasi.png?raw=true",  # Ganti dengan URL logo Anda
        layout="centered"  # Layout halaman
)

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self,title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        with st.sidebar:        
            app = option_menu(
                menu_title='Citasi ',
                options=['Account','Kalkulator','Metode','Penjelasan'],
                icons=['person-circle','chat-text-fill','house-fill','info-circle-fill'],
                menu_icon='chat-text-fill',
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'grey'},
        "icon": {"color": "white", "font-size": "23px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "black"},
        "nav-link-selected": {"background-color": "black"},}
                
                )

        if app == "Account":
            account.app()
        if app == "Kalkulator":
            kalkulator.app()
        if app == "Metode":
            metode.app()
        if app == "Penjelasan":
            penjelasan.app()

    run()