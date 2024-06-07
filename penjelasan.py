import streamlit as st
import requests
from PIL import Image
from io import BytesIO

def fetch_image_from_url(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    return image

def resize_image(image, size):
    resized_image = image.resize(size)
    return resized_image

def app():
    st.write('Penjelasan')

    st.subheader("Website Citasi")

    image_url = "https://github.com/ardhien50/Website-CITASI/blob/Front-End/Gambar/Logo%20Website%20Citasi.png?raw=true"
    try:
        image = fetch_image_from_url(image_url)
        resized_image = image.copy()
        resized_image.thumbnail((500, 500))
        st.image(resized_image, caption="Website Citasi", channels="RGB", use_column_width=True)
        st.write('Proyek ini mengangkat topik "Klasifikasi Kualitas Air Sungai Citarum Menggunakan Pembelajaran Mesin Berbasis Website". Melanjutkan project sebelumnya yang berbasis website dengan nama “quwaci”, dimana menyediakan sistem informasi mengenai kualitas air Sungai Citarum dibagi menjadi 8 titik sepanjang hulu hingga hilir. Dimana pada project kali ini diberikan penambahan fitur-fitur dan metode dalam pengklasifikasian air Sungai Citarum.')

    except Exception as e:
        st.error(f"Error fetching and displaying image: {e}")
    
    st.subheader("Metode Machine Learning")
    st.write('Berisikan metode metode Machine Learning yang digunakan pada projek website Citasi, diantaranya terdiri dari KNN with Eucidean Distance, Artificial Neural Network, dan Gaussian Naive Bayes.')
    
    st.subheader("1. Weighted KNN")

    image_url = "https://github.com/ardhien50/Website-CITASI/blob/Front-End/Gambar/knn.png?raw=true"
    try:
        image = fetch_image_from_url(image_url)
        resized_image = image.copy()
        resized_image.thumbnail((500, 500))
        st.image(resized_image, caption="Weighted KNN", channels="RGB", use_column_width=True)
        st.write('K-Nearest Neighbor merupakan salah satu algoritma yang digunakan dalam pengklasifikasian. Prinsip kerja K-Nearest Neighbor (KNN) adalah mencari jarak terdekat antara data yang akan dievaluasi dengan K-Nearest Neighbor terdekatnya dalam data pelatihan.')

        st.link_button("Baca selengkapnya", "https://www.ibm.com/topics/knn")
        
    except Exception as e:
        st.error(f"Error fetching and displaying image: {e}")

    st.subheader("2. Artificial Neural Network")

    image_url = "https://github.com/ardhien50/Website-CITASI/blob/Front-End/Gambar/Neural-Networks-Architecture.png?raw=true"
    try:
        image = fetch_image_from_url(image_url)
        resized_image = image.copy()
        resized_image.thumbnail((500, 500))
        st.image(resized_image, caption="Artificial Neural Network", channels="RGB", use_column_width=True)
        st.write('Jaringan saraf tiruan merupakan salah satu sistem pemrosesan informasi yang di desain dengan menirukan cara kerja otak manusia dalam menyelesaikan suatu masalah dengan melakukan proses belajar melalui perubahan bobot sinapsisnya. Jaringan saraf tiruan mampu melakukan pengenalan kegiatan berbasis data masa lalu. Data masa lalu akan dipelajari oleh jaringan syaraf tiruan sehingga mempunyai kemampuan untuk memberikan keputusan terhadap data yang belum pernah dipelajari.')

        st.link_button("Baca Selengkapnya", "https://www.analyticsvidhya.com/blog/2021/09/introduction-to-artificial-neural-networks/")
        
    except Exception as e:
        st.error(f"Error fetching and displaying image: {e}")


    st.subheader("3. Gaussian Naive Bayes")

    image_url = "https://github.com/ardhien50/Website-CITASI/blob/Front-End/Gambar/GNB.png?raw=true"
    try:
        image = fetch_image_from_url(image_url)
        resized_image = image.copy()
        resized_image.thumbnail((500, 500))
        st.image(resized_image, caption="Gaussian Naive Bayes", channels="RGB", use_column_width=True)
        st.write('Gaussian Naive Bayes (GNB) adalah teknik klasifikasi yang digunakan dalam pembelajaran mesin berdasarkan pendekatan probabilistik dan distribusi Gaussian. Gaussian Naive Bayes mengasumsikan bahwa setiap parameter, disebut juga fitur atau prediktor, memiliki kapasitas independen dalam memprediksi variabel keluaran.')

        st.link_button("Baca Selengkapnya", "https://builtin.com/artificial-intelligence/gaussian-naive-bayes")
        
    except Exception as e:
        st.error(f"Error fetching and displaying image: {e}")

    st.subheader('Dataset')
    with st.container():
        col1, col2, col3 = st.columns(3)

    with col1:
        image_div = st.empty()
        st.write("")
        st.image('https://github.com/ardhien50/Website-CITASI/blob/Front-End/Gambar/Logo%20DLH.png?raw=true')

    with col2:
        image_div = st.empty()
        st.write("")
        st.image('https://github.com/ardhien50/Website-CITASI/blob/Front-End/Gambar/Gedung%20DLHK.png?raw=true')

    with col3:
        image_div = st.empty()
        st.write("")
        st.image('https://github.com/ardhien50/Website-CITASI/blob/Front-End/Gambar/Logo%20DLHK%20Bandung.png?raw=true')
    
    st.write('Dengan menggunakan dataset yang sudah didapatkan dari Dinas Lingkungan Hidup dan Kebersihan Kota Bandung, nantinya akan dipilih tiga metode pembelajaran mesin yang dikiranya dapat memberikan hasil yang optimal. Di dalam dataset tersebut terdiri dari parameter kualitas air yaitu pH, TSS, DO, BOD, COD, Nitrat, Fecal Coliform, Fosfat, dan IP. Kemudian memisahkan datanya menjadi data latih dan data uji lalu membuat model pembelajaran mesin dari setiap model yang sudah ditentukan sebagai alternatif usulan solusi untuk klasifikasi kualitas air Sungai Citarum.')
    st.link_button('Tempat Mendapatkan Dataset', 'https://opendata.jabarprov.go.id/id')
    
    st.subheader("Kandungan Dalam Air")
    st.write('Berikut merupakan penjelasan mengenai data kandungan air yang terdapat pada website Citasi. Website akan menampilkan data data yang lengkap pada setiap titik poin. Dimana data yang yang diberikan akan berisikan, pH, TSS, DO, BOD, COD, Nitrat, Fecal Coliform, Fosfat, dan IP yang nantinya akan digunakan sebagai indikator untuk kualitas air pada titik tersebut.')

    with st.container():
        col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader('1. pH')
        st.write('pH (Potential of Hydrogen) adalah derajat keasaman yang digunakan untuk menyatakan tingkat keasaman atau kebasaan yang dimiliki oleh suatu larutan. Ia didefinisikan sebagai kologaritma aktivitas ion hidrogen (H+) yang terlarut. Koefisien aktivitas ion hidrogen tidak dapat diukur secara eksperimental, sehingga nilainya didasarkan pada perhitungan teoretis. Skala pH bukanlah skala absolut. Ia bersifat relatif terhadap sekumpulan larutan standar yang pH-nya ditentukan berdasarkan persetujuan internasional.')
        st.link_button("Bca Selengkapnya", "https://www.usgs.gov/special-topics/water-science-school/science/ph-and-water#:~:text=oil%20or%20alcohol.-,pH%20is%20a%20measure%20of%20how%20acidic%2Fbasic%20water%20is,hydroxyl%20ions%20in%20the%20water.")

    with col2:
        st.subheader('2. TSS')
        st.write('TSS (Total Suspended Solid) atau total padatan tersuspensi adalah padatan yang tersuspensi di dalam air berupa bahan-bahan organik dan inorganic yang dapat disaring dengan kertas millipore berpori pori 0,45 μm. Materi yang tersuspensi mempunyai dampak buruk terhadap kualitas air karena mengurangi penetrasi matahari ke dalam badan air, kekeruhan air meningkat yang menyebabkan gangguan pertumbuhan bagi organisme produser.')
        st.link_button('Baca Selengkapnya', 'https://www.handalselaras.com/total-suspended-solid-tss/')

    with col3:
        st.subheader('3. DO')
        st.write('DO (Dissolved Oxygen) merupakan faktor penting untuk keberlangsungan hidup organisme air. Istilah Dissolved Oxygen merupakan jumlah oksigen yang tidak terikat dan terkandung bebas dalam air. Indikator ini merupakan salah satu parameter yang dapat menentukan kesehatan lingkungan air untuk organisme yang hidup didalamnya.')
        st.link_button('Baca Selengkapnya', 'https://www.epa.gov/national-aquatic-resource-surveys/indicators-dissolved-oxygen#:~:text=What%20is%20dissolved%20oxygen%3F,of%20a%20pond%20or%20lake.')

    with col1:
        st.subheader('4. BOD')
        st.write('BOD atau Biochemical Oxygen Demand adalah suatu karakteristik yang menunjukkan jumlah oksigen terlarut yang diperlukan oleh mikroorganisme (biasanya bakteri) untuk mengurai atau mendekomposisi bahan organik dalam kondisi aerobik.')
        st.link_button('Baca Selengkapnya', 'https://waterpedia.co.id/pengertian-cod-dan-bod/')

    with col2:
        st.subheader('5. COD')
        st.write('Chemical Oxygen Demand (COD) adalah ukuran jumlah bahan kimia yang dapat dioksidasi dalam air. Tingkat COD yang tinggi di Sungai Citarum dapat menunjukkan tingkat polusi organik yang tinggi, seperti yang disebabkan oleh limbah domestik dan industri. Tingkat COD yang tinggi dapat merugikan ekosistem sungai dan kesehatan manusia yang bergantung pada air.')
        st.link_button('Baca Selengkapnya', 'https://waterpedia.co.id/pengertian-cod-dan-bod/')

    with col3:
        st.subheader('6. Nitrat')
        st.write('Nitrat adalah senyawa nitrogen yang paling teroksidasi penuh dan oleh karena itu stabil terhadap oksidasi, tetapi berpotensi menjadi agen pengoksidasi yang kuat. Nitrat yang terdapat di dalam sumber air seperti misalnya air sumur gali dan sungai umumnya berasal dari pencemaran bahan-bahan kimia (pupuk urea, ZA, dan lain-lainnya) di bagian hulu.')
        st.link_button('Baca Selengkapnya', 'https://jurnal.unismuhpalu.ac.id/index.php/JKS/article/view/3357')

    with col1:
        st.subheader('7. Fecal Coliform')
        st.write('Bakteri koliform adalah kumpulan mikroorganisme yang relatif tidak berbahaya yang hidup dalam jumlah besar di usus manusia dan hewan berdarah panas dan dingin. Mereka membantu pencernaan makanan. Subkelompok spesifik dari koleksi ini adalah bakteri fecal coliform, anggota yang paling umum adalah Escherichia coli. Organisme ini dapat dipisahkan dari kelompok koliform total karena kemampuannya untuk tumbuh pada suhu tinggi dan hanya berhubungan dengan kotoran hewan berdarah panas.')
        st.link_button('Baca Selengkapnya', 'https://www.knowyourh2o.com/outdoor-4/fecal-coliform-bacteria-in-water')

    with col2:
        st.subheader('8. Fosfat')
        st.write('Fosfat adalah salah satu unsur penting bagi pembentukan protein dan metabolisme. Senyawa ini termasuk turunan fosfor yang dapat ditemukan di tanah, udara, dan sedimen. Hal tersebut dijelaskan Anthon Masela dalam buku Karaginan Rumput Laut (Eucheuma Cottonii): Tinjauan Karakteristik Fisika dan Kimia. Fosfor yang ditemukan di alam, mencakup tanah, udara, dan sedimen, memiliki bentuk senyawa fosfat (batuan fosfat). Tidak seperti senyawa bahan lain, fosfor tidak dapat ditemukan di udara bertekanan tinggi.')
        st.link_button('Baca Selengkapnya', 'https://www.detik.com/edu/detikpedia/d-6280990/mengenal-fosfat-dan-kegunaannya-dalam-kehidupan-manusia')

    with col3:
        st.subheader('9. IP (Indeks Pencemaran)')
        st.write('Indeks Pencemaran Kualitas Air Sungai (IP) digunakan untuk mengukur tingkat pencemaran air berdasarkan parameter seperti pH, suhu, oksigen terlarut (DO), kebutuhan oksigen biokimia (BOD), kekeruhan, total padatan tersuspensi (TSS), fosfat, nitrat, dan jumlah faecal coliform. Berdasarkan nilai IP, kualitas air diklasifikasikan sebagai berikut:')
        st.write('1. Tidak Tercemar/Memenuhi Baku Mutu (0 ≤ IP ≤ 1): Air masih bersih dan sesuai standar.')
        st.write('2. Tercemar Ringan (1 < IP ≤ 5): Sedikit tercemar, namun masih dapat ditoleransi.')
        st.write('3. Tercemar Sedang (5 < IP ≤ 10): Pencemaran mulai mempengaruhi ekosistem dan penggunaan air.')
        st.write('4. Tercemar Berat (IP ≥ 10): Air sangat tercemar, memerlukan tindakan segera.')
        st.write('Indeks ini membantu dalam mengidentifikasi tingkat pencemaran dan menentukan langkah pengendalian yang diperlukan untuk menjaga kualitas air dan ekosistem.')
        st.link_button('Baca Selengkapnya', 'https://ppkl.menlhk.go.id/website/filebox/502/180719182446Indeks%20Kualitas%20Air.pdf')

    # Menambahkan judul untuk video
    st.subheader("Video Pameran CITASI")

    # HTML code untuk menyematkan video YouTube
    video_html = """
    <iframe width="560" height="315" src="https://www.youtube.com/embed/O4gGPnAA6vY" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
"""
    # Menampilkan video di Streamlit
    st.markdown(video_html, unsafe_allow_html=True)
    
    st.subheader('Team Capstone')
    with st.container():
        col1, col2, col3 = st.columns(3)

    with col1:
        image_div = st.empty()
        st.write("") # tambahkan baris kosong untuk jarak

        caption_div = st.empty()
        caption_div.markdown('**Daffa Asyqar Ahmad Khalisheka**<br><p style="margin-top:-10px;">S1 Teknik Komputer</p><hr style="width: 100%; margin: 3px 0;">',unsafe_allow_html=True)
        st.image('https://github.com/ardhien50/Website-CITASI/blob/Front-End/Gambar/daffasyqar.jpg?raw=true', width=200, use_column_width=True)

    with col2:
        image_div = st.empty()
        st.write("") # tambahkan baris kosong untuk jarak

        caption_div = st.empty()
        caption_div.markdown('**Rai Barokah Utari**<br><p style="margin-top:-10px;">S1 Teknik Komputer</p><hr style="width: 100%; margin: 3px 0;">',unsafe_allow_html=True)
        st.image('https://github.com/ardhien50/Website-CITASI/blob/Front-End/Gambar/Rai.jpg?raw=true', width=200, use_column_width=True)

    with col3:
        image_div = st.empty()
        st.write("") # tambahkan baris kosong untuk jarak

        caption_div = st.empty()
        caption_div.markdown('**Ardhien Fadhillah Suhartono**<br><p style="margin-top:-10px;">S1 Teknik Komputer</p><hr style="width: 100%; margin: 3px 0;">',unsafe_allow_html=True)
        st.image('https://github.com/ardhien50/Website-CITASI/blob/Front-End/Gambar/Ardhien.jpg?raw=true', width=200, use_column_width=True)

# Run the app
if __name__ == '__main__':
    app()
st.caption('Copyright © Citasi 2024')
