document.addEventListener('DOMContentLoaded', () => {
    // UI Elements
    const promptInput = document.getElementById('prompt');
    const stepsInput = document.getElementById('steps');
    const stepsVal = document.getElementById('steps-val');
    const framesInput = document.getElementById('frames');
    const framesVal = document.getElementById('frames-val');
    const generateBtn = document.getElementById('generate-btn');
    const resetBtn = document.getElementById('reset-btn');

    // View States
    const idleView = document.getElementById('idle-view');
    const progressView = document.getElementById('progress-view');
    const videoView = document.getElementById('video-view');
    
    // Status Elements
    const statusMsg = document.getElementById('status-msg');
    const progressBar = document.getElementById('progress-bar');
    const progressPct = document.getElementById('progress-pct');
    const resultVideo = document.getElementById('result-video');

    // State Mapping
    const showState = (stateId) => {
        [idleView, progressView, videoView].forEach(view => view.classList.remove('active'));
        if (stateId === 'idle') idleView.classList.add('active');
        if (stateId === 'progress') progressView.classList.add('active');
        if (stateId === 'video') videoView.classList.add('active');
    };

    // Range Listeners
    stepsInput.addEventListener('input', (e) => stepsVal.textContent = e.target.value);
    framesInput.addEventListener('input', (e) => framesVal.textContent = e.target.value);

    // Generation Logic
    generateBtn.addEventListener('click', () => {
        const prompt = promptInput.value.trim();
        if (!prompt) {
            alert("Please enter a prompt to initialize synthesis.");
            return;
        }

        startGeneration(prompt);
    });

    resetBtn.addEventListener('click', () => {
        showState('idle');
        promptInput.value = '';
    });

    function startGeneration(prompt) {
        showState('progress');
        statusMsg.textContent = "Connecting to Aether-Gen Engine...";
        progressBar.style.width = '0%';
        progressPct.textContent = '0%';

        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/generate`;
        const ws = new WebSocket(wsUrl);

        ws.onopen = () => {
            ws.send(JSON.stringify({
                prompt: prompt,
                num_steps: parseInt(stepsInput.value),
                num_frames: parseInt(framesInput.value)
            }));
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            if (data.type === 'loading_model') {
                statusMsg.textContent = data.message;
            } else if (data.type === 'generating_frames') {
                statusMsg.textContent = data.message;
                progressBar.style.width = `${data.progress}%`;
                progressPct.textContent = `${data.progress}%`;
            } else if (data.type === 'encoding_video') {
                statusMsg.textContent = data.message;
                progressBar.style.width = '95%';
                progressPct.textContent = '95%';
            } else if (data.type === 'complete') {
                showState('video');
                resultVideo.src = data.video_url;
            } else if (data.type === 'error') {
                alert(`Synthesis Error: ${data.message}`);
                showState('idle');
            }
        };

        ws.onerror = (error) => {
            console.error("WS Error:", error);
            alert("Critical link failure with engine.");
            showState('idle');
        };

        ws.onclose = () => {
            console.log("Engine link closed.");
        };
    }
});
