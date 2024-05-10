import streamlit as st

def app():
    st.write('Metode')
    st.title('Titik Peta Sungai :blue[Citarum]')

    choice = st.selectbox('Silahakan pilih metode Machine Learning untuk melihat hasil yang berbeda', ['KNN with Euclidean Distance','Artificial Neural Network', 'Gaussian Naive Bayes'])

    if choice == ('KNN with Euclidean Distance'):
        st.subheader('KNN with Euclidean Distance')

        html_code = """
        <div id="map" style="height: 500px; width: 100%;"></div>
        <p id="marker_info" style="font-weight: bold;"></p>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.css" />
        <script>
            var locations = {
                "Titik Sungai: Situ Cisanti<br>Alamat: Neglawangi, Kertasari,<br>Bandung Regency, West Java 40386,<br>Memenuhi Baku Mutu": [-7.208484677933202, 107.65792566573455],  // Source of the Citarum River
                "Titik Sungai: Bendungan Saguling<br>Alamat: Saguling, Batujajar,<br>West Bandung Regency, West Java,<br>Tercemar Sedang ": [-6.913526, 107.367661], // Saguling Dam
                "Titik Sungai: Bendungan Cirata<br>Alamat: Citamiang, Maniis,<br>Purwakarta Regency, West Java 41166,<br>Tercemar Berat": [-6.700203, 107.364963], // Cirata Dam
                "Titik Sungai: Bendungan Jatiluhur<br>Alamat: Kutamanah, Sukasari,<br>Purwakarta Regency, West Java 41116,<br>Tercemar Ringan": [-6.526997, 107.385456], // Jatiluhur Dam
                "Titik Sungai: Kabupaten Karawang<br>Alamat: Sungai Citarum, Telukjambe Timur,<br>Karawang, West Java 41361,<br>Memenuhi Baku Mutu": [-6.298185, 107.287757],  // Karawang Regency
                "Titik Sungai: Muara Gembong<br>Alamat: Kecamatan Muara Gembong,<br>Bekasi Regency, West Java,<br>Tercemar Ringan": [-5.984462, 107.043829], // Bekasi
                "Titik Sungai: Sungai Cikapundung<br>Alamat: Bandung City, West Java,<br>Tercemar Berat": [-6.898969, 107.606402],  // Bandung City
                "Titik Sungai: Dayeuhkolot<br>Alamat: Dayeuhkolot, Bandung, West Java,<br>Tercemar Sedang": [-6.990974, 107.626285]  // Dayeuhkolot
            };

            var map = L.map('map').setView([-6.8650, 107.4912], 10);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 18,
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
            }).addTo(map);

            Object.keys(locations).forEach(function(place) {
                var coord = locations[place];
                var marker = L.marker(coord).addTo(map);
                marker.bindPopup(place);
                marker.on('click', function() {
                    handleMarkerClick(marker, place);
                });
            });

            function handleMarkerClick(marker, place) {
                var info_paragraph = document.getElementById("marker_info");
                info_paragraph.innerHTML = place;
                var command = "place_clicked:" + place;
                Streamlit.setComponentValue(command);
            }
        </script>
        """
        st.components.v1.html(html_code, height=600)

        if st.session_state.get("clicked_marker"):
            place = st.session_state.get("clicked_marker").split(":")[1]
            st.write(place)


    elif choice == ('Artificial Neural Network'):
        st.subheader('Artificial Neural Network')

        html_code = """
        <div id="map" style="height: 500px; width: 100%;"></div>
        <p id="marker_info" style="font-weight: bold;"></p>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.css" />
        <script>
            var locations = {
                "Titik Sungai: Situ Cisanti<br>Alamat: Neglawangi, Kertasari,<br>Bandung Regency, West Java 40386,<br>Memenuhi Baku Mutu": [-7.208484677933202, 107.65792566573455],  // Source of the Citarum River
                "Titik Sungai: Bendungan Saguling<br>Alamat: Saguling, Batujajar,<br>West Bandung Regency, West Java,<br>Tercemar Sedang ": [-6.913526, 107.367661], // Saguling Dam
                "Titik Sungai: Bendungan Cirata<br>Alamat: Citamiang, Maniis,<br>Purwakarta Regency, West Java 41166,<br>Tercemar Berat": [-6.700203, 107.364963], // Cirata Dam
                "Titik Sungai: Bendungan Jatiluhur<br>Alamat: Kutamanah, Sukasari,<br>Purwakarta Regency, West Java 41116,<br>Tercemar Ringan": [-6.526997, 107.385456], // Jatiluhur Dam
                "Titik Sungai: Kabupaten Karawang<br>Alamat: Sungai Citarum, Telukjambe Timur,<br>Karawang, West Java 41361,<br>Memenuhi Baku Mutu": [-6.298185, 107.287757],  // Karawang Regency
                "Titik Sungai: Muara Gembong<br>Alamat: Kecamatan Muara Gembong,<br>Bekasi Regency, West Java,<br>Tercemar Ringan": [-5.984462, 107.043829], // Bekasi
                "Titik Sungai: Sungai Cikapundung<br>Alamat: Bandung City, West Java,<br>Tercemar Berat": [-6.898969, 107.606402],  // Bandung City
                "Titik Sungai: Dayeuhkolot<br>Alamat: Dayeuhkolot, Bandung, West Java,<br>Tercemar Sedang": [-6.990974, 107.626285]  // Dayeuhkolot
            };

            var map = L.map('map').setView([-6.8650, 107.4912], 10);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 18,
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
            }).addTo(map);

            Object.keys(locations).forEach(function(place) {
                var coord = locations[place];
                var marker = L.marker(coord).addTo(map);
                marker.bindPopup(place);
                marker.on('click', function() {
                    handleMarkerClick(marker, place);
                });
            });

            function handleMarkerClick(marker, place) {
                var info_paragraph = document.getElementById("marker_info");
                info_paragraph.innerHTML = place;
                var command = "place_clicked:" + place;
                Streamlit.setComponentValue(command);
            }
        </script>
        """
        st.components.v1.html(html_code, height=600)

        if st.session_state.get("clicked_marker"):
            place = st.session_state.get("clicked_marker").split(":")[1]
            st.write(place)

    elif choice == ('Gaussian Naive Bayes'):
        st.subheader('Gaussian Naive Bayes')

        html_code = """
        <div id="map" style="height: 500px; width: 100%;"></div>
        <p id="marker_info" style="font-weight: bold;"></p>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.css" />
        <script>
            var locations = {
                "Titik Sungai: Situ Cisanti<br>Alamat: Neglawangi, Kertasari,<br>Bandung Regency, West Java 40386,<br>Memenuhi Baku Mutu": [-7.208484677933202, 107.65792566573455],  // Source of the Citarum River
                "Titik Sungai: Bendungan Saguling<br>Alamat: Saguling, Batujajar,<br>West Bandung Regency, West Java,<br>Tercemar Sedang ": [-6.913526, 107.367661], // Saguling Dam
                "Titik Sungai: Bendungan Cirata<br>Alamat: Citamiang, Maniis,<br>Purwakarta Regency, West Java 41166,<br>Tercemar Berat": [-6.700203, 107.364963], // Cirata Dam
                "Titik Sungai: Bendungan Jatiluhur<br>Alamat: Kutamanah, Sukasari,<br>Purwakarta Regency, West Java 41116,<br>Tercemar Ringan": [-6.526997, 107.385456], // Jatiluhur Dam
                "Titik Sungai: Kabupaten Karawang<br>Alamat: Sungai Citarum, Telukjambe Timur,<br>Karawang, West Java 41361,<br>Memenuhi Baku Mutu": [-6.298185, 107.287757],  // Karawang Regency
                "Titik Sungai: Muara Gembong<br>Alamat: Kecamatan Muara Gembong,<br>Bekasi Regency, West Java,<br>Tercemar Ringan": [-5.984462, 107.043829], // Bekasi
                "Titik Sungai: Sungai Cikapundung<br>Alamat: Bandung City, West Java,<br>Tercemar Berat": [-6.898969, 107.606402],  // Bandung City
                "Titik Sungai: Dayeuhkolot<br>Alamat: Dayeuhkolot, Bandung, West Java,<br>Tercemar Sedang": [-6.990974, 107.626285]  // Dayeuhkolot
            };

            var map = L.map('map').setView([-6.8650, 107.4912], 10);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 18,
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
            }).addTo(map);

            Object.keys(locations).forEach(function(place) {
                var coord = locations[place];
                var marker = L.marker(coord).addTo(map);
                marker.bindPopup(place);
                marker.on('click', function() {
                    handleMarkerClick(marker, place);
                });
            });

            function handleMarkerClick(marker, place) {
                var info_paragraph = document.getElementById("marker_info");
                info_paragraph.innerHTML = place;
                var command = "place_clicked:" + place;
                Streamlit.setComponentValue(command);
            }
        </script>
        """
        st.components.v1.html(html_code, height=600)

        if st.session_state.get("clicked_marker"):
            place = st.session_state.get("clicked_marker").split(":")[1]
            st.write(place)

app()
