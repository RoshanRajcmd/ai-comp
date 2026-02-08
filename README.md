# Lumi

An **AI-powered personalized assistant** that helps users manage tasks, provides **personalized recommendations**, and supports **preset personas** using **open-sourced and custom MCP servers**.
Lumi supports both **text and voice interactions**, combining modern web technologies with AI inference pipelines.

---

## ⚙️ Source Code

> Multi-component architecture

* **React Frontend** – Web UI with text & voice interaction
* **Flask Backend** – API layer and AI orchestration
* **Ollama (LLM Runtime)** – Local model inference
* **Dockerized Services** – Unified orchestration via Docker Compose

---

## 📚 Tech Stack and Packages

### Frontend

* React (Create React App)
* TypeScript
* React Icons
* PropTypes
* Web Speech API (SpeechRecognition)

### Backend

* Flask (Python)

### AI / Voice

* Ollama
* Llama-3.2-8B LLM
* Piper TTS Voices

### DevOps

* Docker
* Docker Compose

---

### 📦 NPM Packages Installed

```bash
npm install react-icons
npm install prop-types
npm install --save-dev typescript@latest @types/react@latest @types/react-dom@latest
npm install typescript@4.9.5 --save-dev
npm install --save @types/dom-speech-recognition
```

---

## 🎛️ Features

1. AI-powered personalized assistant
2. Task management and intelligent recommendations
3. Preset and customizable personas
4. Text-based interaction
5. Voice input using Web Speech API
6. Voice output using Piper TTS voices
7. Local LLM inference using Ollama
8. Modular architecture using MCP servers
9. Fully Dockerized development environment

---

## 🧑‍💻 Developer Setup

### 🔊 Voice Recognition (Web Speech API)

Uses the browser’s native Speech Recognition API.

📘 References:

* MDN Documentation:
  [https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition](https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition)
* Type Definitions:
  [https://www.npmjs.com/package/@types/dom-speech-recognition](https://www.npmjs.com/package/@types/dom-speech-recognition)

---

### 🗣️ Text-to-Speech (Piper Voices)

Latest Piper voice models can be downloaded from:

[https://huggingface.co/rhasspy/piper-voices/tree/main/en/en_US/lessac/medium](https://huggingface.co/rhasspy/piper-voices/tree/main/en/en_US/lessac/medium)

---

### 🧠 LLM Setup (Ollama)

#### Download the Model (Run Once on Host Machine)

```bash
docker run -it --rm -v ./ollama_data:/root/.ollama ollama/ollama pull Llama-3.2-8B
```

This downloads the **Llama-3.2-8B** model into a persistent Docker volume.

---

### 🐳 Running with Docker (Recommended)

#### Run from Project Root

```bash
docker compose up --build
```

This will start:

* React Frontend
* Flask Backend
* Ollama LLM service

---

### 🧩 Running Components Individually

```bash
cd <component_directory>
docker build frontend .
docker run -d -p 3000:3000 frontend
```

---

### 🌐 Service URLs

| Service        | URL                                            |
| -------------- | ---------------------------------------------- |
| React Frontend | [http://localhost:3000](http://localhost:3000) |
| Flask Backend  | [http://localhost:5000](http://localhost:5000) |
| Ollama API     | [http://ollama:11434](http://ollama:11434)     |

---

## ⚛️ React Application Scripts

This project was bootstrapped using **Create React App**.

### `npm start`

Runs the app in development mode.
Open [http://localhost:3000](http://localhost:3000) in your browser.

* Auto reload on file changes
* Lint errors shown in console

---

### `npm test`

Runs the test runner in interactive watch mode.

---

### `npm run build`

Builds the app for production into the `build` folder.

* Optimized production build
* Minified output
* Hashed filenames
* Ready for deployment

---

### `npm run eject`

⚠️ **One-way operation**

* Exposes all build configs (Webpack, Babel, ESLint, etc.)
* Cannot be undone
* Use only if deep customization is required

---

## 📖 Learn More

* Create React App Docs:
  [https://facebook.github.io/create-react-app/docs/getting-started](https://facebook.github.io/create-react-app/docs/getting-started)
* React Documentation:
  [https://reactjs.org/](https://reactjs.org/)


