document.addEventListener('DOMContentLoaded', function () {
    // Number counter animation
    const numbers = document.querySelectorAll('.dashboard-number');
    const observerOptions = {
        threshold: 0.5
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const targetNumber = parseInt(target.getAttribute('data-target'));
                animateNumber(target, targetNumber);
                observer.unobserve(target);
            }
        });
    }, observerOptions);

    numbers.forEach(number => {
        observer.observe(number);
    });

    function animateNumber(element, target) {
        let current = 0;
        const duration = 2000;
        const stepTime = Math.abs(Math.floor(duration / target));

        const timer = setInterval(() => {
            current += 1;
            element.innerText = current;
            if (current >= target) {
                clearInterval(timer);
                element.innerText = target;
            }
        }, stepTime);
    }
});
