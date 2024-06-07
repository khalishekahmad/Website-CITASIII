import streamlit as st
import pandas as pd
import numpy as np
import joblib
import base64
import plotly.express as px
from tensorflow.keras.models import load_model

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
    
    colors = {
        1: "#6DC5D1",
        2: "#7ABA78",
        3: "#FEB941",
        4: "#C40C0C"
    }
    
    return prediction, f"Kualitas air Sungai Citarum: {class_labels.get(prediction, 'kelas tidak dikenal')} (Class {prediction})", colors.get(prediction, "#FFFFFF")

# Fungsi untuk klasifikasi ANN
def predict_quality_ann(model, scaler, BOD, COD, FecalColiform, IP):
    input_data = pd.DataFrame([[BOD, COD, FecalColiform, IP]], columns=['BOD', 'COD', 'FecalColiform', 'IP'])
    input_data = scaler.transform(input_data)
    prediction = model.predict(input_data)
    
    # Pastikan prediksi adalah scalar
    if prediction.ndim > 1:
        prediction = prediction[0]  # Ambil elemen pertama jika prediksi adalah array 2D
    prediction = np.argmax(prediction) + 1  # Ambil kelas dengan probabilitas tertinggi (1-based index)

    class_labels = {
        1: "Tidak tercemar/memenuhi baku mutu",
        2: "Tercemar ringan",
        3: "Tercemar sedang",
        4: "Tercemar berat"
    }
    
    colors = {
        1: "#6DC5D1",
        2: "#7ABA78",
        3: "#FEB941",
        4: "#C40C0C"
    }
    
    return prediction, f"Kualitas air Sungai Citarum: {class_labels.get(prediction, 'kelas tidak dikenal')} (Class {prediction})", colors.get(prediction, "#FFFFFF")

