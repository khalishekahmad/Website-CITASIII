import streamlit as st

# Menampilkan teks "Kadmium 0.003 mg/L" menggunakan Markdown
st.markdown("## Kadmium\n0.003 mg/L")

# Membuat text input dengan teks default di dalamnya
teks_input = st.text_input("Masukkan teks di sini", value="")

# Menampilkan teks yang dimasukkan
st.write("Teks yang dimasukkan:", teks_input)
