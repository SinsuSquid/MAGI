# 🔮 MAGI System: Tactical Consensus Engine

This project is a high-fidelity terminal implementation of the **MAGI Supercomputer** from Neon Genesis Evangelion. It uses three distinct LLM personas (Melchior, Balthasar, and Casper) to evaluate tactical dilemmas and reach a consensus through parallel neural synchronization.

---

## 🛠️ Project Overview

- **Main Technologies:** Python 3.8+, [Ollama](https://ollama.com/) (Llama 3), `rich` (TUI), `prompt_toolkit`.
- **Core Architecture:**
    - **Parallel Processing:** Uses Python `threading` to query three LLM cores simultaneously.
    - **TUI (Terminal User Interface):** Built with `rich` for a retro NERV-style interface.
    - **Neural Sync:** Each core (Scientist, Mother, Woman) must provide a vote (`APPROVE` or `REJECT`) which is then tallied for a final verdict.

## 📂 Directory Structure & Architecture

The project contains two main implementation paths:

1.  **`magi/magi_system.py` (Primary Entry Point):**
    - A feature-rich, "monolithic" implementation.
    - Includes NERV telemetry logs, Easter eggs (`SECRET_PHRASES`), and CLI argument support.
    - This is the script mapped to the `magi` command in `pyproject.toml`.

2.  **`magi/` (Modular Implementation):**
    - `main.py`: A cleaner, modular entry point using the components below.
    - `orchestrator.py`: Logic for handling parallel core queries and vote parsing.
    - `ui_layouts.py`: Definitions for the `rich` layouts and panels.
    - `config.py`: Global constants, system prompts for the three personas, and ASCII art.

## 🧠 The Three Cores (Personas)

- **MAGI-1: MELCHIOR (Scientist):** Purely logical, analytical, and data-driven.
- **MAGI-2: BALTHASAR (Mother):** Empathetic, human-centric, and ethical.
- **MAGI-3: CASPER (Woman):** Bold, intuitive, independent, and risk-taking.

## 🛠️ Quantization Architecture

To optimize the personas' behavioral profiles, it is recommended to use different quantization levels in Ollama:

- **Melchior (High Precision):** Use `q8_0` or `fp16`. Logical consistency and data parsing require high fidelity.
- **Balthasar (Standard Precision):** Use `q4_K_M` or `q5_K_M`. A balance of performance and nuanced ethical reasoning.
- **Casper (Low Precision/Chaos):** Use `q3_K_L` or `q4_K_S`. Higher perplexity from heavy quantization introduces the chaotic, "maverick" tokens that suit Casper's intuitive and risk-taking nature! (๑˃ᴗ˂)

## 🚀 Building and Running

### Prerequisites
- **Ollama:** Must be installed and running.

### Tactical Installation (Recommended)
Run the automated installer to set up dependencies and initialize the specialized MAGI cores:
- **Linux/macOS:** `bash install.sh`
- **Windows:** `install.bat`

**Deployment Modes:**
- **Full Tactical Sync:** Pulls 3 unique quants for maximum persona differentiation (Heavy).
- **Standard Sync:** Uses a single base `llama3` for all cores to save storage (Light).

### Manual Commands
- **Install Dependencies:** `pip install -r requirements.txt`
- **Create Cores Manually:** `ollama create <persona> -f <persona>.modelfile`
- **Run Interactive Mode:** `magi` or `python magi/magi_system.py`
- **Single Query Mode:** `magi -p "Your dilemma here"`

## 🎨 Development Conventions

- **NERV Aesthetic:** Strictly adhere to the tactical color palette:
    - `Amber (#ff9900)`: General UI and warnings.
    - `Green (#00ff66)`: Approvals and 100% Sync.
    - `Red (#ff0033)`: Rejections and Critical Errors.
- **Vote Parsing:** LLM responses MUST include `[VOTE: APPROVE]` or `[VOTE: REJECT]`. Use robust regex parsing to detect these tags regardless of surrounding fluff.
- **Parallelism:** Always query cores in parallel to maintain the "simultaneous sync" feel of the MAGI.

---
*God's in his heaven—all's right with the world.*
