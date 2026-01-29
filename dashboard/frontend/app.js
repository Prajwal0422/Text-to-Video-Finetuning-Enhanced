/**
 * AETHER-GEN CORE ENGINE INTERFACE
 * Handles WebSocket communication, UI state management, and real-time telemetry.
 */

document.addEventListener('DOMContentLoaded', () => {
    // ────────────────────────────────────
    // UI CORE ELEMENTS
    // ────────────────────────────────────
    const UI = {
        prompt: document.getElementById('prompt'),
        frames: document.getElementById('frames'),
        steps: document.getElementById('steps'),
        framesVal: document.getElementById('frames-val'),
        stepsVal: document.getElementById('steps-val'),
        generateBtn: document.getElementById('generate-btn'),
        newGenBtn: document.getElementById('new-gen-btn'),
        
        views: {
            idle: document.getElementById('idle-view'),
            active: document.getElementById('active-view'),
            result: document.getElementById('result-view')
        },
        
        status: document.getElementById('current-status'),
        progressBar: document.getElementById('progress-bar'),
        progressLabel: document.getElementById('progress-label'),
        video: document.getElementById('result-video'),
        serverStatus: document.getElementById('server-status'),
        logStream: document.getElementById('log-stream')
    };

    let socket = null;
    let isGenerating = false;

    // ────────────────────────────────────
    // UTILITIES
    // ────────────────────────────────────

    const addLog = (message, type = 'info') => {
        const entry = document.createElement('div');
        entry.className = `log-entry ${type}`;
        const time = new Date().toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
        entry.innerHTML = `<span style="opacity: 0.4">[${time}]</span> ${message}`;
        UI.logStream.prepend(entry);
    };

    const switchView = (state) => {
        Object.keys(UI.views).forEach(key => {
            if (key === state) {
                UI.views[key].style.display = 'flex';
                UI.views[key].classList.add('active');
            } else {
                UI.views[key].style.display = 'none';
                UI.views[key].classList.remove('active');
            }
        });
    };

    const updateProgress = (pct, message) => {
        UI.progressBar.style.width = `${pct}%`;
        UI.progressLabel.textContent = `${pct}% Complete`;
        if (message) {
            UI.status.textContent = message;
            addLog(`[PROCESS] ${message}`, 'process');
        }
    };

    // ────────────────────────────────────
    // NETWORK LAYER
    // ────────────────────────────────────

    const initializeSocket = () => {
        if (socket) socket.close();
        
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/stream`;
        
        try {
            socket = new WebSocket(wsUrl);
            
            socket.onopen = () => {
                UI.serverStatus.textContent = "Engine Connected";
                document.querySelector('.status-dot-pulse').style.background = "#06b6d4";
                addLog("Neural link established with inference engine.", 'system');
            };

            socket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                
                switch (data.type) {
                    case 'status':
                        UI.status.textContent = data.message;
                        addLog(data.message);
                        break;
                        
                    case 'progress':
                        updateProgress(data.progress, data.message);
                        break;
                        
                    case 'complete':
                        handleCompletion(data.video_url);
                        break;
                        
                    case 'error':
                        handleError(data.message);
                        break;
                }
            };

            socket.onclose = () => {
                UI.serverStatus.textContent = "Engine Disconnected";
                document.querySelector('.status-dot-pulse').style.background = "#f43f5e";
                addLog("Connection severed. Check backend status.", 'error');
                if (isGenerating) handleError("Neural link lost during generation.");
            };

            socket.onerror = (err) => {
                addLog("WebSocket protocol error.", 'error');
            };

        } catch (e) {
            addLog(`Network failure: ${e.message}`, 'error');
        }
    };

    // ────────────────────────────────────
    // EVENT HANDLERS
    // ────────────────────────────────────

    const handleCompletion = (videoUrl) => {
        isGenerating = false;
        addLog("Sequence materialization successful.", 'system');
        
        // Cache bust the video source
        UI.video.src = `${videoUrl}?t=${Date.now()}`;
        UI.video.load();
        
        setTimeout(() => {
            switchView('result');
            UI.generateBtn.disabled = false;
        }, 500);
    };

    const handleError = (msg) => {
        isGenerating = false;
        addLog(`FAILURE: ${msg}`, 'error');
        alert(`System Error: ${msg}`);
        switchView('idle');
        UI.generateBtn.disabled = false;
    };

    // Slider Listeners
    UI.frames.addEventListener('input', (e) => UI.framesVal.textContent = e.target.value);
    UI.steps.addEventListener('input', (e) => UI.stepsVal.textContent = e.target.value);

    // Generation Trigger
    UI.generateBtn.addEventListener('click', () => {
        const prompt = UI.prompt.value.trim();
        if (!prompt) {
            addLog("Rejected: Prompt is required for latent synthesis.", 'error');
            return;
        }

        isGenerating = true;
        UI.generateBtn.disabled = true;
        
        addLog(`Initiating sequence: "${prompt.substring(0, 30)}..."`);
        switchView('active');
        updateProgress(0, "Stabilizing latent space...");

        // Ensure socket is open before sending
        if (!socket || socket.readyState !== WebSocket.OPEN) {
            initializeSocket();
        }

        const checkReady = setInterval(() => {
            if (socket && socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify({
                    prompt: prompt,
                    num_frames: parseInt(UI.frames.value),
                    num_steps: parseInt(UI.steps.value)
                }));
                clearInterval(checkReady);
            }
        }, 100);
    });

    UI.newGenBtn.addEventListener('click', () => {
        switchView('idle');
        UI.generateBtn.disabled = false;
        addLog("Viewport cleared. Ready for new input.");
    });

    // Initialize on load
    initializeSocket();
});
