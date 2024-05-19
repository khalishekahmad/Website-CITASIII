import streamlit as st

st.subheader('Jalur Sungai Citarum dengan Titik Pemantauan')

html_code = """
<div id="map" style="height: 600px; width: 100%;"></div>
<p id="marker_info" style="font-weight: bold;"></p>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.css" />
<script>
    var locations = {
        "Titik Sungai: Situ Cisanti<br>Alamat: Neglawangi, Kertasari,<br>Bandung Regency, West Java 40386,<br>Memenuhi Baku Mutu": [-7.20848, 107.65793],
        "Titik Sungai: Bendungan Saguling<br>Alamat: Saguling, Batujajar,<br>West Bandung Regency, West Java,<br>Tercemar Sedang": [-6.91353, 107.36766],
        "Titik Sungai: Bendungan Cirata<br>Alamat: Citamiang, Maniis,<br>Purwakarta Regency, West Java 41166,<br>Tercemar Berat": [-6.70020, 107.36496],
        "Titik Sungai: Bendungan Jatiluhur<br>Alamat: Kutamanah, Sukasari,<br>Purwakarta Regency, West Java 41116,<br>Tercemar Ringan": [-6.52699, 107.38545],
        "Titik Sungai: Kabupaten Karawang<br>Alamat: Sungai Citarum, Telukjambe Timur,<br>Karawang, West Java 41361,<br>Memenuhi Baku Mutu": [-6.29818, 107.28775],
        "Titik Sungai: Muara Gembong<br>Alamat: Kecamatan Muara Gembong,<br>Bekasi Regency, West Java,<br>Tercemar Ringan": [-5.98446, 107.04382],
        "Titik Sungai: Sungai Cikapundung<br>Alamat: Bandung City, West Java,<br>Tercemar Berat": [-6.89896, 107.60640],
        "Titik Sungai: Dayeuhkolot<br>Alamat: Dayeuhkolot, Bandung, West Java,<br>Tercemar Sedang": [-6.99097, 107.62628]
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
        [-7.20848, 107.65793],  // Situ Cisanti
        [-7.18054, 107.66980],
        [-7.14448, 107.67003],
        [-7.10764, 107.66509],
        [-7.07155, 107.66121],
        [-7.03201, 107.64569],
        [-7.00004, 107.62987],
        [-6.97468, 107.61188],
        [-6.93776, 107.58522],
        [-6.91494, 107.54823],
        [-6.89097, 107.52088],
        [-6.86463, 107.49024],
        [-6.83481, 107.46592],
        [-6.80731, 107.44558],
        [-6.78070, 107.42344],
        [-6.74547, 107.39627],
        [-6.71322, 107.37092],
        [-6.70020, 107.36496],  // Bendungan Cirata
        [-6.67403, 107.34144],
        [-6.65627, 107.31662],
        [-6.63612, 107.29451],
        [-6.61667, 107.26991],
        [-6.59857, 107.24847],
        [-6.57091, 107.22261],
        [-6.55105, 107.20083],
        [-6.52699, 107.38545],  // Bendungan Jatiluhur
        [-6.49343, 107.16531],
        [-6.46583, 107.13758],
        [-6.43719, 107.11504],
        [-6.41203, 107.08920],
        [-6.38076, 107.05969],
        [-6.34561, 107.03419],
        [-6.31552, 107.00651],
        [-6.29818, 107.28775],  // Kabupaten Karawang
        [-6.24883, 106.97535],
        [-6.20872, 106.95713],
        [-6.16534, 106.93340],
        [-6.12567, 106.91324],
        [-6.09034, 106.89289],
        [-6.04367, 106.87267],
        [-6.00568, 106.84894],
        [-5.98446, 107.04382]   // Muara Gembong
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
