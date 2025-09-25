document.addEventListener('DOMContentLoaded', function() {
    // Modal configuration - add new modals here
    const modals = {
        main: {
            overlay: 'popupOverlay',
            openBtn: '[name="openModalBtn"]',
            closeBtn: 'closePopup'
        },
        billScan: {
            overlay: 'popupOverlayBillScan',
            openBtn: '[name="scan-bill"]',
            closeBtn: 'closePopupBillScan'
        },
        ia: {
            overlay: 'popupOverlayIA',
            openBtn: '[name="go-ia"]',
            closeBtn: 'closePopupIA' // Fixed: Now uses unique ID
        }
    };

    // Store references to DOM elements
    const elements = {};
    
    // Initialize modal elements
    Object.keys(modals).forEach(key => {
        const modal = modals[key];
        elements[key] = {
            overlay: document.getElementById(modal.overlay),
            openBtn: modal.openBtn.startsWith('a[') || modal.openBtn.includes('[') 
                ? document.querySelectorAll(modal.openBtn)
                : document.getElementById(modal.openBtn),
            closeBtn: document.getElementById(modal.closeBtn)
        };
    });

    // Generic modal functions
    function openModal(modalKey) {
        const modal = elements[modalKey];
        if (modal && modal.overlay) {
            // Close all other modals first
            closeAllModals();
            
            modal.overlay.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }
    }

    function closeModal(modalKey) {
        const modal = elements[modalKey];
        if (modal && modal.overlay) {
            modal.overlay.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    }

    function closeAllModals() {
        Object.keys(elements).forEach(key => {
            const modal = elements[key];
            if (modal && modal.overlay) {
                modal.overlay.style.display = 'none';
            }
        });
        document.body.style.overflow = 'auto';
    }

    function isModalOpen(modalKey) {
        const modal = elements[modalKey];
        return modal && modal.overlay && modal.overlay.style.display === 'flex';
    }

    // Set up event listeners for each modal
    Object.keys(modals).forEach(key => {
        const modal = elements[key];
        
        // Open button event listener
        if (modal.openBtn) {
            modal.openBtn.forEach(btn => {
                btn.addEventListener('click', function(e) {
                    e.preventDefault();
                    openModal(key);
                });
            });
        }

        // Close button event listener
        if (modal.closeBtn) {
            modal.closeBtn.addEventListener('click', function(e) {
                e.preventDefault();
                closeModal(key);
            });
        }

        // Close on overlay click
        if (modal.overlay) {
            modal.overlay.addEventListener('click', function(event) {
                if (event.target === modal.overlay) {
                    closeModal(key);
                }
            });
        }
    });

    // Close on Escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            // Find and close the currently open modal
            Object.keys(elements).forEach(key => {
                if (isModalOpen(key)) {
                    closeModal(key);
                }
            });
        }
    });

    // Public API (optional - for external access)
    window.ModalSystem = {
        open: openModal,
        close: closeModal,
        closeAll: closeAllModals,
        isOpen: isModalOpen
    };

    const select = document.getElementById('expense-category-select');
    const inputNew = document.getElementById('newCategoryInput');

    if (!select || !inputNew) return;

    function toggleNewCategory() {
        if (select.value === 'new-category') {
            inputNew.style.display = 'block';
            inputNew.focus();
        } else {
            inputNew.style.display = 'none';
            inputNew.value = '';
        }
    }

    // inicial
    toggleNewCategory();

    // al cambiar selección
    select.addEventListener('change', toggleNewCategory);
});


const menuItems = document.querySelectorAll('.menu-item');

menuItems.forEach(item => {
    item.addEventListener('click', function(e) {
        // Remover la clase active de todos los elementos
        menuItems.forEach(mi => {
            mi.classList.remove('active', 'ripple');
        });

        // Agregar la clase active al elemento clickeado
        this.classList.add('active');
        
        // Efecto de onda
        this.classList.add('ripple');
        setTimeout(() => {
            this.classList.remove('ripple');
        }, 300);

        // Log para mostrar qué opción se seleccionó
        console.log(`Opción seleccionada: ${this.dataset.option}`);
    });

    // Efecto hover mejorado
    item.addEventListener('mouseenter', function() {
        if (!this.classList.contains('active')) {
            this.style.background = 'rgba(0, 0, 0, 0.05)';
        }
    });

    item.addEventListener('mouseleave', function() {
        if (!this.classList.contains('active')) {
            this.style.background = 'transparent';
        }
    });
});

// Seleccionar la primera opción por defecto
if (menuItems.length > 0) {
    menuItems[0].classList.add('active');
}