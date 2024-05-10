import folium
import streamlit as st
from streamlit_folium import st_folium

def app():
    st.write('Metode')
    st.title('Titik Peta Sungai :blue[Citarum]')

    choice = st.selectbox('Silahakan pilih metode Machine Learning untuk melihat hasil yang berbeda', ['KNN with Euclidean Distance','Artificial Neural Network', 'Gaussian Naive Bayes'])
    
    if choice == ('KNN with Euclidean Distance'):
        st.subheader('KNN with Euclidean Distance')
        # Create a base map centered on the Citarum River
        m = folium.Map(location=[-6.8650, 107.4912], zoom_start=10)

        # Updated markers along the Citarum River with more accurate coordinates
        locations = {
        "Titik Sungai: Situ Cisanti<br>Alamat: Neglawangi, Kertasari,<br>Bandung Regency, West Java 40386": [-7.208484677933202, 107.65792566573455],  # Source of the Citarum River
        "Titik Sungai: Bendungan Saguling<br>Alamat: Saguling, Batujajar,<br>West Bandung Regency, West Java ": [-6.913526, 107.367661], # Saguling Dam
        "Titik Sungai: Bendungan Cirata<br>Alamat: Citamiang, Maniis,<br>Purwakarta Regency, West Java 41166": [-6.700203, 107.364963], # Cirata Dam
        "Titik Sungai: Bendungan Jatiluhur<br>Alamat: Kutamanah, Sukasari,<br>Purwakarta Regency, West Java 41116": [-6.526997, 107.385456], # Jatiluhur Dam
        "Titik Sungai: Kabupaten Karawang<br>Alamat: Sungai Citarum, Telukjambe Timur,<br>Karawang, West Java 41361": [-6.298185, 107.287757],  # Karawang Regency
        "Titik Sungai: Muara Gembong<br>Alamat: Kecamatan Muara Gembong,<br>Bekasi Regency, West Java": [-5.984462, 107.043829], # Bekasi
        "Titik Sungai: Sungai Cikapundung<br>Alamat: Bandung City, West Java": [-6.898969, 107.606402],  # Bandung City
        "Titik Sungai: Dayeuhkolot<br>Alamat: Dayeuhkolot, Bandung, West Java": [-6.990974, 107.626285],  # Dayeuhkolot
    }

        # Loop through the locations dictionary and add each marker to the map
        for place, coord in locations.items():
            folium.Marker(
            location=coord,
            popup=folium.Popup(place, max_width=300),  # Use folium.Popup to control the width of the popup
            tooltip=place.replace('<br>', '\n')  # Replace <br> with \n for the tooltip
        ).add_to(m)

        # Render the Folium map in Streamlit with adjusted width and height
        st_folium(m, width=600, height=500)  # Adjust the width to 1000 pixels and height to 600 pixels

    elif choice == ('Artificial Neural Network'):
        st.subheader('Artificial Neural Network')
        # Create a base map centered on the Citarum River
        m = folium.Map(location=[-6.8650, 107.4912], zoom_start=10)

        # Updated markers along the Citarum River with more accurate coordinates
        locations = {
        "Titik Sungai: Situ Cisanti<br>Alamat: Neglawangi, Kertasari,<br>Bandung Regency, West Java 40386": [-7.208484677933202, 107.65792566573455],  # Source of the Citarum River
        "Titik Sungai: Bendungan Saguling<br>Alamat: Saguling, Batujajar,<br>West Bandung Regency, West Java ": [-6.913526, 107.367661], # Saguling Dam
        "Titik Sungai: Bendungan Cirata<br>Alamat: Citamiang, Maniis,<br>Purwakarta Regency, West Java 41166": [-6.700203, 107.364963], # Cirata Dam
        "Titik Sungai: Bendungan Jatiluhur<br>Alamat: Kutamanah, Sukasari,<br>Purwakarta Regency, West Java 41116": [-6.526997, 107.385456], # Jatiluhur Dam
        "Titik Sungai: Kabupaten Karawang<br>Alamat: Sungai Citarum, Telukjambe Timur,<br>Karawang, West Java 41361": [-6.298185, 107.287757],  # Karawang Regency
        "Titik Sungai: Muara Gembong<br>Alamat: Kecamatan Muara Gembong,<br>Bekasi Regency, West Java": [-5.984462, 107.043829], # Bekasi
        "Titik Sungai: Sungai Cikapundung<br>Alamat: Bandung City, West Java": [-6.898969, 107.606402],  # Bandung City
        "Titik Sungai: Dayeuhkolot<br>Alamat: Dayeuhkolot, Bandung, West Java": [-6.990974, 107.626285],  # Dayeuhkolot
    }

        # Loop through the locations dictionary and add each marker to the map
        for place, coord in locations.items():
            folium.Marker(
            location=coord,
            popup=folium.Popup(place, max_width=300),  # Use folium.Popup to control the width of the popup
            tooltip=place.replace('<br>', '\n')  # Replace <br> with \n for the tooltip
        ).add_to(m)

        # Render the Folium map in Streamlit with adjusted width and height
        st_folium(m, width=600, height=500)  # Adjust the width to 1000 pixels and height to 600 pixels

    elif choice == ('Gaussian Naive Bayes'):
        st.subheader('Gaussian Naive Bayes')
        # Create a base map centered on the Citarum River
        m = folium.Map(location=[-6.8650, 107.4912], zoom_start=10)

        # Updated markers along the Citarum River with more accurate coordinates
        locations = {
        "Titik Sungai: Situ Cisanti<br>Alamat: Neglawangi, Kertasari,<br>Bandung Regency, West Java 40386": [-7.208484677933202, 107.65792566573455],  # Source of the Citarum River
        "Titik Sungai: Bendungan Saguling<br>Alamat: Saguling, Batujajar,<br>West Bandung Regency, West Java ": [-6.913526, 107.367661], # Saguling Dam
        "Titik Sungai: Bendungan Cirata<br>Alamat: Citamiang, Maniis,<br>Purwakarta Regency, West Java 41166": [-6.700203, 107.364963], # Cirata Dam
        "Titik Sungai: Bendungan Jatiluhur<br>Alamat: Kutamanah, Sukasari,<br>Purwakarta Regency, West Java 41116": [-6.526997, 107.385456], # Jatiluhur Dam
        "Titik Sungai: Kabupaten Karawang<br>Alamat: Sungai Citarum, Telukjambe Timur,<br>Karawang, West Java 41361": [-6.298185, 107.287757],  # Karawang Regency
        "Titik Sungai: Muara Gembong<br>Alamat: Kecamatan Muara Gembong,<br>Bekasi Regency, West Java": [-5.984462, 107.043829], # Bekasi
        "Titik Sungai: Sungai Cikapundung<br>Alamat: Bandung City, West Java": [-6.898969, 107.606402],  # Bandung City
        "Titik Sungai: Dayeuhkolot<br>Alamat: Dayeuhkolot, Bandung, West Java": [-6.990974, 107.626285],  # Dayeuhkolot
    }

        # Loop through the locations dictionary and add each marker to the map
        for place, coord in locations.items():
            folium.Marker(
            location=coord,
            popup=folium.Popup(place, max_width=300),  # Use folium.Popup to control the width of the popup
            tooltip=place.replace('<br>', '\n')  # Replace <br> with \n for the tooltip
        ).add_to(m)

        # Render the Folium map in Streamlit with adjusted width and height
        st_folium(m, width=600, height=500)  # Adjust the width to 1000 pixels and height to 600 pixels