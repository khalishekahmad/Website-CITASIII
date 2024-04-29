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
            'Apakah ingin melakukan analisa', 
            ('pH', 'TSS', 'DO', 'BOD', 'COD', 'Nitrat', 'FecalColiform', 'Fosfat', 'IP'),
            )

            output_coloumns = ['Class']
            df_grouped = df.groupby(by=[groupby_column], as_index=False)[output_coloumns].sum()
        
            fig = px.bar(
                df_grouped,
                x=groupby_column,
                y=output_coloumns,
                color_continuous_scale=['blue', 'red'],
                template='plotly_white',
                title=f'<b>Class by {groupby_column}</b>'
            )
            st.plotly_chart(fig)


app()