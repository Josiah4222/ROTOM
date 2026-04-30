document.addEventListener('DOMContentLoaded', function () {
    // Gallery lightbox
    const galleryModal = document.getElementById('gallery-modal');
    const galleryItems = document.querySelectorAll('.gallery-item');
    const modalImage = document.getElementById('modal-image');
    const closeButtons = document.querySelectorAll('.modal-close');

    if (galleryModal && modalImage) {
        galleryItems.forEach(item => {
            item.addEventListener('click', () => {
                const img = item.querySelector('.gallery-image');
                if (img) {
                    modalImage.src = img.src;
                    galleryModal.classList.add('open');
                    document.body.style.overflow = 'hidden';
                }
            });
        });

        closeButtons.forEach(button => {
            button.addEventListener('click', () => {
                galleryModal.classList.remove('open');
                document.body.style.overflow = '';
            });
        });

        galleryModal.addEventListener('click', (e) => {
            if (e.target === galleryModal) {
                galleryModal.classList.remove('open');
                document.body.style.overflow = '';
            }
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                galleryModal.classList.remove('open');
                document.body.style.overflow = '';
            }
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            const target = document.querySelector(targetId);
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Form submission handling (if any)
    document.querySelectorAll('.booking-form').forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            alert('Thank you for your interest! We will contact you shortly.');
        });
    });
});
