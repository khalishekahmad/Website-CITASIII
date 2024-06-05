import streamlit as st
import pandas as pd
import numpy as np
import joblib
import folium
from tensorflow.keras.models import load_model
from streamlit_folium import folium_static
import json

# Fungsi untuk klasifikasi Weighted KNN dan Gaussian Naive Bayes
def predict_quality_general(model, scaler, BOD, COD, FecalColiform, IP):
    input_data = pd.DataFrame([[BOD, COD, FecalColiform, IP]], columns=['BOD', 'COD', 'FecalColiform', 'IP'])
    input_data = scaler.transform(input_data)
    prediction = model.predict(input_data)[0]
    
    class_labels = {
        1: "Tidak tercemar/memenuhi baku mutu",
        2: "Tercemar ringan",
        3: "Tercemar sedang",
        4: "Tercemar berat"
    }
    
    return class_labels.get(prediction, 'kelas tidak dikenal')

# Fungsi untuk klasifikasi ANN
def predict_quality_ann(model, scaler, BOD, COD, FecalColiform, IP):
    input_data = pd.DataFrame([[BOD, COD, FecalColiform, IP]], columns=['BOD', 'COD', 'FecalColiform', 'IP'])
    input_data = scaler.transform(input_data)
    prediction = model.predict(input_data)
    
    if prediction.ndim > 1:
        prediction = prediction[0]  
    prediction = np.argmax(prediction) + 1  

    class_labels = {
        1: "Tidak tercemar/memenuhi baku mutu",
        2: "Tercemar ringan",
        3: "Tercemar sedang",
        4: "Tercemar berat"
    }
    
    return class_labels.get(prediction, 'kelas tidak dikenal')

