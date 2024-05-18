import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from scipy.spatial import distance

def knn_predict(X_train, y_train, X_test, k=3):
    # Calculate Euclidean distances
    distances = distance.cdist(X_test, X_train, 'euclidean')
    neighbors_idx = np.argsort(distances, axis=1)[:, :k]
    neighbors_labels = y_train[neighbors_idx]
    predictions = np.array([np.argmax(np.bincount(labels)) for labels in neighbors_labels])
    return predictions

def preprocess_input(df):
    # Ensure all columns are of float type
    df['pH'] = df['pH'].astype(float)
    df['TSS'] = df['TSS'].astype(float)
    df['DO'] = df['DO'].astype(float)
    df['BOD'] = df['BOD'].astype(float)
    df['COD'] = df['COD'].astype(float)
    df['Nitrat'] = df['Nitrat'].astype(float)
    df['FecalColiform'] = df['FecalColiform'].astype(float)
    df['Fosfat'] = df['Fosfat'].astype(float)
    
    # Handle missing columns by adding them with default values
    expected_columns = ['pH', 'TSS', 'DO', 'BOD', 'COD', 'Nitrat', 'FecalColiform', 'Fosfat', 'NH3N', 'TOC']
    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0.0

    return df

def app():
    st.write('Kalkulator')
    st.title('Kalkulator')

    choice = st.selectbox('Manual atau Upload File', ['Manual', 'Upload File'])

    if choice == 'Upload File':
        st.subheader('Silahkan Upload File Dalam Bentuk CSV')
        uploaded_file = st.file_uploader('Choose a CSV file', type='csv')
        if uploaded_file:
            st.markdown('---')
            df_uploaded = pd.read_csv(uploaded_file)
            st.dataframe(df_uploaded)
            groupby_column = st.selectbox(
                'Pilih kolom untuk dianalisis',
                ('pH', 'TSS', 'DO', 'BOD', 'COD', 'Nitrat', 'FecalColiform', 'Fosfat'),
            )

            # Plot data berdasarkan kolom yang dipilih
            fig = px.bar(
                df_uploaded,
                x=groupby_column,
                y='Class',
                color='Class',
                title=f'<b>Analisis Class berdasarkan {groupby_column}</b>',
                template='plotly_white'
            )
            st.plotly_chart(fig)

    elif choice == 'Manual':
        st.subheader('Silahkan masukkan data kualitas :blue[Air Sungai] secara manual')
        col1, col2, col3 = st.columns(3)

        with col1:
            pH = st.number_input('Input Nilai pH', min_value=0.0, max_value=14.0, value=7.0)
            TSS = st.number_input('Input Nilai TSS (mg/L)', min_value=0.0, value=28.0)
            DO = st.number_input('Input Nilai DO (mg/L)', min_value=0.0, value=5.0)
            NH3N = st.number_input('Input Nilai NH3N (mg/L)', min_value=0.0, value=0.5)
        with col2:
            BOD = st.number_input('Input Nilai BOD (mg/L)', min_value=0.0, value=3.0)
            COD = st.number_input('Input Nilai COD (mg/L)', min_value=0.0, value=20.0)
            Nitrat = st.number_input('Input Nilai Nitrat (mg/L)', min_value=0.0, value=2.0)
            TOC = st.number_input('Input Nilai TOC (mg/L)', min_value=0.0, value=5.0)
        with col3:
            FecalColiform = st.number_input('Input Nilai FecalColiform (jml/100L)', min_value=0.0, value=75.0)
            Fosfat = st.number_input('Input Nilai Fosfat (mg/L)', min_value=0.0, value=0.05)
            # Adding missing columns
            # Oxygen Demanding Substances (ODS)
            ODS = st.number_input('Input Nilai ODS (mg/L)', min_value=0.0, value=4.0)
            # Total Nitrogen (TN)
            TN = st.number_input('Input Nilai TN (mg/L)', min_value=0.0, value=2.0)

        if st.button('Submit'):
            features = {
                'pH': pH,
                'TSS': TSS,
                'DO': DO,
                'BOD': BOD,
                'COD': COD,
                'Nitrat': Nitrat,
                'FecalColiform': FecalColiform,
                'Fosfat': Fosfat,
                'NH3N': NH3N,
                'TOC': TOC,
                'ODS': ODS,
                'TN': TN,
            }

            # Convert the inputs to a DataFrame
            df_manual = pd.DataFrame(features, index=[0])
            st.write(df_manual)

            # Preprocess the data to match the model input
            df_manual_processed = preprocess_input(df_manual)

            # Load the training data from CSV file
            training_file = 'DatasetCitasi/DataCITASI.csv'  # Replace with actual file path
            try:
                df_train = pd.read_csv(training_file)
            except FileNotFoundError:
                st.error('File training_data.csv tidak ditemukan. Pastikan file ada di direktori yang benar.')
                return

            # Assuming the training CSV has the same preprocessing steps
            df_train_processed = preprocess_input(df_train)

            # Separate features and target
            X_train = df_train_processed.drop(columns='Class').values
            y_train = df_train_processed['Class'].values

            # Ensure the feature dimensions match
            if X_train.shape[1] != df_manual_processed.shape[1]:
                st.error(f'Jumlah fitur input ({df_manual_processed.shape[1]}) tidak sesuai dengan jumlah fitur data pelatihan ({X_train.shape[1]}).')
                return

            # Make a prediction using KNN
            prediction = knn_predict(X_train, y_train, df_manual_processed.values, k=3)

            # Display the prediction
            st.subheader(f'Prediksi Kelas: {prediction[0]}')

            # Plot the data
            fig = px.bar(
                df_manual.melt(var_name='Parameter', value_name='Nilai'),
                x='Parameter',
                y='Nilai',
                color='Parameter',
                title='Diagram Data Kualitas Air Sungai'
            )
            st.plotly_chart
            st.plotly_chart(fig)

app()
