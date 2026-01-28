document.addEventListener('DOMContentLoaded', () => {
    const UI = {
        prompt: document.getElementById('prompt'),
        frames: document.getElementById('frames'),
        steps: document.getElementById('steps'),
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
        serverStatus: document.getElementById('server-status')
    };

    let socket = null;

    const switchView = (state) => {
        Object.keys(UI.views).forEach(key => {
            UI.views[key].classList.toggle('active', key === state);
        });
    };

    const updateProgress = (pct, message) => {
        UI.progressBar.style.width = `${pct}%`;
        UI.progressLabel.textContent = `${pct}% Complete`;
        if (message) UI.status.textContent = message;
    };

    const initializeSocket = () => {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/stream`;
        socket = new WebSocket(wsUrl);

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            switch (data.type) {
                case 'status': UI.status.textContent = data.message; break;
                case 'progress': updateProgress(data.progress, data.message); break;
                case 'complete': 
                    UI.video.src = `${data.video_url}?t=${Date.now()}`;
                    UI.video.load();
                    switchView('result');
                    UI.generateBtn.disabled = false;
                    break;
                case 'error': 
                    alert(data.message);
                    switchView('idle');
                    UI.generateBtn.disabled = false;
                    break;
            }
        };

        socket.onclose = () => {
            UI.serverStatus.textContent = "Offline";
            UI.serverStatus.parentElement.querySelector('.status-dot').style.backgroundColor = "#ef4444";
        };
    };

    UI.generateBtn.addEventListener('click', () => {
        const prompt = UI.prompt.value.trim();
        if (!prompt) return alert("Prompt required.");

        UI.generateBtn.disabled = true;
        switchView('active');
        updateProgress(0, "Connecting to Engine...");

        if (socket) socket.close();
        initializeSocket();

        const checkReady = setInterval(() => {
            if (socket.readyState === WebSocket.OPEN) {
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
    });

    initializeSocket();
});
