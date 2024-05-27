import streamlit as st
import pandas as pd
import joblib
import base64  # Impor modul base64 untuk encoding file CSV
import plotly.express as px  # Impor Plotly untuk visualisasi

# Fungsi untuk klasifikasi
def predict_quality(model, scaler, BOD, COD, FecalColiform, IP):
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
def app():
    # Judul aplikasi
    st.title('Kalkulator Klasifikasi Kualitas Air Sungai Citarum')

    # Pilihan metode machine learning
    ml_choice = st.selectbox('Silahakan pilih metode Machine Learning untuk melihat hasil yang berbeda', ['Weighted KNN','Artificial Neural Network', 'Gaussian Naive Bayes'])

    # Load model dan scaler sesuai pilihan
    if ml_choice == 'Weighted KNN':
        model_path = 'model_knn_euclidean.pkl'
        scaler_path = 'scaler_knn_euclidean.pkl'
    elif ml_choice == 'Artificial Neural Network':
        model_path = 'model_ann.pkl'
        scaler_path = 'scaler_ann.pkl'
    elif ml_choice == 'Gaussian Naive Bayes':
        model_path = 'model_gnb.pkl'
        scaler_path = 'scaler_gnb.pkl'

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)

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

        # Input parameter dari user dalam tiga kolom
        col1, col2, col3 = st.columns(3)

        with col1:
            st.session_state.pH = st.text_input('Potential of Hydrogen (pH):', value=st.session_state.pH, help="pH (Potential of Hydrogen) adalah ukuran keasaman yang digunakan untuk menyatakan tingkat keasaman atau kebasahan yang dimiliki oleh suatu larutan.", placeholder="6 - 8")
            st.session_state.TSS = st.text_input('Total Suspended Solids (TSS):', value=st.session_state.TSS, help="Total Suspended Solids (TSS) adalah ukuran partikel tergantung dalam air, dalam miligram per liter (mg/L).", placeholder="20 - 36 mg/L")
            st.session_state.DO = st.text_input('Dissolved Oxygen (DO):', value=st.session_state.DO, help="Dissolved Oxygen (DO) adalah ukuran oksigen yang terlarut dalam air, dalam miligram per liter (mg/L).", placeholder="0.00 - 7.79 mg/L")

        with col2:
            st.session_state.BOD = st.text_input('Biochemical Oxygen Demand:', value=st.session_state.BOD, help="Biochemical Oxygen Demand (BOD) adalah jumlah oksigen terlarut yang dibutuhkan oleh organisme biologis aerobik untuk memecah bahan organik yang ada dalam sampel air tertentu pada suhu tertentu selama periode waktu tertentu, dalam miligram per liter (mg/L).", placeholder="1.7 - 6 mg/L")
            st.session_state.COD = st.text_input('Chemical Oxygen Demand (COD):', value=st.session_state.COD, help="Chemical Oxygen Demand (COD) adalah ukuran kapasitas air untuk mengkonsumsi oksigen selama dekomposisi bahan organik dan oksidasi bahan kimia anorganik seperti amonia dan nitrit, dalam miligram per liter (mg/L).", placeholder="10 - 30 mg/L")
            st.session_state.Nitrat = st.text_input('Nitrat:', value=st.session_state.Nitrat, help="Nitrate (NO3) adalah ukuran konsentrasi nitrat dalam air, dalam miligram per liter (mg/L).", placeholder="0 - 4 mg/L")

        with col3:
            st.session_state.FecalColiform = st.text_input('Fecal Coliform:', value=st.session_state.FecalColiform, help="Fecal Coliform adalah sekelompok bakteri yang ditemukan di usus hewan berdarah panas dan digunakan sebagai indikator kontaminasi feses dalam air, dalam jumlah koloni per 100 mililiter (cfu/100 mL).", placeholder="50 - 100 jml/100L")
            st.session_state.Fosfat = st.text_input('Fosfat:', value=st.session_state.Fosfat, help="Phosphate (PO4) adalah ukuran konsentrasi fosfat dalam air, dalam miligram per liter (mg/L).", placeholder="0.03 - 0.1 mg/L")
            st.session_state.IP = st.text_input('Indeks Pencemaran (IP):', value=st.session_state.IP, help="Indeks Pencemaran (IP) adalah ukuran polusi pada sungai.", placeholder="Masukkan nilai IP...")

        # Tombol untuk klasifikasi dan reset
        col1, col2 = st.columns(2)

        with col1:
            if st.button('Klasifikasi'):
                try:
                    # Konversi input menjadi float
                    pH = float(st.session_state.pH)
                    TSS = float(st.session_state.TSS)
                    DO = float(st.session_state.DO)
                    BOD = float(st.session_state.BOD)
                    COD = float(st.session_state.COD)
                    Nitrat = float(st.session_state.Nitrat)
                    FecalColiform = float(st.session_state.FecalColiform)
                    Fosfat = float(st.session_state.Fosfat)
                    IP = float(st.session_state.IP)

                    # Pengecekan nilai negatif
                    if any(val < 0 for val in [pH, TSS, DO, BOD, COD, Nitrat, FecalColiform, Fosfat, IP]):
                        st.write("OH NO! Maaf tidak boleh ada nilai negatif. Mohon Pastikan semua nilai sudah benar.")
                    else:
                        prediction, result, color = predict_quality(model, scaler, BOD, COD, FecalColiform, IP)
                        st.markdown(f'<div style="background-color:{color};padding:10px;border-radius:5px;">{result}</div>', unsafe_allow_html=True)
                        st.write("MANTAB!!! Model KNN dengan Euclidean Distance telah mencapai akurasi sebesar 95%.")
                except ValueError as e:
                    st.write(f"OOOPS! Mohon Pastikan semua nilai sudah dimasukkan dengan benar dan dalam format numerik.")
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
        # Upload file dataset
        st.write("Unggah file dataset CSV untuk klasifikasi otomatis:")
        uploaded_file = st.file_uploader("Unggah file dataset CSV", type="csv")

        if uploaded_file is not None:
            # Membaca dataset
            df = pd.read_csv(uploaded_file)
        
            # Menampilkan dataset yang diunggah
            st.write("Dataset yang diunggah:")
            st.write(df.head())
        
            # Memastikan fitur yang dibutuhkan ada dalam dataset
            required_features = ['BOD', 'COD', 'FecalColiform', 'IP']
            if all(feature in df.columns for feature in required_features):
                    # Menambahkan kolom prediksi
                df['Kualitas Air'] = df.apply(lambda row: predict_quality(model, scaler, row['BOD'], row['COD'], row['FecalColiform'], row['IP'])[1], axis=1)
            
                # Menampilkan dataset dengan kolom prediksi
                st.write("Hasil klasifikasi:")
                st.write(df)
            
                # Count the number of occurrences of each class
                class_counts = df['Kualitas Air'].value_counts().reset_index()
                class_counts.columns = ['Kualitas Air', 'Jumlah']

                # Plotting the classification results
                fig = px.pie(
                    class_counts,
                    names='Kualitas Air',
                    values='Jumlah',
                    title='<b>Hasil Klasifikasi Kualitas Air Sungai</b>',
                    template='plotly_white'
                )
                st.plotly_chart(fig)
            
            # Menyediakan opsi untuk mengunduh hasil klasifikasi
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # B64 encode
            href = f'<a href="data:file/csv;base64,{b64}" download="hasil_klasifikasi.csv">Unduh hasil klasifikasi</a>'
            st.markdown(href, unsafe_allow_html=True)
        else:
            st.error("Dataset tidak memiliki semua fitur yang dibutuhkan. Pastikan kolom BOD, COD, FecalColiform, dan IP ada dalam dataset.")


