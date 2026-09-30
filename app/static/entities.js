/*
  entities.js
  Main JavaScript for DigiLetClass entity UI logic.
  - Handles modal loading and display for entities
  - Initializes Bootstrap tooltips
  - Handles card click events to open modals
  - Toggles between card and table views
  - Handles details button logic in tables
*/
function fetchAndShowModal(entityType, entityId) {
    if (!entityType || !entityId) return;
    // Show spinner while loading
    document.getElementById('entityModalBody').innerHTML = '<div class="d-flex justify-content-center align-items-center" style="height:150px;"><div class="spinner-border text-primary" role="status" aria-label="Caricamento..."><span class="visually-hidden">Caricamento...</span></div></div>';
    fetch(`/modal/${entityType}/${entityId}`)
        .then(response => {
            if (!response.ok) throw new Error('Not found');
            return response.text();
        })
        .then(html => {
            document.getElementById('entityModalBody').innerHTML = html;
            var modal = new bootstrap.Modal(document.getElementById('entityModal'));
            modal.show();
        })
        .catch((err) => {
            console.error(err);
            document.getElementById('entityModalBody').innerHTML = '<div class="text-danger">Errore nel caricamento dei dettagli.</div>';
        });
}

document.addEventListener('DOMContentLoaded', function() {
    // Tooltip initialization
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Attach click listeners to entity cards
    var cards = document.querySelectorAll('.card[data-entity-id]');
    cards.forEach(function(card) {
        card.addEventListener('click', function(e) {
            // Prevent badge links from triggering the modal
            if (e.target.tagName === 'A' && e.target.classList.contains('badge')) {
                return;
            }
            var entityId = card.getAttribute('data-entity-id');
            var entityType = card.getAttribute('data-entity-type');
            fetchAndShowModal(entityType, entityId);
        });
    });

    // View toggle logic (list / card / map)
    var viewButtons = [
        { btn: document.getElementById('btnViewList'), view: document.getElementById('entityListView') },
        { btn: document.getElementById('btnViewCard'), view: document.getElementById('entityCardView') },
        { btn: document.getElementById('btnViewMap'), view: document.getElementById('entityMapView') }
    ].filter(function(entry) { return entry.btn && entry.view; });

    viewButtons.forEach(function(entry) {
        entry.btn.addEventListener('click', function() {
            viewButtons.forEach(function(other) {
                other.view.style.display = other === entry ? '' : 'none';
                other.btn.classList.toggle('active', other === entry);
            });
            if (entry.btn.id === 'btnViewMap' && window.initPlacesMap) {
                window.initPlacesMap();
            }
        });
    });

    // Click on table rows opens modal
    var tableRows = document.querySelectorAll('#entityListView tbody tr[data-entity-id]');
    tableRows.forEach(function(row) {
        row.addEventListener('click', function(e) {
            if (e.target.tagName === 'A') return;
            fetchAndShowModal(row.getAttribute('data-entity-type'), row.getAttribute('data-entity-id'));
        });
    });
});