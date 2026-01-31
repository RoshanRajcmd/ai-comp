# Local Offline Coding Agent Setup

This guide sets up a **fully local, UI-free coding agent** on **macOS Apple Silicon (M3)** using:

* **llama.cpp** (native, Metal-accelerated inference)
* **GGUF local models** (easy to swap, future-proof)
* **aider** (CLI coding agent that edits your repo safely)

No VS Code extensions. No SaaS. No background daemons.

---

## 0. Prerequisites

* macOS (Apple Silicon M1/M2/M3)
* 16 GB RAM (works well for 6–8B models)
* Homebrew installed
* Git installed
* Python 3.9+

Check:

```bash
brew --version
git --version
python3 --version
```

---

## 1. Install llama.cpp (Native + Metal)

Install via Homebrew:

```bash
brew install llama.cpp
```

Verify:

```bash
llama-cli --help
llama-server --help
```

> `llama-server` provides an OpenAI-compatible HTTP API.

---

## 2. Create a Models Directory

Create a single place for all models:

```bash
mkdir -p ~/Documents/VSCodeWS/llm/models
```

Recommended structure:

```text
~/Documents/VSCodeWS/llm/models/
├── deepseek-coder-6.7b-q4_K_M.gguf
├── qwen2.5-coder-7b-q4_K_M.gguf
├── llama-3.1-8b-q4_K_M.gguf
```

---

## 3. Download Recommended Coding Models (GGUF)

### ⭐ Recommended (Laptop-friendly)

* **DeepSeek-Coder 6.7B – q4_K_M** (best overall)
* **Qwen2.5-Coder 7B – q4_K_M** (very strong, modern)

Download from Hugging Face (example):
deepseek-coder-6.7b-q4_K_M.gguf

(Repeat for other models you want.)

---

## 4. Run llama.cpp Server (Metal Optimized)

### Start Server

```bash
llama-server \
  -m ~/Documents/VSCodeWS/llm/models/deepseek-coder-6.7b-q4_K_M.gguf \
  -c 4096 \
  -t 6 \
  --port 11434
```

Explanation:

* `-m` → model path
* `-c 4096` → context window
* `-t 6` → CPU threads (prevents thermal throttling)
* `--metal` → Apple GPU acceleration
* `--port 11434` → API endpoint

### Test Server

```bash
curl http://localhost:11434/v1/models
```

---

## 5. Switching Models

Stop server (`Ctrl+C`), then restart with a different model:

```bash
llama-server \
  -m ~/Documents/VSCodeWS/llm/models/qwen2.5-coder-7b-instruct-q4_k_m.gguf \
  -c 4096 \
  -t 6 \
  --port 11434
```

No reinstallation required.

---

## 6. Remove a Model

```bash
rm ~/Documents/VSCodeWS/llm/models/old-model-name.gguf
```

That’s it — no registry cleanup needed.

---

## 7. Install aider (CLI Coding Agent)

Install via pip:

```bash
python -m pip install aider-install
aider-install
```

Verify:

```bash
aider --version
```