# Memuat data GeoJSON
def load_geojson(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read().split('=')[1].strip().rstrip(';')
        return json.loads(file_content)

geojson_data_sungai = load_geojson('Sungai Citarum.js')
geojson_data_batas = load_geojson('Batas_DAS.js')
geojson_data_waduk = load_geojson('Waduk.js')

def app():
    # Memuat data titik-titik sungai dari file CSV
    file_path_points = 'filtered_citarum_points.csv'
    points_data = pd.read_csv(file_path_points)

    # Menambahkan judul aplikasi
    st.title('Peta Interaktif Sungai Citarum')

    # Pilihan metode machine learning
    st.header("Pilih Model Machine Learning")
    ml_choice = st.selectbox('Silakan pilih model Machine Learning untuk melihat tampilan peta titik-titik sungai atau tampilkan peta awal', 
                            ['Tampilan Awal Peta', 'Weighted KNN', 'Artificial Neural Network', 'Gaussian Naive Bayes'])

    # Menampilkan informasi kotak di atas peta dalam dua kolom
    st.header('Informasi Warna Pada Peta')
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Status Kualitas Air Sungai")
        boxes_info = [
            {"title": "Memenuhi Baku Mutu", "color": "#6DC5D1", "width": "200px", "height": "50px"},
            {"title": "Tercemar Ringan", "color": "#7ABA78", "width": "200px", "height": "50px"},
            {"title": "Tercemar Sedang", "color": "#FEB941", "width": "200px", "height": "50px"},
            {"title": "Tercemar Berat", "color": "#C40C0C", "width": "200px", "height": "50px"}
        ]

        for box in boxes_info:
            st.markdown(
                f"""
                <div style="background-color: {box['color']}; width: {box['width']}; height: {box['height']}; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; margin-bottom: 10px;">
                    {box['title']}
                </div>
                """,
                unsafe_allow_html=True
            )

    with col2:
        st.subheader("Legenda (Keterangan)")
        legend_items = [
            {"title": "Aliran Sungai", "color": "blue", "width": "200px", "height": "20px"},
            {"title": "Batas DAS", "color": "pink", "width": "200px", "height": "20px"}
        ]

        for item in legend_items:
            st.markdown(
                f"""
                <div style="background-color: {item['color']}; width: {item['width']}; height: {item['height']}; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; margin-bottom: 10px;">
                    {item['title']}
                </div>
                """,
                unsafe_allow_html=True
            )

    # Membuat peta awal
    m = folium.Map(location=[-6.9, 107.6], zoom_start=10, tiles='OpenStreetMap', width='100%', height='600px')

    # Menambahkan data GeoJSON ke peta
    geojson_sungai = folium.GeoJson(geojson_data_sungai, name="Sungai Citarum", style_function=lambda feature: {
        'color': 'blue', 'weight': 5
    })

    geojson_batas = folium.GeoJson(geojson_data_batas, name="Batas DAS", style_function=lambda feature: {
        'fillColor': 'pink', 'color': 'pink', 'weight': 2, 'fillOpacity': 0.55
    })

    geojson_waduk = folium.GeoJson(geojson_data_waduk, name="Waduk", style_function=lambda feature: {
        'color': 'blue', 'weight': 5
    })

    # Menambahkan titik-titik sungai dari file CSV ke peta
    if ml_choice == 'Tampilan Awal Peta':
        for _, row in points_data.iterrows():
            folium.Marker(location=[row['latitude'], row['longitude']], popup=row['name'], 
                        icon=folium.Icon(color='blue', icon='tint', prefix='fa')).add_to(m)

        geojson_sungai.add_to(m)
        geojson_batas.add_to(m)
        geojson_waduk.add_to(m)

        # Menambahkan kontrol lapisan
        folium.LayerControl().add_to(m)

        # Menampilkan peta awal di Streamlit
        folium_static(m, width=777, height=590)

    # Memuat model dan scaler berdasarkan pilihan
    else:
        model, scaler = None, None

        if ml_choice == 'Weighted KNN':
            st.write("Hasil akurasi model KNN dengan Euclidean Distance dan SMOTE-ADASYN adalah 94,7%")
            model_path = 'model_knn_euclidean.pkl'
            scaler_path = 'scaler_knn_euclidean.pkl'
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
        elif ml_choice == 'Artificial Neural Network':
            st.write("Hasil akurasi model Artificial Neural Network dan SMOTE-ADASYN adalah 91,8%")
            model_path = 'model_ann.h5'
            scaler_path = 'scaler_ann.pkl'
            try:
                model = load_model(model_path)
            except Exception as e:
                st.write(f"Kesalahan saat memuat model: {e}")
            scaler = joblib.load(scaler_path) if model else None
        elif ml_choice == 'Gaussian Naive Bayes':
            st.write("Hasil akurasi model Gaussian Naive Bayes dan SMOTE-ADASYN adalah 95,2%")
            model_path = 'model_gnb.pkl'
            scaler_path = 'scaler_gnb.pkl'
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)

        # Memastikan model berhasil dimuat sebelum melanjutkan
        if model and scaler:
            file_path_points = 'Dataset_titik_sungai.csv'
            points_data = pd.read_csv(file_path_points)
        
            if ml_choice == 'Artificial Neural Network':
                points_data['Status'] = points_data.apply(lambda row: predict_quality_ann(model, scaler, row['BOD'], row['COD'], row['FecalColiform'], row['IP']), axis=1)
            else:
                points_data['Status'] = points_data.apply(lambda row: predict_quality_general(model, scaler, row['BOD'], row['COD'], row['FecalColiform'], row['IP']), axis=1)

            # Menentukan warna berdasarkan status
            def get_color(status):
                if status == "Tidak tercemar/memenuhi baku mutu":
                    return "#6DC5D1"
                elif status == "Tercemar ringan":
                    return "#7ABA78"
                elif status == "Tercemar sedang":
                    return "#FEB941"
                elif status == "Tercemar berat":
                    return "#C40C0C"
                else:
                    return "gray"

            # Membuat peta tanpa OpenStreetMap, hanya batas DAS, aliran sungai, waduk, dan titik-titik sungai
            m = folium.Map(location=[-6.9, 107.6], zoom_start=10, width='100%', height='600px')

            # Menambahkan data GeoJSON ke peta tanpa opsi lapisan
            folium.GeoJson(geojson_data_batas, name="Batas DAS", style_function=lambda feature: {
                'fillColor': 'pink', 'color': 'pink', 'weight': 2, 'fillOpacity': 0.55
            }).add_to(m)

            folium.GeoJson(geojson_data_sungai, name="Sungai Citarum", style_function=lambda feature: {
                'color': 'blue', 'weight': 5
            }).add_to(m)

            folium.GeoJson(geojson_data_waduk, name="Waduk", style_function=lambda feature: {
                'color': 'blue', 'weight': 5
            }).add_to(m)

            # Menambahkan titik-titik sungai yang telah diprediksi ke peta dengan warna yang sesuai
            for _, row in points_data.iterrows():
                color = get_color(row['Status'])
                popup_content = f"""
                <b>Status:</b> {row['Status']}<br>
                <b>Nama:</b> {row['Titik Sungai']}<br>
                <b>Alamat:</b> {row['Alamat']}
                """
                folium.CircleMarker(
                    location=[row['Latitude'], row['Longitude']],
                    radius=8,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=1,
                    popup=popup_content
                ).add_to(m)

            # Menampilkan peta dengan prediksi di Streamlit
            folium_static(m, width=777, height=590)

app()