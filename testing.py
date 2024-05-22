import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Fungsi utama aplikasi
def app():
    st.title('Kalkulator Klasifikasi Kualitas Air Sungai Citarum')

    choice = st.selectbox('Pilih Metode Input', ['Manual', 'Upload File'])

    # Jika pilihan Upload File
    if choice == 'Upload File':
        st.subheader('Silahkan Upload File Dalam Bentuk CSV')
        uploaded_file = st.file_uploader('Pilih file CSV', type='csv')
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df)

            model = load_model()
            if model:
                df['Prediction'] = model.predict(df[['pH', 'TSS', 'DO', 'BOD', 'COD', 'Nitrat', 'FecalColiform', 'Fosfat', 'IP']])
                st.write('Hasil Prediksi:')
                st.dataframe(df)

                fig = px.pie(df, names='Prediction', title='Distribusi Klasifikasi Kualitas Air Sungai')
                st.plotly_chart(fig)
    
    # Jika pilihan Manual
    elif choice == 'Manual':
        st.subheader('Silahkan masukkan data kualitas Air Sungai secara manual')
        col1, col2, col3 = st.columns(3)

        with col1:
            pH = st.text_input('Input Nilai pH', placeholder='6-8')
            TSS = st.text_input('Input Nilai TSS', placeholder='20-36 mg/L')
            DO = st.text_input('Input Nilai DO', placeholder='0,00-7,79 mg/L')
        with col2:
            BOD = st.text_input('Input Nilai BOD', placeholder='1,7-6 mg/L')
            COD = st.text_input('Input Nilai COD', placeholder='10-30 mg/L')
            Nitrat = st.text_input('Input Nilai Nitrat', placeholder='0-4 mg/L')
        with col3:
            FecalColiform = st.text_input('Input Nilai FecalColiform', placeholder='50-100 jml/100L')
            Fosfat = st.text_input('Input Nilai Fosfat', placeholder='0,03-0,1 mg/L')
            IP = st.text_input('Input Nilai IP', placeholder='0')

        if st.button('Submit'):
            try:
                input_data = np.array([[float(pH), float(TSS), float(DO), float(BOD), float(COD), float(Nitrat), float(FecalColiform), float(Fosfat), float(IP)]])
                st.write('Input Data:', input_data)  # Output untuk verifikasi data input

                model = load_model()
                if model:
                    waterriver_class = model.predict(input_data)
                    st.write('Prediksi Kelas:', waterriver_class[0])  # Output hasil prediksi

                    klasifikasi_kualitas_airsungai, color = interpret_prediction(waterriver_class[0])
                else:
                    klasifikasi_kualitas_airsungai = 'Model tidak berhasil dimuat.'
                    color = 'grey'

            except ValueError:
                klasifikasi_kualitas_airsungai = 'Mohon masukkan semua nilai dengan format yang benar.'
                color = 'grey'

            st.markdown(f'<div style="background-color: {color}; padding: 10px; border-radius: 5px;"><h3 style="color: white;">{klasifikasi_kualitas_airsungai}</h3></div>', unsafe_allow_html=True)

def load_model():
    try:
        return pickle.load(open('model_logreg.sav', 'rb'))
    except Exception as e:
        st.write(f'Error loading model: {e}')
        return None

def interpret_prediction(prediction):
    if prediction == 1:
        return 'Air Sungai Citarum Tidak Tercemar', 'blue'
    elif prediction == 2:
        return 'Air Sungai Citarum Tercemar Ringan', 'yellow'
    elif prediction == 3:
        return 'Air Sungai Citarum Tercemar Sedang', 'orange'
    elif prediction == 4:
        return 'Air Sungai Citarum Tercemar Berat', 'red'
    else:
        return 'Kelas tidak dikenal', 'grey'

# Evaluasi Model dengan Data Uji
def evaluate_model():
    st.subheader('Evaluasi Model dengan Data Uji')
    data_uji = pd.read_csv('data_uji.csv')  # Ganti dengan path yang benar

    X_test = data_uji[['pH', 'TSS', 'DO', 'BOD', 'COD', 'Nitrat', 'FecalColiform', 'Fosfat', 'IP']].values
    y_test = data_uji['Class']  # Ganti dengan nama kolom label yang sesuai

    model = load_model()
    if model:
        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')

        st.write(f'Akurasi: {accuracy}')
        st.write(f'Presisi: {precision}')
        st.write(f'Recall: {recall}')
        st.write(f'F1 Score: {f1}')
    else:
        st.write('Model tidak berhasil dimuat.')

# Panggil fungsi utama
if __name__ == '__main__':
    app()
    evaluate_model()
