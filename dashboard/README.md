# 🎬 Text-to-Video Finetuning – Enhanced Platform

A production-grade, real-time Text-to-Video generation platform. This system combines a high-performance **FastAPI** backend with a modern, responsive **WebSocket-driven dashboard** to provide a seamless AI product experience.

## 🏗️ System Architecture
The platform is built on a decoupled, asynchronous architecture designed for low-latency feedback and high scalability:

-   **Backend (Python/FastAPI)**: Manages the lifecycle of video generation tasks. It uses an asynchronous Task Manager to handle GPU workloads without blocking the API or WebSocket connections.
-   **Inference Pipeline (PyTorch/Diffusers)**: Utilizes the **ZeroScope V2** model for state-of-the-art text-to-video synthesis. Optimized with FP16 precision and model CPU offloading.
-   **Real-Time Layer (WebSockets)**: Streams live denoising progress and status updates directly from the GPU inference thread to the user interface.
-   **Frontend (HTML5/CSS3/JavaScript)**: A premium "dark-mode" dashboard that provides professional controls for prompt engineering and real-time visualization.

## 🧠 Real-Time Workflow
1.  **Submission**: User submits a prompt and generation parameters (steps, frames).
2.  **Task Queuing**: The `TaskManager` registers the request and initializes a dedicated WebSocket stream.
3.  **Live Denoising**: As the diffusion model iterates, each step triggers a callback that sends progress percentages and status messages (e.g., "Step 12/25: Generating temporal coherence").
4.  **Finalization**: The VAE decodes the latents into video pixels, which are then encoded into an optimized MP4 file.
5.  **Auto-Preview**: The dashboard receives the completion signal and automatically renders the video player.

## 🛠️ Setup & Execution

### 1. Backend Setup
```bash
cd dashboard/backend
pip install -r requirements.txt
```

### 2. Running the Platform
```bash
# Start the FastAPI server (serves both API and Frontend)
python main.py
```
Access the dashboard at: `http://localhost:8000/frontend/index.html`

## 📝 Example Prompts
-   "A futuristic cyberpunk city with neon lights and flying cars, cinematic lighting, 4k."
-   "Time-lapse of a blooming flower in a mystical forest, high detail, slow motion."
-   "Astronaut walking on Mars, red dust blowing, hyper-realistic."

## 🙏 Acknowledgements
Built upon the foundations of **ExponentialML**, **Hugging Face Diffusers**, and the **ModelScope** ecosystem. Distributed under the **MIT License**.
