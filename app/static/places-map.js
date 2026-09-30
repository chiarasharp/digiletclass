/*
  places-map.js
  Initializes a Leaflet map showing geolocated places in the current filtered result set.
  Markers open the standard entity modal on click.
*/
(function() {
    var mapInitialized = false;

    window.initPlacesMap = function() {
        if (mapInitialized) return;
        mapInitialized = true;

        var container = document.getElementById('placesMap');
        if (!container || !window.mapItemsData || !window.L) return;

        var map = L.map('placesMap');
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 18
        }).addTo(map);

        var markers = [];
        window.mapItemsData.forEach(function(place) {
            if (!place.location || !place.location.geo) return;
            var parts = place.location.geo.split(',').map(function(s) { return parseFloat(s.trim()); });
            if (parts.length !== 2 || isNaN(parts[0]) || isNaN(parts[1])) return;
            var name = (place.place_names && place.place_names[0] && place.place_names[0].name) || place.id;
            var marker = L.marker([parts[0], parts[1]]).addTo(map);
            marker.bindPopup('<strong>' + name + '</strong><br><a href="#" data-entity-id="' + place.id + '">Vedi dettagli</a>');
            marker.on('popupopen', function() {
                var link = document.querySelector('.leaflet-popup-content a[data-entity-id="' + place.id + '"]');
                if (link) {
                    link.addEventListener('click', function(e) {
                        e.preventDefault();
                        fetchAndShowModal('places', place.id);
                    });
                }
            });
            markers.push(marker);
        });

        if (markers.length > 0) {
            var group = L.featureGroup(markers);
            map.fitBounds(group.getBounds().pad(0.1));
        } else {
            map.setView([41.9, 12.5], 5);
        }

        setTimeout(function() { map.invalidateSize(); }, 100);
    };
})();
