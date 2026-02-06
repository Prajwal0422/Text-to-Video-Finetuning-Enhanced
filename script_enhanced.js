// Enhanced JavaScript with Professional Animations
// Import base functionality
document.addEventListener('DOMContentLoaded', () => {
    initParticles();
    initVideoPlayer();
    initGallery();
    initStatCounters();
    initScrollAnimations();
    initProgressBar();
});

// ===================================
// PARTICLE BACKGROUND
// ===================================
function initParticles() {
    const canvas = document.getElementById('particles-canvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    let particles = [];
    let animationId;
    
    function resizeCanvas() {
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;
    }
    
    class Particle {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 2 + 1;
            this.speedX = Math.random() * 0.5 - 0.25;
            this.speedY = Math.random() * 0.5 - 0.25;
            this.opacity = Math.random() * 0.5 + 0.2;
        }
        
        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            
            if (this.x > canvas.width) this.x = 0;
            if (this.x < 0) this.x = canvas.width;
            if (this.y > canvas.height) this.y = 0;
            if (this.y < 0) this.y = canvas.height;
        }
        
        draw() {
            ctx.fillStyle = `rgba(99, 102, 241, ${this.opacity})`;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
        }
    }
    
    function init() {
        resizeCanvas();
        particles = [];
        for (let i = 0; i < 50; i++) {
            particles.push(new Particle());
        }
    }
    
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(particle => {
            particle.update();
            particle.draw();
        });
        animationId = requestAnimationFrame(animate);
    }
    
    init();
    animate();
    
    window.addEventListener('resize', () => {
        resizeCanvas();
        init();
    });
}

// ===================================
// VIDEO PLAYER
// ===================================
function initVideoPlayer() {
    const playBtn = document.getElementById('playBtn');
    const videoPlaceholder = document.getElementById('mainVideoPlayer');
    const progressFill = document.querySelector('.progress-fill');
    const timeDisplay = document.querySelector('.time-display');
    
    let isPlaying = false;
    let currentTime = 0;
    const duration = 8; // 8 seconds
    let animationId;
    
    function togglePlay() {
        isPlaying = !isPlaying;
        
        if (isPlaying) {
            playBtn.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <rect x="6" y="4" width="4" height="16"></rect>
                    <rect x="14" y="4" width="4" height="16"></rect>
                </svg>
            `;
            videoPlaceholder.style.opacity = '0.7';
            startProgress();
        } else {
            playBtn.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <polygon points="5 3 19 12 5 21 5 3"></polygon>
                </svg>
            `;
            videoPlaceholder.style.opacity = '1';
            stopProgress();
        }
    }
    
    function startProgress() {
        function update() {
            if (currentTime >= duration) {
                currentTime = 0;
                isPlaying = false;
                togglePlay();
                return;
            }
            
            currentTime += 0.016; // ~60fps
            const progress = (currentTime / duration) * 100;
            progressFill.style.width = `${progress}%`;
            timeDisplay.textContent = `${formatTime(currentTime)} / ${formatTime(duration)}`;
            
            if (isPlaying) {
                animationId = requestAnimationFrame(update);
            }
        }
        update();
    }
    
    function stopProgress() {
        if (animationId) {
            cancelAnimationFrame(animationId);
        }
    }
    
    function formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }
    
    if (playBtn) {
        playBtn.addEventListener('click', togglePlay);
    }
    
    if (videoPlaceholder) {
        videoPlaceholder.addEventListener('click', togglePlay);
    }
    
    // Progress bar click
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        progressBar.addEventListener('click', (e) => {
            const rect = progressBar.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const percentage = x / rect.width;
            currentTime = percentage * duration;
            const progress = (currentTime / duration) * 100;
            progressFill.style.width = `${progress}%`;
            timeDisplay.textContent = `${formatTime(currentTime)} / ${formatTime(duration)}`;
        });
    }
}

// ===================================
// GALLERY INTERACTION
// ===================================
function initGallery() {
    const galleryItems = document.querySelectorAll('.gallery-item');
    const mainPlayer = document.getElementById('mainVideoPlayer');
    
    galleryItems.forEach((item, index) => {
        item.addEventListener('click', () => {
            // Visual feedback
            galleryItems.forEach(i => i.style.borderColor = 'var(--border-color)');
            item.style.borderColor = 'var(--accent-primary)';
            
            // Update main player (in real app, would load different video)
            const info = item.querySelector('.gallery-info');
            const title = info.querySelector('h4').textContent;
            const desc = info.querySelector('p').textContent;
            
            const videoInfo = mainPlayer.querySelector('.video-info');
            videoInfo.querySelector('h4').textContent = title;
            videoInfo.querySelector('p').textContent = `Prompt: "${desc}"`;
            
            // Animation
            mainPlayer.style.transform = 'scale(0.98)';
            setTimeout(() => {
                mainPlayer.style.transform = 'scale(1)';
            }, 200);
        });
    });
}

// ===================================
// STAT COUNTERS
// ===================================
function initStatCounters() {
    const statNumbers = document.querySelectorAll('.stat-number');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.dataset.animated) {
                entry.target.dataset.animated = 'true';
                animateCounter(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    statNumbers.forEach(stat => observer.observe(stat));
}

function animateCounter(element) {
    const target = parseFloat(element.dataset.target);
    if (isNaN(target)) return;
    
    const duration = 2000;
    const steps = 60;
    const increment = target / steps;
    let current = 0;
    let step = 0;
    
    const timer = setInterval(() => {
        step++;
        current += increment;
        
        if (step >= steps) {
            current = target;
            clearInterval(timer);
        }
        
        element.textContent = current.toFixed(1);
    }, duration / steps);
}

// ===================================
// SCROLL ANIMATIONS
// ===================================
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll(
        '.video-player, .gallery-item, .stat-card, .comparison-side, .metric-card'
    );
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// ===================================
// PROGRESS BAR ANIMATION
// ===================================
function initProgressBar() {
    const progressBar = document.querySelector('.progress-bar');
    if (!progressBar) return;
    
    progressBar.addEventListener('mouseenter', () => {
        progressBar.style.height = '6px';
    });
    
    progressBar.addEventListener('mouseleave', () => {
        progressBar.style.height = '4px';
    });
}

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
    
    if (currentScroll > 50) {
        navbar.style.boxShadow = '0 4px 16px rgba(0, 0, 0, 0.3)';
        navbar.style.background = 'rgba(10, 10, 15, 0.95)';
    } else {
        navbar.style.boxShadow = 'none';
        navbar.style.background = 'rgba(10, 10, 15, 0.8)';
    }
    
    lastScroll = currentScroll;
});

// ===================================
// CONSOLE EASTER EGG
// ===================================
console.log('%c🚀 Text-to-Video Finetuning Framework', 'font-size: 20px; font-weight: bold; color: #6366f1;');
console.log('%cBuilt with PyTorch, Diffusers, and passion for AI research', 'font-size: 12px; color: #a1a1aa;');
console.log('%cGitHub: https://github.com/Prajwal0422/Text-to-Video-Finetuning-Enhanced', 'font-size: 12px; color: #8b5cf6;');
