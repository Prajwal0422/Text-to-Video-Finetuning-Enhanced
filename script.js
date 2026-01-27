// ===================================
// SMOOTH SCROLLING
// ===================================
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

// ===================================
// NAVBAR SCROLL EFFECT
// ===================================
const navbar = document.querySelector('.navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    // Add shadow on scroll
    if (currentScroll > 50) {
        navbar.style.boxShadow = '0 4px 16px rgba(0, 0, 0, 0.3)';
    } else {
        navbar.style.boxShadow = 'none';
    }
    
    lastScroll = currentScroll;
});

// ===================================
// INTERSECTION OBSERVER FOR ANIMATIONS
// ===================================
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all cards and sections
const animatedElements = document.querySelectorAll(
    '.about-card, .feature-card, .pipeline-stage, .workflow-step, .result-card, .metric-card, .tech-category, .ack-card'
);

animatedElements.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// ===================================
// MOBILE MENU TOGGLE
// ===================================
const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
const navLinks = document.querySelector('.nav-links');

if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        mobileMenuToggle.classList.toggle('active');
    });
}

// ===================================
// PIPELINE STAGE HOVER EFFECT
// ===================================
const pipelineStages = document.querySelectorAll('.pipeline-stage');

pipelineStages.forEach((stage, index) => {
    stage.addEventListener('mouseenter', () => {
        pipelineStages.forEach((s, i) => {
            if (i !== index) {
                s.style.opacity = '0.5';
            }
        });
    });
    
    stage.addEventListener('mouseleave', () => {
        pipelineStages.forEach(s => {
            s.style.opacity = '1';
        });
    });
});

// ===================================
// GRADIENT ORB MOUSE FOLLOW
// ===================================
const orbs = document.querySelectorAll('.gradient-orb');
let mouseX = 0;
let mouseY = 0;

document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
});

function animateOrbs() {
    orbs.forEach((orb, index) => {
        const speed = (index + 1) * 0.02;
        const x = (mouseX - window.innerWidth / 2) * speed;
        const y = (mouseY - window.innerHeight / 2) * speed;
        
        orb.style.transform = `translate(${x}px, ${y}px)`;
    });
    
    requestAnimationFrame(animateOrbs);
}

animateOrbs();

// ===================================
// COPY CODE SNIPPET ON CLICK
// ===================================
const codeSnippets = document.querySelectorAll('.code-snippet code');

codeSnippets.forEach(code => {
    code.style.cursor = 'pointer';
    code.title = 'Click to copy';
    
    code.addEventListener('click', () => {
        const text = code.textContent;
        navigator.clipboard.writeText(text).then(() => {
            // Visual feedback
            const originalText = code.textContent;
            code.textContent = '✓ Copied!';
            code.style.color = '#10b981';
            
            setTimeout(() => {
                code.textContent = originalText;
                code.style.color = '';
            }, 2000);
        });
    });
});

// ===================================
// PERFORMANCE METRICS COUNTER ANIMATION
// ===================================
function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

// Observe metric cards for counter animation
const metricObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting && !entry.target.dataset.animated) {
            entry.target.dataset.animated = 'true';
            const valueElement = entry.target.querySelector('.metric-value');
            const value = valueElement.textContent;
            
            // Only animate if it's a number
            if (!isNaN(parseFloat(value))) {
                animateCounter(valueElement, parseFloat(value));
            }
        }
    });
}, { threshold: 0.5 });

document.querySelectorAll('.metric-card').forEach(card => {
    metricObserver.observe(card);
});

// ===================================
// ACTIVE NAVIGATION LINK
// ===================================
const sections = document.querySelectorAll('section[id]');
const navLinksArray = document.querySelectorAll('.nav-link');

window.addEventListener('scroll', () => {
    let current = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (pageYOffset >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });
    
    navLinksArray.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});

// ===================================
// LAZY LOAD IMAGES (if any are added)
// ===================================
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ===================================
// CONSOLE EASTER EGG
// ===================================
console.log('%c🚀 Text-to-Video Finetuning Framework', 'font-size: 20px; font-weight: bold; color: #6366f1;');
console.log('%cBuilt with PyTorch, Diffusers, and passion for AI research', 'font-size: 12px; color: #a1a1aa;');
console.log('%cGitHub: https://github.com/yourusername/text-to-video-finetuning', 'font-size: 12px; color: #8b5cf6;');

// ===================================
// INITIALIZE
// ===================================
document.addEventListener('DOMContentLoaded', () => {
    console.log('✓ Page loaded successfully');
    
    // Add loaded class to body for CSS transitions
    document.body.classList.add('loaded');
});
