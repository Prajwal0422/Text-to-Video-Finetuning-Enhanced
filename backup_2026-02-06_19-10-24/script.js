// ===================================
// AETHER-GEN INTERACTIVE LOGIC
// ===================================

document.addEventListener('DOMContentLoaded', () => {
    // Smooth Scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
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

    // Navbar Effect
    const navbar = document.querySelector('.glass-nav');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.style.borderBottomColor = 'rgba(255, 255, 255, 0.15)';
            navbar.style.background = 'rgba(3, 3, 5, 0.9)';
        } else {
            navbar.style.borderBottomColor = 'rgba(255, 255, 255, 0.05)';
            navbar.style.background = 'rgba(3, 3, 5, 0.7)';
        }
    });

    // Reveal Animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal-active');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.arch-card, .features-split').forEach(el => {
        observer.observe(el);
    });
});
