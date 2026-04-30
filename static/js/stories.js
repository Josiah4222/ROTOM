function openLightbox(el) {
    const img = el.querySelector('img');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightbox = document.getElementById('lightbox');
    if (lightboxImg && img) lightboxImg.src = img.src;
    if (lightbox) lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    const lightbox = document.getElementById('lightbox');
    if (lightbox) lightbox.classList.remove('active');
    document.body.style.overflow = '';
}

document.addEventListener('DOMContentLoaded', function () {
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeLightbox(); });

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.story').forEach(s => {
        s.style.opacity = '0';
        s.style.transform = 'translateY(40px)';
        s.style.transition = 'all 0.7s ease-out';
        observer.observe(s);
    });
});
