// Ultra-Modern Interactions
document.addEventListener('DOMContentLoaded', () => {
    initSmoothScroll();
    initNavbar();
    initAnimations();
    initVideoPlayer();
});

// Smooth Scrolling
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

// Navbar Effects
function initNavbar() {
    const nav = document.querySelector('.nav');
    let lastScroll = 0;
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            nav.style.background = 'rgba(10, 10, 15, 0.95)';
            nav.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.3)';
        } else {
            nav.style.background = 'rgba(10, 10, 15, 0.8)';
            nav.style.boxShadow = 'none';
        }
        
        lastScroll = currentScroll;
    });
}

// Scroll Animations
function initAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    document.querySelectorAll('.feature-card, .demo-stat, .tech-item').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Video Player
function initVideoPlayer() {
    const playBtn = document.querySelector('.play-btn');
    const videoThumbs = document.querySelectorAll('.video-thumb');
    const videoPrompt = document.querySelector('.video-prompt');
    
    if (playBtn) {
        playBtn.addEventListener('click', () => {
            // Simulate video play
            playBtn.style.transform = 'scale(0.9)';
            setTimeout(() => {
                playBtn.style.transform = 'scale(1)';
            }, 200);
        });
    }
    
    videoThumbs.forEach((thumb, index) => {
        thumb.addEventListener('click', () => {
            const prompts = [
                '"Urban cityscape at night"',
                '"Peaceful forest scene"',
                '"Abstract flowing colors"'
            ];
            videoPrompt.textContent = prompts[index];
            
            // Visual feedback
            videoThumbs.forEach(t => t.style.opacity = '0.6');
            thumb.style.opacity = '1';
        });
    });
}

// Parallax Effect
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const spheres = document.querySelectorAll('.gradient-sphere');
    
    spheres.forEach((sphere, index) => {
        const speed = (index + 1) * 0.05;
        sphere.style.transform = `translateY(${scrolled * speed}px)`;
    });
});

// Console Easter Egg
console.log('%c🚀 Text-to-Video AI Framework', 'font-size: 24px; font-weight: bold; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;');
console.log('%cBuilt with PyTorch & Diffusion Models', 'font-size: 14px; color: #a0a0b0;');
console.log('%cGitHub: https://github.com/Prajwal0422/Text-to-Video-Finetuning-Enhanced', 'font-size: 12px; color: #667eea;');
