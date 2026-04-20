<div align="center">

# 🛡️ Aegis-SRE

**Predictive Anomaly Detection · Agentic Root Cause Analysis · 100% Local**

*Predicting a crash is science. Diagnosing it is engineering.*

<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Anomaly%20Detection-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Ollama](https://img.shields.io/badge/Ollama-Llama%203.2%20Local-black?style=flat-square&logo=ollama&logoColor=white)](https://ollama.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-Orchestration-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-blueviolet?style=flat-square)](CONTRIBUTING.md)

<br/>

> Aegis-SRE is an autonomous Site Reliability agent that fuses **Classical ML** for high-speed anomaly detection with **Generative AI** for contextual root cause analysis — solving the *3 AM on-call problem* before the pager ever fires.

<br/>

[Overview](#-overview) · [Architecture](#-system-architecture) · [Features](#-key-features) · [Quickstart](#-quickstart) · [Tech Stack](#-tech-stack) · [Roadmap](#-roadmap) · [Contributing](#-contributing)

</div>

---

## 🌟 Overview

Most monitoring tools are **reactive** — they alert you after something breaks. **Aegis-SRE is proactive.**

By combining an **Isolation Forest** model for statistical anomaly detection with a **locally-hosted LLM (Llama 3.2 via Ollama)** for deep contextual reasoning, Aegis monitors your system metrics in real time, detects failure signatures *before* they escalate, and autonomously generates a verifiable **Root Cause Analysis (RCA)** complete with a suggested patch — all without sending a single byte to an external API.

This is not just a monitoring dashboard. Aegis is a two-brain system:

| Brain | Technology | Role |
|---|---|---|
| 🔬 **The Predictor** | Isolation Forest (Scikit-learn) | Detects statistical outliers in CPU, RAM, traffic, and error-rate streams that precede system failures |
| 🧠 **The Diagnostician** | Llama 3.2 (Ollama) + RAG | Reads surrounding log context and recent Git commits to reason about *why* the anomaly is occurring and *how* to fix it |

---

## 🧠 System Architecture

Aegis-SRE operates as a **three-stage autonomous pipeline**:

```
                    ┌─────────────────────────────────────┐
                    │         LIVE SYSTEM METRICS          │
                    │   CPU · RAM · Traffic · Error Rate   │
                    └──────────────────┬──────────────────┘
                                       │
                                       ▼
                    ┌─────────────────────────────────────┐
                    │     STAGE 1 — THE SENTINEL          │
                    │   Isolation Forest (Classical ML)    │
                    │   Background thread · Real-time      │
                    └──────────────────┬──────────────────┘
                                       │
                        ┌──────────────┴──────────────┐
                        │                             │
                   [NORMAL]                     [ANOMALY DETECTED]
                        │                             │
                   Continue                           ▼
                  Monitoring         ┌─────────────────────────────┐
                                     │   STAGE 2 — THE DIAGNOSTICIAN│
                                     │   Context Extraction (Logs)  │
                                     │   RAG over Git + README      │
                                     │   Ollama LLM Reasoning       │
                                     └──────────────┬──────────────┘
                                                    │
                                                    ▼
                                     ┌─────────────────────────────┐
                                     │   STAGE 3 — THE RESOLVER    │
                                     │   Streamlit Incident Report  │
                                     │   Root Cause Analysis (RCA)  │
                                     │   Suggested Code Patch       │
                                     └─────────────────────────────┘
```

### Stage Breakdown

**Stage 1 · The Sentinel (Classical ML)**
A background thread continuously ingests system telemetry. The trained Isolation Forest model scores each data point, flagging statistical outliers that match known failure signatures — memory leak patterns, traffic spikes, cascading error rates — *before* they trigger a crash.

**Stage 2 · The Diagnostician (GenAI Agent)**
On anomaly detection, the agent captures the surrounding log window and runs a Retrieval-Augmented Generation (RAG) pass over your project's `README`, recent Git commits, and historical logs. The local LLM then performs a zero-shot causal diagnosis: *what changed, why it matters, and what to do next.*

**Stage 3 · The Resolver (Dashboard)**
A Streamlit dashboard surfaces real-time health metrics and structured **Incident Reports** containing the exact anomalous log line, the predicted failure category, the AI-generated RCA, and a suggested code-level fix.

---

## ✨ Key Features

- **🔮 Proactive Detection** — Catches memory leaks, traffic spikes, and error cascades *before* they become outages, not after
- **🤖 Autonomous RCA** — LLM agent reasons across logs, commits, and documentation to produce a human-readable root cause report with zero manual input
- **🔒 Fully Local & Private** — All inference runs on-device via Ollama. No API keys. No telemetry. No data leaves your machine
- **📊 Real-Time Dashboard** — Streamlit UI with live metric visualizations and structured incident cards
- **🧩 Modular Pipeline** — Each stage (Sentinel → Diagnostician → Resolver) is independently testable and replaceable
- **📁 RAG over Your Codebase** — The agent reads *your* repository context, not generic documentation — making every diagnosis project-specific

---

## 🚀 Quickstart

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/download) installed and running locally
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/aegis-sre.git
cd aegis-sre
```

### 2. Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Pull the Local LLM

```bash
ollama pull llama3.2
```

### 4. Configure the Agent

Copy the example environment file and set your paths:

```bash
cp .env.example .env
```

```env
# .env
LOG_FILE_PATH=./data/sample_logs.csv
REPO_CONTEXT_PATH=./context/
OLLAMA_MODEL=llama3.2
ANOMALY_THRESHOLD=0.15
```

### 5. Train the Sentinel Model

```bash
python src/train_sentinel.py --data ./data/server_metrics.csv
```

### 6. Launch Aegis

```bash
# Start the FastAPI orchestration backend
uvicorn src.api.main:app --reload --port 8000

# In a separate terminal, launch the dashboard
streamlit run src/dashboard/app.py
```

Navigate to `http://localhost:8501` to open the Aegis dashboard.

---

## 🗂️ Project Structure

```
aegis-sre/
├── data/
│   ├── server_metrics.csv         # Training data (CPU, RAM, Traffic, Error Rate)
│   └── sample_logs.txt            # Sample log file for RAG context
│
├── src/
│   ├── sentinel/
│   │   ├── train_sentinel.py      # Isolation Forest training pipeline
│   │   └── monitor.py             # Real-time background monitoring thread
│   │
│   ├── diagnostician/
│   │   ├── rag_engine.py          # Log + commit context retrieval
│   │   └── llm_agent.py           # Ollama inference + RCA generation
│   │
│   ├── api/
│   │   └── main.py                # FastAPI orchestration layer
│   │
│   └── dashboard/
│       └── app.py                 # Streamlit real-time UI
│
├── context/                       # Drop your README, docs, and commit history here
├── models/                        # Saved Isolation Forest artifacts
├── tests/
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Anomaly Detection** | Scikit-learn · Isolation Forest | Unsupervised outlier detection on tabular metrics |
| **LLM Inference** | Ollama · Llama 3.2 | 100% local generative reasoning — no API costs |
| **RAG Context** | LangChain · FAISS | Semantic retrieval over logs, commits, and docs |
| **Orchestration** | FastAPI | Async pipeline coordination between all stages |
| **Dashboard** | Streamlit | Real-time metric visualization and incident reporting |
| **Data** | Kaggle · CSV · Live `/proc` | Server metrics and log datasets |

---

## 📊 Example Incident Report

```
╔══════════════════════════════════════════════════════════════════╗
║  🚨 AEGIS INCIDENT REPORT — 2025-07-15 03:47:22 UTC             ║
╠══════════════════════════════════════════════════════════════════╣
║  Anomaly Score    │ -0.312  (threshold: -0.150)                  ║
║  Predicted Class  │ MEMORY_LEAK                                  ║
║  Confidence       │ 87.4%                                        ║
╠══════════════════════════════════════════════════════════════════╣
║  TRIGGERING LOG LINE                                             ║
║  > [03:47:19] worker-3 RSS 94.2% — GC pause 4800ms              ║
╠══════════════════════════════════════════════════════════════════╣
║  ROOT CAUSE ANALYSIS (Llama 3.2)                                 ║
║                                                                  ║
║  Based on commit a3f812c ("refactor: cache layer rewrite"),      ║
║  the LRU eviction policy was replaced with an unbounded dict.    ║
║  Under sustained traffic, this cache grows without limit,        ║
║  causing the GC pressure visible in worker-3's RSS spike.        ║
╠══════════════════════════════════════════════════════════════════╣
║  SUGGESTED PATCH                                                 ║
║                                                                  ║
║  - Replace `self.cache = {}` with                                ║
║    `self.cache = LRUCache(maxsize=1024)`                         ║
║  - Add eviction telemetry to cache.py, line 47                   ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 🗺️ Roadmap

- [x] Isolation Forest sentinel with CSV ingestion
- [x] Ollama LLM integration for zero-shot RCA
- [x] FastAPI orchestration backend
- [x] Streamlit real-time dashboard
- [ ] **v0.2** — Git commit RAG pipeline (LangChain + FAISS)
- [ ] **v0.2** — LSTM-based time-series predictor as sentinel alternative
- [ ] **v0.3** — Slack / PagerDuty webhook integration for incident dispatch
- [ ] **v0.3** — Docker Compose deployment for one-command setup
- [ ] **v1.0** — Multi-service topology support (microservices mode)
- [ ] **v1.0** — Automated patch PR generation via GitHub API

---

## 🤝 Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

```bash
# Run the test suite
pytest tests/ -v

# Lint
ruff check src/
```

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">

Built with the **Responsible Vibe Coding** philosophy —
AI-assisted engineering where the human owns the system, but the AI tames the complexity.

<br/>

⭐ **Star this repo** if Aegis saves your on-call rotation.

</div>
