import streamlit as st
import pickle
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LogisticRegression

# Load the pre-trained models and scalers
logreg_model_path = 'model_logreg.sav'
knn_model_path = 'model_knn_euclidean.pkl'
scaler_path = 'scaler_knn_euclidean.pkl'

try:
    kualitas_air_sungai_logreg = pickle.load(open(logreg_model_path, 'rb'))
except FileNotFoundError:
    st.error('Logistic Regression model file not found. Please ensure that model_logreg.sav is in the correct directory.')
except ModuleNotFoundError as e:
    st.error(f'Module not found: {e}. Please install the required modules.')

try:
    knn_model = joblib.load(knn_model_path)
    scaler = joblib.load(scaler_path)
except FileNotFoundError:
    st.error('KNN model or scaler file not found. Please ensure that model_knn_euclidean.pkl and scaler_euclidean.pkl are in the correct directory.')

# Function for KNN classification
def predict_quality_knn(BOD, COD, FecalColiform, IP):
    input_data = scaler.transform([[BOD, COD, FecalColiform, IP]])
    prediction = knn_model.predict(input_data)[0]
    
    class_labels = {
        1: "Tidak tercemar/memenuhi baku mutu",
        2: "Tercemar ringan",
        3: "Tercemar sedang",
        4: "Tercemar berat"
    }
    
    return f"Kualitas Air Sungai Citarum: {class_labels.get(prediction, 'kelas tidak dikenal')} (Kelas {prediction})"

