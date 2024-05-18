import streamlit as st

st.subheader('Jalur Sungai Citarum dengan Titik Pemantauan')

html_code = """
<div id="map" style="height: 600px; width: 100%;"></div>
<p id="marker_info" style="font-weight: bold;"></p>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.css" />
<script>
    var locations = {
        "Titik Sungai: Situ Cisanti<br>Alamat: Neglawangi, Kertasari,<br>Bandung Regency, West Java 40386,<br>Memenuhi Baku Mutu": [-7.208484677933202, 107.65792566573455],
        "Titik Sungai: Bendungan Saguling<br>Alamat: Saguling, Batujajar,<br>West Bandung Regency, West Java,<br>Tercemar Sedang ": [-6.913526, 107.367661],
        "Titik Sungai: Bendungan Cirata<br>Alamat: Citamiang, Maniis,<br>Purwakarta Regency, West Java 41166,<br>Tercemar Berat": [-6.700203, 107.364963],
        "Titik Sungai: Bendungan Jatiluhur<br>Alamat: Kutamanah, Sukasari,<br>Purwakarta Regency, West Java 41116,<br>Tercemar Ringan": [-6.526997, 107.385456],
        "Titik Sungai: Kabupaten Karawang<br>Alamat: Sungai Citarum, Telukjambe Timur,<br>Karawang, West Java 41361,<br>Memenuhi Baku Mutu": [-6.298185, 107.287757],
        "Titik Sungai: Muara Gembong<br>Alamat: Kecamatan Muara Gembong,<br>Bekasi Regency, West Java,<br>Tercemar Ringan": [-5.984462, 107.043829],
        "Titik Sungai: Sungai Cikapundung<br>Alamat: Bandung City, West Java,<br>Tercemar Berat": [-6.898969, 107.606402],
        "Titik Sungai: Dayeuhkolot<br>Alamat: Dayeuhkolot, Bandung, West Java,<br>Tercemar Sedang": [-6.990974, 107.626285]
    };

    var map = L.map('map').setView([-6.8650, 107.4912], 10);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
    }).addTo(map);

    function getIcon(color) {
        return new L.Icon({
            iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-${color}.png`,
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
            iconSize: [25, 41],
            shadowSize: [41, 41],
            iconAnchor: [12, 41],
            shadowAnchor: [12, 41],
            popupAnchor: [1, -34]
        });
    }

    var iconColors = {
        "Memenuhi Baku Mutu": 'green',
        "Tercemar Sedang": 'orange',
        "Tercemar Berat": 'red',
        "Tercemar Ringan": 'yellow'
    };

    Object.keys(locations).forEach(function(place) {
        var coord = locations[place];
        var condition = place.split('<br>')[3].trim();
        var color = iconColors[condition];
        var marker = L.marker(coord, {icon: getIcon(color)}).addTo(map);
        marker.bindPopup(place);
        marker.on('click', function() {
            handleMarkerClick(marker, place);
        });
    });

    // Koordinat lebih detail sepanjang jalur Sungai Citarum
    var citarumCoordinates = [
        [-7.208484677933202, 107.65792566573455],  // Situ Cisanti
        [-7.180543, 107.669803],
        [-7.144481, 107.670036],
        [-7.107647, 107.665094],
        [-7.071550, 107.661217],
        [-7.032015, 107.645695],
        [-7.000049, 107.629878],
        [-6.974688, 107.611886],
        [-6.937760, 107.585220],
        [-6.914947, 107.548237],
        [-6.890974, 107.520882],
        [-6.864636, 107.490248],
        [-6.834812, 107.465924],
        [-6.807319, 107.445586],
        [-6.780705, 107.423447],
        [-6.745477, 107.396274],
        [-6.713225, 107.370923],
        [-6.700203, 107.364963],  // Bendungan Cirata
        [-6.674034, 107.341447],
        [-6.656276, 107.316623],
        [-6.636122, 107.294516],
        [-6.616673, 107.269914],
        [-6.598573, 107.248473],
        [-6.570911, 107.222611],
        [-6.551058, 107.200838],
        [-6.526997, 107.385456],  // Bendungan Jatiluhur
        [-6.493438, 107.165310],
        [-6.465831, 107.137589],
        [-6.437194, 107.115047],
        [-6.412038, 107.089206],
        [-6.380760, 107.059692],
        [-6.345614, 107.034196],
        [-6.315520, 107.006517],
        [-6.298185, 107.287757],  // Kabupaten Karawang
        [-6.248835, 106.975352],
        [-6.208727, 106.957138],
        [-6.165341, 106.933406],
        [-6.125673, 106.913248],
        [-6.090349, 106.892899],
        [-6.043670, 106.872672],
        [-6.005684, 106.848943],
        [-5.984462, 107.043829]   // Muara Gembong
    ];

    // Debugging: Log koordinat ke console
    console.log('Koordinat Sungai Citarum:', citarumCoordinates);

    // Menggambar polyline sepanjang koordinat yang ditentukan
    var polyline = L.polyline(citarumCoordinates, {color: 'blue'}).addTo(map);

    // Debugging: Pastikan polyline ditambahkan ke peta
    if (polyline) {
        console.log('Polyline berhasil ditambahkan ke peta.');
    } else {
        console.log('Gagal menambahkan polyline ke peta.');
    }

    // Zoom the map to the polyline
    map.fitBounds(polyline.getBounds());

    function handleMarkerClick(marker, place) {
        var info_paragraph = document.getElementById("marker_info");
        info_paragraph.innerHTML = place;
        var command = "place_clicked:" + place;
        Streamlit.setComponentValue(command);
    }
</script>
"""

# Render peta dalam aplikasi Streamlit
st.components.v1.html(html_code, height=600)

if "clicked_marker" in st.session_state:
    place = st.session_state["clicked_marker"].split(":")[1]
    st.write(place)
