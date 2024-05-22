import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.express as px

# Load the pre-trained model
model_path = 'model_logreg.sav'
kualitas_air_sungai_logreg = pickle.load(open(model_path, 'rb'))

def app():
    st.title('Kalkulator Klasifikasi Kualitas Air Sungai Citarum')

    choice = st.selectbox('Pilih metode input data', ['Manual', 'Upload File'])

    if choice == 'Upload File':
        st.subheader('Silahkan Upload File Dalam Bentuk CSV')
        uploaded_file = st.file_uploader('Pilih file CSV', type='csv')
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df)

            groupby_column = st.selectbox(
                'Pilih kolom untuk dianalisis',
                df.columns.tolist(),  # Automatically list all columns
            )

            fig = px.bar(
                df,
                x=groupby_column,
                y='Class',
                color='Class',
                title=f'<b>Analisis Class berdasarkan {groupby_column}</b>',
                template='plotly_white'
            )
            st.plotly_chart(fig)

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

        if st.button('Submit'):
            try:
                input_data = np.array([[float(pH), float(TSS), float(DO), float(BOD), float(COD), float(Nitrat), float(FecalColiform), float(Fosfat), float(IP)]])
                
                st.write('Input Data:', input_data)
                
                if not np.isnan(input_data).any() and not np.isinf(input_data).any():
                    waterriver_class = kualitas_air_sungai_logreg.predict(input_data)
                    
                    st.write('Prediksi Kelas:', waterriver_class[0])

                    if waterriver_class[0] == 1:
                        klasifikasi_kualitas_airsungai = 'Air Sungai Citarum Memenuhi Baku Mutu'
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
                else:
                    klasifikasi_kualitas_airsungai = 'Input data contains NaN or infinity values.'
                    color = 'grey'
            except ValueError:
                klasifikasi_kualitas_airsungai = 'Mohon masukkan semua nilai dengan format yang benar.'
                color = 'grey'

            st.markdown(f'<div style="background-color: {color}; padding: 10px; border-radius: 5px;"><h3 style="color: white;">{klasifikasi_kualitas_airsungai}</h3></div>', unsafe_allow_html=True)
        
        # Display the manual data in a dataframe and plot it
        features = {
            'pH': pH,
            'TSS': TSS,
            'DO': DO,
            'BOD': BOD,
            'COD': COD,
            'Nitrat': Nitrat,
            'FecalColiform': FecalColiform,
            'Fosfat': Fosfat,
            'IP': IP
        }

        df_manual = pd.DataFrame(features, index=[0])
        st.write(df_manual)

        df_melted = df_manual.melt(var_name='Parameter', value_name='Nilai')
        df_melted['Nilai'] = df_melted['Nilai'].astype(str)

        fig = px.bar(
            df_melted,
            x='Parameter',
            y='Nilai',
            color='Parameter',
            title='Diagram Data Kualitas Air Sungai'
        )
        st.plotly_chart(fig)

if __name__ == '__main__':
    app()