def app():
    st.title('Kalkulator Klasifikasi Kualitas Air Sungai Citarum')

    choice = st.selectbox('Pilih metode input data', ['Manual', 'Upload File'])

    if choice == 'Upload File':
        st.subheader('Silahkan Upload File Dalam Bentuk CSV')
        uploaded_file = st.file_uploader('Pilih file CSV', type='csv')
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df)

            required_columns = ['pH', 'TSS', 'DO', 'BOD', 'COD', 'Nitrat', 'FecalColiform', 'Fosfat', 'IP']
            if all(column in df.columns for column in required_columns):
                input_data = df[required_columns]

                try:
                    input_data = input_data.astype(float).to_numpy()
                    
                    predictions = kualitas_air_sungai_logreg.predict(input_data)
                    prediction_labels = []
                    for pred in predictions:
                        if pred == 1:
                            prediction_labels.append('Air Sungai Citarum Tidak Tercemar')
                        elif pred == 2:
                            prediction_labels.append('Air Sungai Citarum Tercemar Ringan')
                        elif pred == 3:
                            prediction_labels.append('Air Sungai Citarum Tercemar Sedang')
                        elif pred == 4:
                            prediction_labels.append('Air Sungai Citarum Tercemar Berat')
                        else:
                            prediction_labels.append('Kelas tidak dikenal')

                    df['Klasifikasi'] = prediction_labels
                    st.dataframe(df)

                    class_counts = df['Klasifikasi'].value_counts().reset_index()
                    class_counts.columns = ['Klasifikasi', 'Jumlah']

                    fig = px.pie(
                        class_counts,
                        names='Klasifikasi',
                        values='Jumlah',
                        title='<b>Hasil Klasifikasi Kualitas Air Sungai</b>',
                        template='plotly_white'
                    )
                    st.plotly_chart(fig)

                except ValueError:
                    st.error('Ada kesalahan dalam format data input. Pastikan semua kolom berisi nilai numerik.')
            else:
                st.error('File CSV tidak memiliki kolom yang diperlukan untuk prediksi.')

    elif choice == 'Manual':
        st.subheader('Silahkan masukkan data kualitas Air Sungai secara manual')
        col1, col2, col3 = st.columns(3)

        with col1:
            pH = st.text_input('Potential of Hydrogen (pH):', help="pH (Potential of Hydrogen) adalah ukuran keasaman yang digunakan untuk menyatakan tingkat keasaman atau kebasahan yang dimiliki oleh suatu larutan.", placeholder="6 - 8")
            TSS = st.text_input('Total Suspended Solids (TSS):', help="Total Suspended Solids (TSS) adalah ukuran partikel tergantung dalam air, dalam miligram per liter (mg/L).", placeholder="20 - 36 mg/L")
            DO = st.text_input('Dissolved Oxygen (DO):', help="Dissolved Oxygen (DO) adalah ukuran oksigen yang terlarut dalam air, dalam miligram per liter (mg/L).", placeholder="0.00 - 7.79 mg/L")

        with col2:
            BOD = st.text_input('Biochemical Oxygen Demand (BOD):', help="Biochemical Oxygen Demand (BOD) adalah jumlah oksigen terlarut yang dibutuhkan oleh organisme biologis aerobik untuk memecah bahan organik yang ada dalam sampel air tertentu pada suhu tertentu selama periode waktu tertentu, dalam miligram per liter (mg/L).", placeholder="1.7 - 6 mg/L")
            COD = st.text_input('Chemical Oxygen Demand (COD):', help="Chemical Oxygen Demand (COD) adalah ukuran kapasitas air untuk mengkonsumsi oksigen selama dekomposisi bahan organik dan oksidasi bahan kimia anorganik seperti amonia dan nitrit, dalam miligram per liter (mg/L).", placeholder="10 - 30 mg/L")
            Nitrat = st.text_input('Nitrat:', help="Nitrate (NO3) adalah ukuran konsentrasi nitrat dalam air, dalam miligram per liter (mg/L).", placeholder="0 - 4 mg/L")

        with col3:
            FecalColiform = st.text_input('Fecal Coliform:', help="Fecal Coliform adalah sekelompok bakteri yang ditemukan di usus hewan berdarah panas dan digunakan sebagai indikator kontaminasi feses dalam air, dalam jumlah koloni per 100 mililiter (cfu/100 mL).", placeholder="50 - 100 jml/100L")
            Fosfat = st.text_input('Fosfat:', help="Phosphate (PO4) adalah ukuran konsentrasi fosfat dalam air, dalam miligram per liter (mg/L).", placeholder="0.03 - 0.1 mg/L")
            IP = st.text_input('Indeks Pencemaran (IP):', help="Indeks Pencemaran (IP) adalah ukuran polusi pada sungai.", placeholder="Masukkan nilai IP...")

        col1, col2 = st.columns(2)

        with col1:
            if st.button('Klasifikasi'):
                if not all([pH, TSS, DO, BOD, COD, Nitrat, FecalColiform, Fosfat, IP]):
                    st.error('Mohon masukkan semua nilai dengan format yang benar.')
                else:
                    try:
                        input_data = np.array([[float(pH), float(TSS), float(DO), float(BOD), float(COD), float(Nitrat), float(FecalColiform), float(Fosfat), float(IP)]])
                        
                        st.write('Input Data:', input_data)
                        
                        if not np.isnan(input_data).any() and not np.isinf(input_data).any():
                            waterriver_class = kualitas_air_sungai_logreg.predict(input_data)
                            knn_result = predict_quality_knn(float(BOD), float(COD), float(FecalColiform), float(IP))
                            
                            st.write('Prediksi Kelas (Logistic Regression):', waterriver_class[0])

                            if waterriver_class[0] == 1:
                                klasifikasi_kualitas_airsungai = 'Air Sungai Citarum Tidak Tercemar'
                                color = 'blue'
                            elif waterriver_class[0] == 2:
                                klasifikasi_kualitas_airsungai = 'Air Sungai Citarum Tercemar Ringan'
                                color = 'yellow'
                            elif waterriver_class[0] == 3:
                                klasifikasi_kualitas_airsungai = 'Air Sungai Citarum Tercemar Sedang'
                                color = 'orange'
                            elif waterriver_class[0] == 4:
                                klasifikasi_kualitas_airsungai = 'Air Sungai Citarum Tercemar Berat'
                                color = 'red'
                            else:
                                klasifikasi_kualitas_airsungai = 'Kelas tidak dikenal'
                                color = 'grey'

                            st.markdown(f'<div style="background-color: {color}; padding: 10px; border-radius: 5px;"><h3 style="color: white;">{klasifikasi_kualitas_airsungai}</h3></div>', unsafe_allow_html=True)
                            st.write(knn_result)
                            st.write("Hasil akurasi model KNN dengan Euclidean Distance adalah 95%")
                        else:
                            klasifikasi_kualitas_airsungai = 'Input data contains NaN or infinity values.'
                            color = 'grey'
                    except ValueError:
                        klasifikasi_kualitas_airsungai = 'Mohon masukkan semua nilai dengan format yang benar.'
                        color = 'grey'

                    st.markdown(f'<div style="background-color: {color}; padding: 10px; border-radius: 5px;"><h3 style="color: white;">{klasifikasi_kualitas_airsungai}</h3></div>', unsafe_allow_html=True)

                    try:
                        features = {
                            'pH': float(pH),
                            'TSS': float(TSS),
                            'DO': float(DO),
                            'BOD': float(BOD),
                            'COD': float(COD),
                            'Nitrat': float(Nitrat),
                            'FecalColiform': float(FecalColiform),
                            'Fosfat': float(Fosfat),
                            'IP': float(IP)
                        }

                        df_manual = pd.DataFrame(features, index=[0])
                        st.write(df_manual)

                        df_melted = df_manual.melt(var_name='Parameter', value_name='Nilai')

                        fig = px.pie(
                            df_melted,
                            names='Parameter',
                            values='Nilai',
                            title='Diagram Data Kualitas Air Sungai'
                        )
                        st.plotly_chart(fig)
                    except ValueError:
                        st.error('Ada kesalahan dalam format data input. Pastikan semua kolom berisi nilai numerik.')

        with col2:
            if st.button('Reset'):
                st.experimental_rerun()

app()
