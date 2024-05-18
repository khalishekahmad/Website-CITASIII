import streamlit as st

def app():
    st.write('Metode')
    st.title('Titik Peta Sungai :blue[Citarum]')

    # Informasi untuk setiap kotak dengan ukuran yang diinginkan
    boxes_info = [
        {"title": "Memenuhi Baku Mutu", "color": "#6DC5D1", "width": "50px", "height": "50px"},
        {"title": "Tercemar Ringan", "color": "#7ABA78", "width": "50px", "height": "50px"},
        {"title": "Tercemar Sedang", "color": "#FEB941", "width": "50px", "height": "50px"},
        {"title": "Tercemar Berat", "color": "#C40C0C", "width": "50px", "height": "50px"}
    ]

    # Membuat empat kolom
    col1, col2, col3, col4 = st.columns(4)

    # Menampilkan setiap kotak di dalam kolom yang berbeda
    with col1:
        box = boxes_info[0]
        st.write(box["title"])
        st.markdown(f'<div style="width: {box["width"]}; height: {box["height"]}; background-color: {box["color"]};"></div>', unsafe_allow_html=True)

    with col2:
        box = boxes_info[1]
        st.write(box["title"])
        st.markdown(f'<div style="width: {box["width"]}; height: {box["height"]}; background-color: {box["color"]};"></div>', unsafe_allow_html=True)

    with col3:
        box = boxes_info[2]
        st.write(box["title"])
        st.markdown(f'<div style="width: {box["width"]}; height: {box["height"]}; background-color: {box["color"]};"></div>', unsafe_allow_html=True)

    with col4:
        box = boxes_info[3]
        st.write(box["title"])
        st.markdown(f'<div style="width: {box["width"]}; height: {box["height"]}; background-color: {box["color"]};"></div>', unsafe_allow_html=True)


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

            function getGreenIcon() {
                return new L.Icon({
                    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
                    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                    iconSize: [25, 41],
                    shadowSize: [41, 41],
                    iconAnchor: [12, 41],
                    shadowAnchor: [12, 41],
                    popupAnchor: [1, -34]
                });
            }

            function getOrangeIcon() {
                return new L.Icon({
                    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-orange.png',
                    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                    iconSize: [25, 41],
                    shadowSize: [41, 41],
                    iconAnchor: [12, 41],
                    shadowAnchor: [12, 41],
                    popupAnchor: [1, -34]
                });
            }

            function getRedIcon() {
                return new L.Icon({
                    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
                    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                    iconSize: [25, 41],
                    shadowSize: [41, 41],
                    iconAnchor: [12, 41],
                    shadowAnchor: [12, 41],
                    popupAnchor: [1, -34]
                });
            }

            function getBlueIcon() {
                return new L.Icon({
                    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png',
                    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                    iconSize: [25, 41],
                    shadowSize: [41, 41],
                    iconAnchor: [12, 41],
                    shadowAnchor: [12, 41],
                    popupAnchor: [1, -34]
                });
            }

            Object.keys(locations).forEach(function(place) {
                var coord = locations[place];
                var condition = place.split('<br>')[3].trim(); // Extracting and trimming condition from place description
                var marker;

                if (condition === 'Tercemar Ringan') {
                    marker = L.marker(coord, {icon: getGreenIcon()}).addTo(map);
                } else if (condition === 'Tercemar Sedang') {
                    marker = L.marker(coord, {icon: getOrangeIcon()}).addTo(map);
                } else if (condition === 'Tercemar Berat') {
                    marker = L.marker(coord, {icon: getRedIcon()}).addTo(map);
                } else if (condition === 'Memenuhi Baku Mutu') {
                    marker = L.marker(coord, {icon: getBlueIcon()}).addTo(map);
                }

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

        if "clicked_marker" in st.session_state:
            place = st.session_state["clicked_marker"].split(":")[1]
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
                "Titik Sungai: Bendungan Saguling<br>Alamat: Saguling, Batujajar,<br>West Bandung Regency, West Java,<br>Tercemar Berat ": [-6.913526, 107.367661], // Saguling Dam
                "Titik Sungai: Bendungan Cirata<br>Alamat: Citamiang, Maniis,<br>Purwakarta Regency, West Java 41166,<br>Tercemar Berat": [-6.700203, 107.364963], // Cirata Dam
                "Titik Sungai: Bendungan Jatiluhur<br>Alamat: Kutamanah, Sukasari,<br>Purwakarta Regency, West Java 41116,<br>Memenuhi Baku Mutu": [-6.526997, 107.385456], // Jatiluhur Dam
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

            function getGreenIcon() {
                return new L.Icon({
                    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
                    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                    iconSize: [25, 41],
                    shadowSize: [41, 41],
                    iconAnchor: [12, 41],
                    shadowAnchor: [12, 41],
                    popupAnchor: [1, -34]
                });
            }

            function getOrangeIcon() {
                return new L.Icon({
                    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-orange.png',
                    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                    iconSize: [25, 41],
                    shadowSize: [41, 41],
                    iconAnchor: [12, 41],
                    shadowAnchor: [12, 41],
                    popupAnchor: [1, -34]
                });
            }

            function getRedIcon() {
                return new L.Icon({
                    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
                    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                    iconSize: [25, 41],
                    shadowSize: [41, 41],
                    iconAnchor: [12, 41],
                    shadowAnchor: [12, 41],
                    popupAnchor: [1, -34]
                });
            }

            function getBlueIcon() {
                return new L.Icon({
                    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png',
                    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                    iconSize: [25, 41],
                    shadowSize: [41, 41],
                    iconAnchor: [12, 41],
                    shadowAnchor: [12, 41],
                    popupAnchor: [1, -34]
                });
            }

            Object.keys(locations).forEach(function(place) {
                var coord = locations[place];
                var condition = place.split('<br>')[3].trim(); // Extracting and trimming condition from place description
                var marker;

                if (condition === 'Tercemar Ringan') {
                    marker = L.marker(coord, {icon: getGreenIcon()}).addTo(map);
                } else if (condition === 'Tercemar Sedang') {
                    marker = L.marker(coord, {icon: getOrangeIcon()}).addTo(map);
                } else if (condition === 'Tercemar Berat') {
                    marker = L.marker(coord, {icon: getRedIcon()}).addTo(map);
                } else if (condition === 'Memenuhi Baku Mutu') {
                    marker = L.marker(coord, {icon: getBlueIcon()}).addTo(map);
                }

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

        if "clicked_marker" in st.session_state:
            place = st.session_state["clicked_marker"].split(":")[1]
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
                "Titik Sungai: Situ Cisanti<br>Alamat: Neglawangi, Kertasari,<br>Bandung Regency, West Java 40386,<br>Tercemar Berat": [-7.208484677933202, 107.65792566573455],  // Source of the Citarum River
                "Titik Sungai: Bendungan Saguling<br>Alamat: Saguling, Batujajar,<br>West Bandung Regency, West Java,<br>Tercemar Sedang": [-6.913526, 107.367661], // Saguling Dam
                "Titik Sungai: Bendungan Cirata<br>Alamat: Citamiang, Maniis,<br>Purwakarta Regency, West Java 41166,<br>Tercemar Berat": [-6.700203, 107.364963], // Cirata Dam
                "Titik Sungai: Bendungan Jatiluhur<br>Alamat: Kutamanah, Sukasari,<br>Purwakarta Regency, West Java 41116,<br>Tercemar Ringan": [-6.526997, 107.385456], // Jatiluhur Dam
                "Titik Sungai: Kabupaten Karawang<br>Alamat: Sungai Citarum, Telukjambe Timur,<br>Karawang, West Java 41361,<br>Memenuhi Baku Mutu": [-6.298185, 107.287757],  // Karawang Regency
                "Titik Sungai: Muara Gembong<br>Alamat: Kecamatan Muara Gembong,<br>Bekasi Regency, West Java,<br>Tercemar Ringan": [-5.984462, 107.043829], // Bekasi
                "Titik Sungai: Sungai Cikapundung<br>Alamat: Bandung City, West Java,<br>Tercemar Sedang": [-6.898969, 107.606402],  // Bandung City
                "Titik Sungai: Dayeuhkolot<br>Alamat: Dayeuhkolot, Bandung, West Java,<br>Tercemar Sedang": [-6.990974, 107.626285]  // Dayeuhkolot
            };

            var map = L.map('map').setView([-6.8650, 107.4912], 10);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 18,
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
            }).addTo(map);

            function getGreenIcon() {
                return new L.Icon({
                    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
                    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                    iconSize: [25, 41],
                    shadowSize: [41, 41],
                    iconAnchor: [12, 41],
                    shadowAnchor: [12, 41],
                    popupAnchor: [1, -34]
                });
            }

            function getOrangeIcon() {
                return new L.Icon({
                    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-orange.png',
                    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                    iconSize: [25, 41],
                    shadowSize: [41, 41],
                    iconAnchor: [12, 41],
                    shadowAnchor: [12, 41],
                    popupAnchor: [1, -34]
                });
            }

            function getRedIcon() {
                return new L.Icon({
                    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
                    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                    iconSize: [25, 41],
                    shadowSize: [41, 41],
                    iconAnchor: [12, 41],
                    shadowAnchor: [12, 41],
                    popupAnchor: [1, -34]
                });
            }

            function getBlueIcon() {
                return new L.Icon({
                    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png',
                    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                    iconSize: [25, 41],
                    shadowSize: [41, 41],
                    iconAnchor: [12, 41],
                    shadowAnchor: [12, 41],
                    popupAnchor: [1, -34]
                });
            }

            Object.keys(locations).forEach(function(place) {
                var coord = locations[place];
                var condition = place.split('<br>')[3].trim(); // Extracting and trimming condition from place description
                var marker;

                if (condition === 'Tercemar Ringan') {
                    marker = L.marker(coord, {icon: getGreenIcon()}).addTo(map);
                } else if (condition === 'Tercemar Sedang') {
                    marker = L.marker(coord, {icon: getOrangeIcon()}).addTo(map);
                } else if (condition === 'Tercemar Berat') {
                    marker = L.marker(coord, {icon: getRedIcon()}).addTo(map);
                } else if (condition === 'Memenuhi Baku Mutu') {
                    marker = L.marker(coord, {icon: getBlueIcon()}).addTo(map);
                }

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

        if "clicked_marker" in st.session_state:
            place = st.session_state["clicked_marker"].split(":")[1]
            st.write(place)

app()
