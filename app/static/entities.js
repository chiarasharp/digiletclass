function fetchAndShowModal(entityType, entityId) {
    if (!entityType || !entityId) return;
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

    // View toggle logic
    var toggleBtn = document.getElementById('toggleViewBtn');
    var cardView = document.getElementById('orgsCardView');
    var tableView = document.getElementById('orgsTableView');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            if (cardView.style.display === 'none') {
                cardView.style.display = '';
                tableView.style.display = 'none';
                toggleBtn.textContent = 'Vista Tabella';
            } else {
                cardView.style.display = 'none';
                tableView.style.display = '';
                toggleBtn.textContent = 'Vista Card';
            }
        });
    }

    // Attach click listeners to table details buttons
    var detailsBtns = document.querySelectorAll('#orgsTableView .details-btn');
    detailsBtns.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            var row = btn.closest('tr');
            var idx = row.getAttribute('data-org-index');
            var org = window.sData[idx];
            fetchAndShowModal('org', org.id);
        });
    });
}); 