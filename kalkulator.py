import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.write('Kalkulator')
    st.title('Kalkulator')

    choice = st.selectbox('Manual atau Upload File', ['Manual','Upload File'])

    if choice == ('Upload File'):
        st.subheader('Silahkan Upload File Dalam Bentuk CSV')
        uploaded_file = st.file_uploader('Choose a CSV file', type='csv')
        if uploaded_file:
            st.markdown('---')
            df = pd.read_csv(uploaded_file)
            st.dataframe(df)
            groupby_column = st.selectbox(
                'Pilih kolom untuk dianalisis',
                ('pH', 'TSS', 'DO', 'BOD', 'COD', 'Nitrat', 'FecalColiform', 'Fosfat', 'IP'),
            )

            # Plot data berdasarkan kolom yang dipilih
            fig = px.bar(
                df,
                x=groupby_column,
                y='Class',
                color='Class',
                title=f'<b>Analisis Class berdasarkan {groupby_column}</b>',
                template='plotly_white'
            )
            st.plotly_chart(fig)
    
    elif choice == ('Manual'):
        
        st.subheader('Silahkan masukkan data kualitas :blue[Air Sungai] secara manual')
        col1, col2, col3 = st.columns(3)

        with col1:
            pH = st.text_input('Input Nilai pH', value=('6-8'))
            TSS = st.text_input('Input Nilai TSS', value=('20-36 mg/L'))
            DO = st.text_input('Input Nilai DO', value=('0,00-7,79 mg/L'))
        with col2:
            BOD = st.text_input('Input Nilai BOD', value=('1,7-6 mg/L'))
            COD = st.text_input('Input Nilai COD', value=('10-30 mg/L'))
            Nitrat = st.text_input('Input Nilai Nitrat', value=('0-4 mg/L'))
        with col3:
            FecalColiform = st.text_input('Input Nilai FecalColiform', value=('50-100 jml/100L'))
            Fosfat = st.text_input('Input Nilai Fosfat', value=('0,03-0,1 mg/L'))
            IP = st.text_input('Input Nilai IP', value=('0'))

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
                'IP': IP
            }

            df_manual = pd.DataFrame(features, index=[0])
            st.write(df_manual)

            fig = px.bar(
                df_manual.melt(var_name='Parameter', value_name='Nilai'),
                x='Parameter',
                y='Nilai',
                color='Parameter',
                title='Diagram Data Kualitas Air Sungai'
            )
            st.plotly_chart(fig)


app()