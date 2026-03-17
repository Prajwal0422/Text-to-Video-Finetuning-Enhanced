/**
 * NEXUS VISION - Exciting Animations Engine
 * Adds dynamic visual effects to the frontend
 */

// Create floating particles background
function createParticles() {
    const particlesContainer = document.createElement('div');
    particlesContainer.className = 'particles-bg';
    document.body.prepend(particlesContainer);
    
    const particleCount = 50;
    const colors = ['#6366f1', '#8b5cf6', '#ec4899', '#10b981'];
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.background = colors[Math.floor(Math.random() * colors.length)];
        particle.style.animationDelay = Math.random() * 20 + 's';
        particle.style.animationDuration = (15 + Math.random() * 10) + 's';
        particlesContainer.appendChild(particle);
    }
}

// Add ripple effect to buttons
function addRippleEffect() {
    document.querySelectorAll('.btn, .quick-prompt-btn, .feature-card').forEach(element => {
        element.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.className = 'ripple';
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.5)';
            ripple.style.transform = 'scale(0)';
            ripple.style.animation = 'ripple 0.6s ease-out';
            ripple.style.pointerEvents = 'none';
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
}

// Animate elements on scroll
function animateOnScroll() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                entry.target.style.opacity = '1';
            }
        });
    }, {
        threshold: 0.1
    });
    
    document.querySelectorAll('.feature-card, .example-card, .stat-card').forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });
}

// Add hover glow effect
function addHoverGlow() {
    document.querySelectorAll('.btn-primary, .btn-secondary').forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.classList.add('pulse-glow-strong');
        });
        
        btn.addEventListener('mouseleave', function() {
            this.classList.remove('pulse-glow-strong');
        });
    });
}

// Create confetti celebration
function createConfetti() {
    const colors = ['#6366f1', '#8b5cf6', '#ec4899', '#10b981', '#f59e0b'];
    const confettiCount = 50;
    
    for (let i = 0; i < confettiCount; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.left = Math.random() * 100 + '%';
        confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.animationDelay = Math.random() * 3 + 's';
        confetti.style.animationDuration = (2 + Math.random() * 2) + 's';
        document.body.appendChild(confetti);
        
        setTimeout(() => confetti.remove(), 5000);
    }
}

// Animate progress bar with gradient
function animateProgressBar(progressBar, percent) {
    progressBar.style.background = 'linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899)';
    progressBar.style.backgroundSize = '200% 100%';
    progressBar.style.animation = 'gradient-shift 2s ease infinite';
    
    let currentPercent = 0;
    const interval = setInterval(() => {
        if (currentPercent >= percent) {
            clearInterval(interval);
            return;
        }
        currentPercent += 1;
        progressBar.style.width = currentPercent + '%';
    }, 20);
}

// Add typing effect to text
function addTypingEffect(element, text, speed = 50) {
    let i = 0;
    element.textContent = '';
    
    const typeWriter = () => {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(typeWriter, speed);
        }
    };
    
    typeWriter();
}

// Shake element (for errors)
function shakeElement(element) {
    element.classList.add('shake');
    setTimeout(() => element.classList.remove('shake'), 500);
}

// Pulse element (for success)
function pulseElement(element) {
    element.classList.add('heartbeat');
    setTimeout(() => element.classList.remove('heartbeat'), 1500);
}

// Add gradient text animation
function animateGradientText() {
    document.querySelectorAll('h1, h2, .hero-title').forEach(el => {
        if (!el.classList.contains('gradient-text-animated')) {
            el.classList.add('gradient-text-animated');
        }
    });
}

// Mouse trail effect
let mouseTrail = [];
function createMouseTrail(e) {
    const trail = document.createElement('div');
    trail.className = 'mouse-trail';
    trail.style.position = 'fixed';
    trail.style.left = e.clientX + 'px';
    trail.style.top = e.clientY + 'px';
    trail.style.width = '10px';
    trail.style.height = '10px';
    trail.style.borderRadius = '50%';
    trail.style.background = 'rgba(99, 102, 241, 0.5)';
    trail.style.pointerEvents = 'none';
    trail.style.zIndex = '9999';
    trail.style.animation = 'fade-out 1s ease-out forwards';
    
    document.body.appendChild(trail);
    mouseTrail.push(trail);
    
    if (mouseTrail.length > 20) {
        const oldTrail = mouseTrail.shift();
        oldTrail.remove();
    }
    
    setTimeout(() => trail.remove(), 1000);
}

// Add CSS for fade-out animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fade-out {
        to {
            opacity: 0;
            transform: scale(0);
        }
    }
    
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Initialize all animations
function initAnimations() {
    // Create particles background
    createParticles();
    
    // Add ripple effects
    addRippleEffect();
    
    // Animate on scroll
    animateOnScroll();
    
    // Add hover glow
    addHoverGlow();
    
    // Animate gradient text
    animateGradientText();
    
    // Add mouse trail (optional - can be disabled)
    // document.addEventListener('mousemove', createMouseTrail);
    
    console.log('✨ Animations initialized');
}

// Export functions for use in other scripts
window.NexusAnimations = {
    createConfetti,
    animateProgressBar,
    addTypingEffect,
    shakeElement,
    pulseElement,
    initAnimations
};

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAnimations);
} else {
    initAnimations();
}