Official site: [https://aider.chat](https://aider.chat)

---

## 8. Initialize a Project for aider

Inside your git repository:

```bash
git init   # if not already a repo
aider
```

Or explicitly point aider at your local model API:

```bash
aider \
  --model openai/qwen2.5-coder-7b \
  --openai-api-base http://localhost:11434 \
  --openai-api-key none \
  --map-tokens 0 \
  --edit-format diff
```

NOTE:
If you need to limit the context window on aider side as well then append the below
```bash
--max-chat-history-tokens 3000 \
```

If you are getting the model warning error to be removed https://aider.chat/docs/llms/warnings.html append the below
```bash
  --no-show-model-warnings
```

---

## 9. Basic aider Commands

Inside aider prompt:

```text
/add file.py        # allow agent to edit file
/drop file.py       # remove file from context
/ls                 # list tracked files
/diff               # show proposed changes
/commit             # commit changes
/undo               # revert last change
```

Example task:

```text
Refactor this module to use async/await and add unit tests.
```

---

## 10. Safe Workflow (Recommended)

```bash
git status
aider
git diff
git commit -m "AI: refactor auth logic"
```

Aider will never silently overwrite files.

---

## 11. Performance Tuning (macOS M3)

Recommended limits:

* Context: 2048–4096
* Threads: 4–6
* Quantization: q4_K_M
* One model running at a time

Avoid:

* Docker
* q8 models
* Threads > CPU performance cores

---

## 12. Optional: One-Command Launch Script

### macOS (Apple Silicon)

Create `run-llm.sh`:

```bash
#!/bin/bash
llama-server \
  -m ~/Documents/VSCodeWS/llm/models/deepseek-coder-6.7b-q4_K_M.gguf \
  -c 4096 \
  -t 6 \
  --metal
```

```bash
chmod +x run-llm.sh
./run-llm.sh
```

---

## 13. Linux Mint Setup (CPU or GPU)

### 13.1 Install llama.cpp (Linux Mint)

```bash
sudo apt update
sudo apt install -y build-essential cmake python3 python3-pip git

git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
make
sudo cp llama-server /usr/local/bin/
```

Verify:

```bash
llama-server --help
```

---

### 13.2 Linux Mint (CPU-only) – Run Server

```bash
llama-server \
  -m ~/Documents/VSCodeWS/llm/models/deepseek-coder-6.7b-q4_K_M.gguf \
  -c 4096 \
  -t $(nproc)
```

Recommended:

* Use `q4_K_M` or `q4_0`
* Threads = physical cores, not logical

---

### 13.3 Linux Mint (NVIDIA GPU – Optional)

Install CUDA + drivers, then build with CUDA:

```bash
make clean
make LLAMA_CUBLAS=1
sudo cp llama-server /usr/local/bin/
```

Run:

```bash
llama-server \
  -m ~/Documents/VSCodeWS/llm/models/deepseek-coder-6.7b-q4_K_M.gguf \
  -c 4096
```

---

### 13.4 Install aider (Linux Mint)

```bash
python3 -m pip install --upgrade aider-chat
aider-chat
```

Run:

```bash
aider \
  --model openai/qwen2.5-coder-7b \
  --openai-api-base http://localhost:11434 \
  --openai-api-key none
```

---

## 14. Full Removal / Clean Uninstall

### 14.1 Stop Running Services

```bash
pkill llama-server
```

---

### 14.2 Remove Models

```bash
rm -rf ~/llm
```

---

### 14.3 Remove llama.cpp

#### macOS (Homebrew)

```bash
brew uninstall llama.cpp
```

#### Linux Mint (source build)

```bash
sudo rm /usr/local/bin/llama-server
rm -rf ~/llama.cpp
```

---

### 14.4 Remove aider

```bash
python3 -m pip uninstall aider-install
python3 -m pip uninstall aider-chat
```

---

### 14.5 Optional: Python Cleanup

```bash
pip cache purge
```

---

### 14.6 Verify Clean State

```bash
which llama-server || echo "llama.cpp removed"
which aider || echo "aider removed"
```

---

## 15. Final Notes

You now have a setup that can be:

* Installed
* Removed
* Reinstalled
* Migrated across machines

With **zero vendor lock-in** and full control over models and agents.

Create `run-llm.sh`:

```bash
#!/bin/bash
llama-server \
  -m ~/Documents/VSCodeWS/llm/models/deepseek-coder-6.7b-q4_K_M.gguf \
  -c 4096 \
  -t 6 \
  --metal
```

```bash
chmod +x run-llm.sh
./run-llm.sh
```

---

## 13. What You Now Have

* Fully offline coding agent
* Fast model switching
* Git-safe edits
* Zero UI / zero SaaS
* Future-proof for new models

---

## Next Steps (Optional)

* Add multiple agents
* Write your own minimal agent loop
* Add test-running tools
* Automate benchmarks per model

You now own the stack.
