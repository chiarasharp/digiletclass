// Sidebar navigation - Reusable for any page with sidebar TOC

document.addEventListener('DOMContentLoaded', function() {
    // Trova tutte le sidebar TOC (sia .methodology-toc che .project-toc)
    const tocContainers = document.querySelectorAll('.methodology-toc, .project-toc');

    tocContainers.forEach(tocContainer => {
        const tocLinks = tocContainer.querySelectorAll('a');

        // Smooth scrolling per i link dell'indice
        tocLinks.forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Raccogli tutte le sezioni linkate
        const sections = [];
        tocLinks.forEach(link => {
            const href = link.getAttribute('href');
            const id = href.substring(1); // rimuovi il #
            if (document.getElementById(id)) {
                sections.push({ id: id, href: href });
            }
        });

        // Evidenzia la sezione corrente durante lo scroll
        function updateActiveSection() {
            const scrollPosition = window.scrollY + 150;

            // Trova la sezione corrente
            let currentSection = sections[0];
            for (let i = sections.length - 1; i >= 0; i--) {
                const section = document.getElementById(sections[i].id);
                if (section && section.offsetTop <= scrollPosition) {
                    currentSection = sections[i];
                    break;
                }
            }

            // Rimuovi 'active' da tutti i link e aggiungilo al link corrente
            tocLinks.forEach(link => {
                if (link.getAttribute('href') === currentSection.href) {
                    link.classList.add('active');
                } else {
                    link.classList.remove('active');
                }
            });
        }

        // Aggiorna all'inizio e durante lo scroll
        if (sections.length > 0) {
            updateActiveSection();
            window.addEventListener('scroll', updateActiveSection);
        }
    });
});
