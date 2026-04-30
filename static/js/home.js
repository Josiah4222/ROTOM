document.addEventListener('DOMContentLoaded', function() {
    // Counter Animation
    let valueDisplays = document.querySelectorAll(".num");
    let interval = 4000;

    valueDisplays.forEach((valueDisplay) => {
        let startValue = 0;
        let originalText = valueDisplay.textContent;
        let hasPlus = originalText.includes('+');
        let endValue = parseInt(valueDisplay.getAttribute("data-val")) || 0;
        if (endValue === 0) return;
        
        let duration = Math.floor(interval / endValue);
        let counter = setInterval(function () {
            startValue += Math.ceil(endValue / (interval / duration));
            valueDisplay.textContent = startValue;
            if (startValue >= endValue) {
                valueDisplay.textContent = endValue + (hasPlus ? '+' : '');
                clearInterval(counter);
            }
        }, duration);
    });

    // Testimonial Slider
    const testimonialContainer = document.querySelector('.testimonial-container');
    const testimonials = document.querySelectorAll('.testimonial');
    const prevButton = document.querySelector('.control-prev');
    const nextButton = document.querySelector('.control-next');
    let currentIndex = 0;
    const totalTestimonials = testimonials.length;

    if (testimonialContainer && testimonials.length > 0) {
        function updateTestimonial() {
            testimonialContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
            testimonials.forEach((testimonial, index) => {
                testimonial.classList.toggle('active', index === currentIndex);
            });
        }

        if (nextButton) {
            nextButton.addEventListener('click', () => {
                currentIndex = (currentIndex + 1) % totalTestimonials;
                updateTestimonial();
            });
        }

        if (prevButton) {
            prevButton.addEventListener('click', () => {
                currentIndex = (currentIndex - 1 + totalTestimonials) % totalTestimonials;
                updateTestimonial();
            });
        }

        setInterval(() => {
            currentIndex = (currentIndex + 1) % totalTestimonials;
            updateTestimonial();
        }, 17000);
    }

    // Contact Form Submission
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const form = this;
            const emailInput = document.getElementById('id_email');
            const phoneInput = document.getElementById('id_phone_number');
            const email = emailInput ? emailInput.value : '';
            const phone = phoneInput ? phoneInput.value : '';
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            const messagesDiv = document.getElementById('form-messages');

            // Clear previous messages
            if (messagesDiv) messagesDiv.innerHTML = '';

            // Client-side validation
            if (!emailRegex.test(email)) {
                showFormError('Please enter a valid email address.');
                return;
            }

            if (phone && (!phone.match(/^\d{10}$/) || (!phone.startsWith('09') && !phone.startsWith('07')))) {
                showFormError('Phone number, if provided, must be 10 digits starting with 09 or 07.');
                return;
            }

            // Submit form via AJAX
            const data = new FormData(form);
            fetch(form.action, {
                method: 'POST',
                body: data,
                headers: {
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    showFormError('Thank you for your message! We will get back to you soon.', 'success');
                    form.reset();
                } else {
                    showFormError('There was an error with your submission. Please check the form.');
                    if (data.errors) {
                        Object.entries(data.errors).forEach(([field, errors]) => {
                            const input = document.querySelector(`#id_${field}`);
                            if (input) {
                                const fieldErrors = document.createElement('div');
                                fieldErrors.className = 'errorlist';
                                fieldErrors.innerHTML = errors.join('<br>');
                                input.after(fieldErrors);
                            }
                        });
                    }
                }
            })
            .catch(error => {
                console.error('Form submission error:', error);
                showFormError('An error occurred. Please try again.');
            });
        });
    }

    function showFormError(message, type = 'error') {
        const messagesDiv = document.getElementById('form-messages');
        if (!messagesDiv) return;
        const errorDiv = document.createElement('div');
        errorDiv.className = `alert ${type}`;
        errorDiv.textContent = message;
        messagesDiv.appendChild(errorDiv);
        setTimeout(() => errorDiv.remove(), 5000);
    }
});

function openTestimonialLightbox(url) {
    const lb = document.getElementById('testimonialLightbox');
    document.getElementById('testimonialLightboxImg').src = url;
    lb.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function closeTestimonialLightbox() {
    document.getElementById('testimonialLightbox').style.display = 'none';
    document.body.style.overflow = '';
}

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeTestimonialLightbox();
});
