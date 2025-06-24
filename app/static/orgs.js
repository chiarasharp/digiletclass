function filterOrgs() {
    var input = document.getElementById('searchInput');
    var filter = input.value.toLowerCase();
    var cards = document.getElementsByClassName('org-card');
    Array.from(cards).forEach(function(card) {
        var text = card.textContent.toLowerCase();
        if (text.indexOf(filter) > -1) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
    // Also filter table rows if table view is visible
    var table = document.getElementById('orgsTableView');
    if (table && table.style.display !== 'none') {
        var rows = table.querySelectorAll('tbody tr');
        rows.forEach(function(row) {
            var text = row.textContent.toLowerCase();
            if (text.indexOf(filter) > -1) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }
}

// Fetch and display modal content from Flask endpoint
function fetchAndShowOrgModal(orgId) {
    fetch(`/org/${orgId}/modal`)
        .then(response => {
            if (!response.ok) throw new Error('Not found');
            return response.text();
        })
        .then(html => {
            document.getElementById('orgModalBody').innerHTML = html;
            var modal = new bootstrap.Modal(document.getElementById('orgModal'));
            modal.show();
        })
        .catch(() => {
            document.getElementById('orgModalBody').innerHTML = '<div class="text-danger">Errore nel caricamento dei dettagli.</div>';
        });
}

document.addEventListener('DOMContentLoaded', function() {
    // Attach click listeners to org cards
    var cards = document.getElementsByClassName('org-card');
    Array.from(cards).forEach(function(card) {
        card.addEventListener('click', function(e) {
            // Prevent badge links from triggering the modal
            if (e.target.tagName === 'A' && e.target.classList.contains('badge')) {
                return;
            }
            var idx = card.getAttribute('data-org-index');
            var org = window.orgsData[idx];
            fetchAndShowOrgModal(org.id);
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
            var org = window.orgsData[idx];
            fetchAndShowOrgModal(org.id);
        });
    });
}); 