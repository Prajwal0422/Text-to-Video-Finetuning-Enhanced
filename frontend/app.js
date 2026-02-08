/**
 * NEXUS VISION CORE ENGINE INTERFACE
 * Handles WebSocket communication, UI state management, and real-time telemetry.
 */

let ws = null;
let isGenerating = false;

// DOM Elements
const generateBtn = document.getElementById('generateBtn');
const promptInput = document.getElementById('prompt');
const modeSelect = document.getElementById('mode');
const durationSelect = document.getElementById('duration');
const progressSection = document.getElementById('progressSection');
const resultSection = document.getElementById('resultSection');
const progressFill = document.getElementById('progressFill');
const progressStatus = document.getElementById('progressStatus');
const progressPercent = document.getElementById('progressPercent');
const progressStep = document.getElementById('progressStep');
const resultVideo = document.getElementById('resultVideo');
const downloadBtn = document.getElementById('downloadBtn');

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

// Initialize WebSocket connection
function connectWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/generate`;
    
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
        // Attempt to reconnect after 3 seconds
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
            handleGenerationComplete(data.video_path);
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
}

// Handle generation complete
function handleGenerationComplete(videoPath) {
    isGenerating = false;
    generateBtn.disabled = false;
    generateBtn.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="5 3 19 12 5 21 5 3"></polygon>
        </svg>
        <span>Generate Video</span>
    `;
    
    // Hide progress, show result
    progressSection.style.display = 'none';
    resultSection.style.display = 'block';
    
    // Set video source
    resultVideo.src = videoPath;
    resultVideo.load();
    
    // Setup download button
    downloadBtn.onclick = () => {
        const a = document.createElement('a');
        a.href = videoPath;
        a.download = `nexus-vision-${Date.now()}.mp4`;
        a.click();
    };
    
    // Scroll to result
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Handle generation error
function handleGenerationError(message) {
    isGenerating = false;
    generateBtn.disabled = false;
    generateBtn.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="5 3 19 12 5 21 5 3"></polygon>
        </svg>
        <span>Generate Video</span>
    `;
    
    progressSection.style.display = 'none';
    alert(`Generation failed: ${message}`);
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

// Generate video button handler
generateBtn.addEventListener('click', async () => {
    const prompt = promptInput.value.trim();
    
    if (!prompt) {
        alert('Please enter a prompt');
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
    
    // Hide previous result
    resultSection.style.display = 'none';
    
    // Send generation request
    const request = {
        prompt: prompt,
        mode: modeSelect.value,
        duration: parseInt(durationSelect.value)
    };
    
    console.log('📤 Sending request:', request);
    ws.send(JSON.stringify(request));
});

// Add spin animation for loading icon
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
    console.log('🚀 NEXUS VISION initialized');
    connectWebSocket();
});

// Example prompts for quick testing
const examplePrompts = [
    "A serene sunset over mountains with flowing clouds",
    "City lights at night with time-lapse effect",
    "Ocean waves crashing on a beach at golden hour",
    "Northern lights dancing in the arctic sky",
    "Cherry blossoms falling in a Japanese garden"
];

// Add example prompt on empty click (optional feature)
promptInput.addEventListener('focus', function() {
    if (!this.value) {
        const randomPrompt = examplePrompts[Math.floor(Math.random() * examplePrompts.length)];
        this.placeholder = `Try: "${randomPrompt}"`;
    }
});
