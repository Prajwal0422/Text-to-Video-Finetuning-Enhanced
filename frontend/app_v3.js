/**
 * NEXUS VISION V3 - Enhanced Frontend Engine
 * Real-time video generation with WebSocket communication
 */

let ws = null;
let isGenerating = false;
let startTime = null;
let timerInterval = null;

// DOM Elements
const generateBtn = document.getElementById('generateBtn');
const promptInput = document.getElementById('prompt');
const modeSelect = document.getElementById('mode');
const durationSelect = document.getElementById('duration');
const resolutionSelect = document.getElementById('resolution');
const fpsSelect = document.getElementById('fps');
const progressSection = document.getElementById('progressSection');
const resultSection = document.getElementById('resultSection');
const progressFill = document.getElementById('progressFill');
const progressStatus = document.getElementById('progressStatus');
const progressPercent = document.getElementById('progressPercent');
const progressStep = document.getElementById('progressStep');
const progressTime = document.getElementById('progressTime');
const resultVideo = document.getElementById('resultVideo');
const downloadBtn = document.getElementById('downloadBtn');
const shareBtn = document.getElementById('shareBtn');
const charCount = document.getElementById('charCount');
const apiStatus = document.getElementById('apiStatus');

// Smooth scroll for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// Update active nav link on scroll
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section[id]');
    const scrollY = window.pageYOffset;

    sections.forEach(section => {
        const sectionHeight = section.offsetHeight;
        const sectionTop = section.offsetTop - 100;
        const sectionId = section.getAttribute('id');
        const navLink = document.querySelector(`.nav-link[href="#${sectionId}"]`);

        if (navLink && scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
            document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
            navLink.classList.add('active');
        }
    });
});

// Character counter
if (promptInput) {
    promptInput.addEventListener('input', () => {
        const count = promptInput.value.length;
        charCount.textContent = count;
        if (count > 500) {
            charCount.style.color = 'var(--error)';
        } else if (count > 400) {
            charCount.style.color = 'var(--warning)';
        } else {
            charCount.style.color = 'var(--text-muted)';
        }
    });
}

// Quick prompt buttons
document.querySelectorAll('.quick-prompt-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const prompt = btn.getAttribute('data-prompt');
        promptInput.value = prompt;
        promptInput.dispatchEvent(new Event('input'));
        promptInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
});

// Initialize WebSocket connection
function connectWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.hostname;
    const port = window.location.port || '8000';
    const wsUrl = `${protocol}//${host}:${port}/ws/generate`;
    
    console.log('Connecting to:', wsUrl);
    ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
        console.log('✅ WebSocket connected');
        updateSystemStatus('online');
    };
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
    };
    
    ws.onerror = (error) => {
        console.error('❌ WebSocket error:', error);
        updateSystemStatus('error');
    };
    
    ws.onclose = () => {
        console.log('🔌 WebSocket disconnected');
        updateSystemStatus('offline');
        setTimeout(connectWebSocket, 3000);
    };
}

// Handle WebSocket messages
function handleWebSocketMessage(data) {
    console.log('📨 Received:', data);
    
    switch (data.type) {
        case 'progress':
            updateProgress(data.progress, data.message, data.step);
            break;
            
        case 'complete':
            handleGenerationComplete(data.video_path, data.duration, data.file_size);
            break;
            
        case 'error':
            handleGenerationError(data.message);
            break;
    }
}

// Update progress UI
function updateProgress(percent, message, step) {
    progressSection.style.display = 'block';
    progressFill.style.width = `${percent}%`;
    progressPercent.textContent = `${Math.round(percent)}%`;
    progressStatus.textContent = message || 'Generating...';
    progressStep.textContent = step || '';
    
    // Add exciting animations
    if (window.NexusAnimations) {
        window.NexusAnimations.animateProgressBar(progressFill, percent);
    }
    
    // Add visual feedback for different stages
    if (percent < 30) {
        progressFill.style.background = 'linear-gradient(90deg, #6366f1, #8b5cf6)';
        progressFill.classList.add('shimmer');
    } else if (percent < 60) {
        progressFill.style.background = 'linear-gradient(90deg, #8b5cf6, #ec4899)';
        progressFill.classList.add('pulse-glow-strong');
    } else {
        progressFill.style.background = 'linear-gradient(90deg, #ec4899, #10b981)';
        progressFill.classList.add('breathe');
    }
}

// Timer for elapsed time
function startTimer() {
    startTime = Date.now();
    timerInterval = setInterval(() => {
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        progressTime.textContent = `${elapsed}s elapsed`;
    }, 100);
}

function stopTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
}

