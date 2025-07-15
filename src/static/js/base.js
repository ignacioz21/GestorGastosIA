 document.addEventListener('DOMContentLoaded', function() {
    // FIXED: Get elements by ID instead of name
    const openBtn = document.getElementById('openModalBtn');
    const closeBtn = document.getElementById('closePopup');
    const popupOverlay = document.getElementById('popupOverlay');

    function openPopup() {
        popupOverlay.style.display = 'flex'; // FIXED: Use flex instead of block
        document.body.style.overflow = 'hidden';
    }

    function closePopup() {
        popupOverlay.style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    // FIXED: Add event listeners properly
    if (openBtn) {
        openBtn.addEventListener('click', function(e) {
            e.preventDefault();
            openPopup();
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            closePopup();
        });
    }

    // Close on overlay click
    if (popupOverlay) {
        popupOverlay.addEventListener('click', function(event) {
            if (event.target === popupOverlay) {
                closePopup();
            }
        });
    }

    // FIXED: Corrected typo (was "documenet")
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && popupOverlay.style.display === 'flex') {
            closePopup();
        }
    });
});