def app():
    # Judul aplikasi
    st.title('Kalkulator Klasifikasi Kualitas Air Sungai Citarum')

    # Membuat modal pop-up
    modal = Modal("📘Manual Book CITASI untuk User📘", key="modal")

    # Tampilkan tombol untuk membuka modal
    if st.button("Buka Panduan Pengguna"):
    modal.open()

    # Tampilkan modal jika dibuka
    if modal.is_open():
    with modal.container():
        st.write("👇 Silakan lihat Panduan Pengguna untuk Website Citasi di buku manual ini yes! 👇")
        st.markdown("[Klik ini dan lihat isinya! 😁](https://drive.google.com/file/d/11VKolylps1qELb8sqVaN6zu5S8z0--F_/view?usp=sharing)", unsafe_allow_html=True)

    # Pilihan metode machine learning
    ml_choice = st.selectbox('Silakan pilih metode Machine Learning untuk melihat hasil yang berbeda', ['Weighted KNN', 'Artificial Neural Network', 'Gaussian Naive Bayes'])

    # Memuat model dan scaler berdasarkan pilihan
    model, scaler, evaluation_image = None, None, None

    if ml_choice == 'Weighted KNN':
        model_path = 'model_knn_euclidean.pkl'
        scaler_path = 'scaler_knn_euclidean.pkl'
        evaluation_image = 'https://github.com/khalishekahmad/test1/blob/ba5b64fdc67c6c2962dbc1e8f948e6ed3f3a6e19/Overall%20Classification%20Report%20Metrics%20-%20KNN%20dengan%20Euclidean%20Distance%20dan%20SMOTE-ADASYN.png?raw=true'
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
    elif ml_choice == 'Artificial Neural Network':
        model_path = 'model_ann.h5'
        scaler_path = 'scaler_ann.pkl'
        evaluation_image = 'https://github.com/khalishekahmad/test1/blob/7f79c4b18a0f858fb8130c4a471b580bbcf26bdb/Overall%20Classification%20Report%20Metrics%20-%20Artificial%20Neural%20Network%20dan%20SMOTE-ADASYN.png?raw=true'
        try:
            model = load_model(model_path)
        except Exception as e:
            st.write(f"Kesalahan saat memuat model: {e}")
        scaler = joblib.load(scaler_path) if model else None
    elif ml_choice == 'Gaussian Naive Bayes':
        model_path = 'model_gnb.pkl'
        scaler_path = 'scaler_gnb.pkl'
        evaluation_image = 'https://github.com/khalishekahmad/test1/blob/7f79c4b18a0f858fb8130c4a471b580bbcf26bdb/Overall%20Classification%20Report%20Metrics%20-%20Gaussian%20Naive%20Bayes%20dan%20SMOTE-ADASYN.png?raw=true'
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)

    # Pastikan model berhasil dimuat sebelum melanjutkan
    if model and scaler:
        # Pilihan metode input data
        choice = st.selectbox('Pilih metode input data', ['Manual', 'Upload File'])

        if choice == 'Manual':
            # Inisialisasi state untuk input
            if 'pH' not in st.session_state:
                st.session_state.pH = ""
            if 'TSS' not in st.session_state:
                st.session_state.TSS = ""
            if 'DO' not in st.session_state:
                st.session_state.DO = ""
            if 'BOD' not in st.session_state:
                st.session_state.BOD = ""
            if 'COD' not in st.session_state:
                st.session_state.COD = ""
            if 'Nitrat' not in st.session_state:
                st.session_state.Nitrat = ""
            if 'FecalColiform' not in st.session_state:
                st.session_state.FecalColiform = ""
            if 'Fosfat' not in st.session_state:
                st.session_state.Fosfat = ""
            if 'IP' not in st.session_state:
                st.session_state.IP = ""

            # Parameter input pengguna dalam tiga kolom
            col1, col2, col3 = st.columns(3)

            with col1:
                st.session_state.pH = st.text_input('Potential of Hydrogen (pH):', value=st.session_state.pH, help="pH (Potential of Hydrogen) adalah ukuran keasaman yang digunakan untuk menyatakan tingkat keasaman atau kebasahan yang dimiliki oleh suatu larutan.", placeholder="6 - 8")
                st.session_state.TSS = st.text_input('Total Suspended Solids (TSS):', value=st.session_state.TSS, help="Total Suspended Solids (TSS) adalah ukuran partikel tergantung dalam air, dalam miligram per liter (mg/L).", placeholder="20 - 36 mg/L")
                st.session_state.DO = st.text_input('Dissolved Oxygen (DO):', value=st.session_state.DO, help="Dissolved Oxygen (DO) adalah ukuran oksigen yang terlarut dalam air, dalam miligram per liter (mg/L).", placeholder="0.00 - 7.79 mg/L")

            with col2:
                st.session_state.BOD = st.text_input('Biochemical Oxygen Demand:', value=st.session_state.BOD, help="Biochemical Oxygen Demand (BOD) adalah jumlah oksigen terlarut yang dibutuhkan oleh organisme biologis aerobik untuk memecah bahan organik yang ada dalam sampel air tertentu pada suhu tertentu selama periode waktu tertentu, dalam miligram per liter (mg/L).", placeholder="1.7 - 6 mg/L")
                st.session_state.COD = st.text_input('Chemical Oxygen Demand:', value=st.session_state.COD, help="Chemical Oxygen Demand (COD) adalah ukuran kapasitas air untuk mengkonsumsi oksigen selama dekomposisi bahan organik dan oksidasi bahan kimia anorganik seperti amonia dan nitrit, dalam miligram per liter (mg/L).", placeholder="10 - 30 mg/L")
                st.session_state.Nitrat = st.text_input('Nitrat:', value=st.session_state.Nitrat, help="Nitrate (NO3) adalah ukuran konsentrasi nitrat dalam air, dalam miligram per liter (mg/L).", placeholder="0 - 4 mg/L")

            with col3:
                st.session_state.FecalColiform = st.text_input('Fecal Coliform:', value=st.session_state.FecalColiform, help="Fecal Coliform adalah sekelompok bakteri yang ditemukan di usus hewan berdarah panas dan digunakan sebagai indikator kontaminasi feses dalam air, dalam jumlah koloni per 100 mililiter (cfu/100 mL).", placeholder="50 - 100 jml/100L")
                st.session_state.Fosfat = st.text_input('Fosfat:', value=st.session_state.Fosfat, help="Phosphate (PO4) adalah ukuran konsentrasi fosfat dalam air, dalam miligram per liter (mg/L).", placeholder="0.03 - 0.1 mg/L")
                st.session_state.IP = st.text_input('Indeks Pencemaran (IP):', value=st.session_state.IP, help="Indeks Pencemaran (IP) adalah ukuran polusi pada sungai.", placeholder="Masukkan nilai/angka IP...")

            # Tombol untuk klasifikasi dan reset
            col1, col2 = st.columns(2)

            with col1:
                if st.button('Klasifikasi'):
                    try:
                        # Konversi input ke float
                        pH = float(st.session_state.pH)
                        TSS = float(st.session_state.TSS)
                        DO = float(st.session_state.DO)
                        BOD = float(st.session_state.BOD)
                        COD = float(st.session_state.COD)
                        Nitrat = float(st.session_state.Nitrat)
                        FecalColiform = float(st.session_state.FecalColiform)
                        Fosfat = float(st.session_state.Fosfat)
                        IP = float(st.session_state.IP)

                        # Periksa nilai negatif
                        if any(val < 0 for val in [pH, TSS, DO, BOD, COD, Nitrat, FecalColiform, Fosfat, IP]):
                            st.write("OOPS! Tidak boleh ada nilai negatif! Pastikan semua nilai sudah benar. (:")
                        else:
                            if ml_choice == 'Artificial Neural Network':
                                prediction, result, color = predict_quality_ann(model, scaler, BOD, COD, FecalColiform, IP)
                            else:
                                prediction, result, color = predict_quality_general(model, scaler, BOD, COD, FecalColiform, IP)
                        
                            st.markdown(f'<div style="background-color:{color};padding:10px;border-radius:5px;">{result}</div>', unsafe_allow_html=True)

                            # Tampilkan tabel rentang nilai parameter indeks pencemaran
                            st.image('https://github.com/khalishekahmad/test1/blob/7f79c4b18a0f858fb8130c4a471b580bbcf26bdb/Tabel%20Rentang%20Nilai%20Parameter%20Indeks%20Pencemaran.png?raw=true', caption='Tabel Rentang Nilai Parameter Indeks Pencemaran untuk Klasifikasi Kualitas Air Sungai Citarum')
                        
                            if ml_choice == 'Weighted KNN':
                                st.image(evaluation_image, caption='Grafik hasil evaluasi model KNN dengan Euclidean Distance')
                                st.write("Gambar di atas menunjukkan hasil metrik untuk klasifikasi kualitas air Sungai Citarum yaitu model KNN yang menggunakan Euclidean Distance dan teknik oversampling SMOTE-ADASYN. Grafik kiri memecah metrik precision, recall, dan f1-score untuk masing-masing dari empat kelas yang dievaluasi.")
                                st.write("- Precision: Metrik ini mengukur ketepatan prediksi positif model. Nilai precision untuk kelas 1, 2, 3, dan 4 masing-masing adalah 95%, 98%, 89%, dan 97%.")
                                st.write("- Recall: Metrik ini mengukur kemampuan model dalam menangkap semua instance positif. Nilai recall untuk kelas 1, 2, 3, dan 4 masing-masing adalah 100%, 83%, 95%, dan 100%.")
                                st.write("- F1 Score: Metrik ini adalah harmonisasi rata-rata dari precision dan recall. Nilai f1-score untuk kelas 1, 2, 3, dan 4 masing-masing adalah 97%, 90%, 92%, dan 98%.")
                                st.write("Grafik kanan menampilkan accuracy keseluruhan model yang mencapai 94,7% menunjukkan bahwa model memiliki tingkat keberhasilan yang tinggi dalam mengklasifikasikan data kualitas air Sungai Citarum.")
                                st.write("Hasil akurasi model KNN dengan Euclidean Distance dan SMOTE-ADASYN adalah 94,7")

                            elif ml_choice == 'Artificial Neural Network':
                                st.image(evaluation_image, caption='Grafik hasil evaluasi model Artificial Neural Network')
                                st.write("Gambar di atas menunjukkan hasil metrik untuk klasifikasi kualitas air Sungai Citarum yaitu model Artificial Neural Network dan teknik oversampling SMOTE-ADASYN. Grafik kiri memecah metrik precision, recall, dan f1-score untuk masing-masing dari empat kelas yang dievaluasi.")
                                st.write("- Precision: Metrik ini mengukur ketepatan prediksi positif model. Nilai precision untuk kelas 1, 2, 3, dan 4 masing-masing adalah 89%, 92%, 89%, dan 99%.")
                                st.write("- Recall: Metrik ini mengukur kemampuan model dalam menangkap semua instance positif. Nilai recall untuk kelas 1, 2, 3, dan 4 masing-masing adalah 100%, 76%, 92%, dan 100%.")
                                st.write("- F1 Score: Metrik ini adalah harmonisasi rata-rata dari precision dan recall. Nilai f1-score untuk kelas 1, 2, 3, dan 4 masing-masing adalah 94%, 83%, 90%, dan 99%.")
                                st.write("Grafik kanan menampilkan accuracy keseluruhan model yang mencapai 91,8% menunjukkan bahwa model memiliki tingkat keberhasilan yang tinggi dalam mengklasifikasikan data kualitas air Sungai Citarum.")
                                st.write("Hasil akurasi model Artificial Neural Network dan SMOTE-ADASYN adalah 91,8")

                            elif ml_choice == 'Gaussian Naive Bayes':
                                st.image(evaluation_image, caption='Grafik hasil evaluasi model Gaussian Naive Bayes')
                                st.write("Gambar di atas menunjukkan hasil metrik untuk klasifikasi kualitas air Sungai Citarum yaitu model Artificial Neural Network dan teknik oversampling SMOTE-ADASYN. Grafik kiri memecah metrik precision, recall, dan f1-score untuk masing-masing dari empat kelas yang dievaluasi.")
                                st.write("- Precision: Metrik ini mengukur ketepatan prediksi positif model. Nilai precision untuk kelas 1, 2, 3, dan 4 masing-masing adalah 100%, 99%, 87%, dan 97%.")
                                st.write("- Recall: Metrik ini mengukur kemampuan model dalam menangkap semua instance positif. Nilai recall untuk kelas 1, 2, 3, dan 4 masing-masing adalah 100%, 85%, 96%, dan 100%.")
                                st.write("- F1 Score: Metrik ini adalah harmonisasi rata-rata dari precision dan recall. Nilai f1-score untuk kelas 1, 2, 3, dan 4 masing-masing adalah 100%, 91%, 91%, dan 99%.")
                                st.write("Grafik kanan menampilkan accuracy keseluruhan model yang mencapai 95,2% menunjukkan bahwa model memiliki tingkat keberhasilan yang tinggi dalam mengklasifikasikan data kualitas air Sungai Citarum.")
                                st.write("Hasil akurasi model Gaussian Naive Bayes dan SMOTE-ADASYN adalah 95,2")

                    except ValueError as e:
                        st.write(f"Mohon pastikan semua nilai sudah dimasukkan dengan benar dan dalam format numerik.")
                        st.write("Tidak boleh ada kolom yang kosong yes!")

            with col2:
                if st.button('Reset'):
                    st.session_state.pH = ""
                    st.session_state.TSS = ""
                    st.session_state.DO = ""
                    st.session_state.BOD = ""
                    st.session_state.COD = ""
                    st.session_state.Nitrat = ""
                    st.session_state.FecalColiform = ""
                    st.session_state.Fosfat = ""
                    st.session_state.IP = ""

        elif choice == 'Upload File':
            # Unggah file dataset
            st.write("Unggah file dataset CSV untuk klasifikasi otomatis:")
            uploaded_file = st.file_uploader("Unggah file dataset CSV", type="csv")

            if uploaded_file is not None:
                # Baca dataset
                df = pd.read_csv(uploaded_file)
            
                # Tampilkan dataset yang diunggah
                st.write("Dataset yang diunggah:")
                st.dataframe(df)  # Menampilkan seluruh dataset
            
                # Pastikan fitur yang diperlukan ada dalam dataset
                required_features = ['BOD', 'COD', 'FecalColiform', 'IP']
                if all(feature in df.columns for feature in required_features):
                    # Tambahkan kolom prediksi
                    if ml_choice == 'Artificial Neural Network':
                        df['Kualitas Air'] = df.apply(lambda row: predict_quality_ann(model, scaler, row['BOD'], row['COD'], row['FecalColiform'], row['IP'])[1], axis=1)
                    else:
                        df['Kualitas Air'] = df.apply(lambda row: predict_quality_general(model, scaler, row['BOD'], row['COD'], row['FecalColiform'], row['IP'])[1], axis=1)
                
                    # Tampilkan dataset dengan kolom prediksi
                    st.write("Hasil klasifikasi:")
                    st.write(df)
                
                    # Hitung jumlah setiap kelas
                    class_counts = df['Kualitas Air'].value_counts().reset_index()
                    class_counts.columns = ['Kualitas Air', 'Jumlah']

                    # Plot hasil klasifikasi
                    fig = px.pie(
                        class_counts,
                        names='Kualitas Air',
                        values='Jumlah',
                        title='<b>Hasil Klasifikasi Kualitas Air Sungai</b>',
                        template='plotly_white'
                    )
                    st.plotly_chart(fig)
                
                    # Opsi untuk mengunduh hasil klasifikasi
                    csv = df.to_csv(index=False)
                    b64 = base64.b64encode(csv.encode()).decode()  # B64 encode
                    href = f'<a href="data:file/csv;base64,{b64}" download="hasil_klasifikasi.csv">Unduh hasil klasifikasi</a>'
                    st.markdown(href, unsafe_allow_html=True)
                else:
                    st.error("Dataset tidak memiliki semua fitur yang dibutuhkan. Pastikan kolom BOD, COD, FecalColiform, dan IP ada dalam dataset.")
    else:

        st.write("Model tidak dapat dimuat. Pastikan file model valid dan coba lagi.")
app()
st.caption('Copyright © Citasi 2024')