// Handle generation complete
function handleGenerationComplete(videoPath, duration, fileSize) {
    stopTimer();
    isGenerating = false;
    generateBtn.disabled = false;
    generateBtn.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="5 3 19 12 5 21 5 3"></polygon>
        </svg>
        <span>Generate Video</span>
    `;
    
    progressSection.style.display = 'none';
    resultSection.style.display = 'block';
    
    // Add celebration animations
    if (window.NexusAnimations) {
        window.NexusAnimations.createConfetti();
        window.NexusAnimations.pulseElement(resultSection);
    }
    
    // Add bounce animation to result section
    resultSection.classList.add('bounce-in');
    
    resultVideo.src = videoPath;
    resultVideo.load();
    
    // Update video info
    const genTime = Math.floor((Date.now() - startTime) / 1000);
    document.getElementById('genTime').textContent = `${genTime}s`;
    document.getElementById('fileSize').textContent = fileSize || 'Unknown';
    document.getElementById('videoRes').textContent = resolutionSelect.value + 'p';
    
    // Setup download button
    downloadBtn.onclick = () => {
        const a = document.createElement('a');
        a.href = videoPath;
        a.download = `nexus-vision-${Date.now()}.mp4`;
        a.click();
    };
    
    // Setup share button
    shareBtn.onclick = () => {
        if (navigator.share) {
            navigator.share({
                title: 'NEXUS VISION Generated Video',
                text: 'Check out this AI-generated video!',
                url: window.location.href
            }).catch(err => console.log('Share failed:', err));
        } else {
            // Fallback: copy link
            navigator.clipboard.writeText(window.location.href);
            alert('Link copied to clipboard!');
        }
    };
    
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Handle generation error
function handleGenerationError(message) {
    stopTimer();
    isGenerating = false;
    generateBtn.disabled = false;
    generateBtn.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="5 3 19 12 5 21 5 3"></polygon>
        </svg>
        <span>Generate Video</span>
    `;
    
    progressSection.style.display = 'none';
    
    // Show user-friendly error message
    const errorMessages = {
        'No prompt provided': 'Please enter a description for your video',
        'API': 'Connection error. Please check your internet and try again',
        'timeout': 'Generation took too long. Please try a simpler prompt',
        'No clips found': 'Could not find matching videos. Try a different description'
    };
    
    let userMessage = message;
    for (const [key, value] of Object.entries(errorMessages)) {
        if (message.includes(key)) {
            userMessage = value;
            break;
        }
    }
    
    alert(`Generation failed: ${userMessage}`);
}

// Update system status indicator
function updateSystemStatus(status) {
    const statusDot = document.querySelector('.status-dot');
    const statusText = document.querySelector('.status-badge span:last-child');
    
    if (statusDot && statusText) {
        switch (status) {
            case 'online':
                statusDot.classList.add('active');
                statusText.textContent = 'Ready';
                break;
            case 'offline':
                statusDot.classList.remove('active');
                statusText.textContent = 'Offline';
                break;
            case 'error':
                statusDot.classList.remove('active');
                statusText.textContent = 'Error';
                break;
        }
    }
}

// Check API status
async function checkAPIStatus() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        if (apiStatus) {
            apiStatus.textContent = data.status === 'online' ? 'Connected' : 'Offline';
            apiStatus.className = 'stat-status ' + (data.status === 'online' ? 'online' : '');
        }
    } catch (error) {
        if (apiStatus) {
            apiStatus.textContent = 'Error';
            apiStatus.className = 'stat-status';
        }
    }
}

// Generate video button handler
if (generateBtn) {
    generateBtn.addEventListener('click', async () => {
        const prompt = promptInput.value.trim();
        
        if (!prompt) {
            alert('Please enter a prompt');
            return;
        }
        
        if (prompt.length > 500) {
            alert('Prompt is too long (max 500 characters)');
            return;
        }
        
        if (isGenerating) {
            return;
        }
        
        if (!ws || ws.readyState !== WebSocket.OPEN) {
            alert('WebSocket not connected. Please wait...');
            connectWebSocket();
            return;
        }
        
        isGenerating = true;
        generateBtn.disabled = true;
        generateBtn.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="animation: spin 1s linear infinite;">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M12 6v6l4 2"></path>
            </svg>
            <span>Generating...</span>
        `;
        
        resultSection.style.display = 'none';
        startTimer();
        
        const request = {
            prompt: prompt,
            mode: modeSelect.value,
            duration: parseInt(durationSelect.value),
            resolution: parseInt(resolutionSelect.value),
            fps: parseInt(fpsSelect.value)
        };
        
        console.log('📤 Sending request:', request);
        ws.send(JSON.stringify(request));
    });
}

// Add spin animation
const style = document.createElement('style');
style.textContent = `
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 NEXUS VISION V3 initialized');
    connectWebSocket();
    checkAPIStatus();
    setInterval(checkAPIStatus, 30000); // Check every 30s
});

// Example prompts for placeholder
const examplePrompts = [
    "A serene sunset over mountains with flowing clouds",
    "City lights at night with time-lapse effect",
    "Ocean waves crashing on a beach at golden hour",
    "Northern lights dancing in the arctic sky",
    "Cherry blossoms falling in a Japanese garden"
];

if (promptInput) {
    promptInput.addEventListener('focus', function() {
        if (!this.value) {
            const randomPrompt = examplePrompts[Math.floor(Math.random() * examplePrompts.length)];
            this.placeholder = `Try: "${randomPrompt}"`;
        }
    });
}
