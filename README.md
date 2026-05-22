# 🔮 MAGI System: Tactical Consensus Engine

```text
╭──────────────────────────────────────────────────────────────────────────────╮
│ 🔴 [SYS.AUTH: SYSTEM_ADMIN]                    [NET_STATUS: FULL_TELEMETRY]  │
├───────────────────────────────────┬──────────────────────────────────────────┤
│                                   │                                          │
│  ███╗   ███╗ █████╗  ██████╗ ██╗  │  [LOCAL NODE: NERV_HQ_GEOFRONT]          │
│  ████╗ ████║██╔══██╗██╔════╝ ██║  │  ──────────────────────────────────────  │
│  ██╔████╔██║███████║██║  ███╗██║  │  [CORE_1: MELCHIOR]  ... 🟢 100% SYNC    │
│  ██║╚██╔╝██║██╔══██║██║   ██║██║  │  [CORE_2: BALTHASAR] ... 🟢 100% SYNC    │
│  ██║ ╚═╝ ██║██║  ██║╚██████╔╝██║  │  [CORE_3: CASPER]    ... 🟢 100% SYNC    │
│  ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  │                                          │
│                                   │  DEFENSE: ABSOLUTE TERROR FIELD ACTIVE   │
├───────────────────────────────────┴──────────────────────────────────────────┤
│ ⚠️  AWAITING DYNAMIC INPUT QUERY...                                          │
╰──────────────────────────────────────────────────────────────────────────────╯
```

> **SUPERCOMPUTER STRATEGY SYSTEM - NERV HQ**

![NERV](https://img.shields.io/badge/NERV-HQ-red?style=for-the-badge)
![Status](https://img.shields.io/badge/STATUS-OPERATIONAL-orange?style=for-the-badge)
![Sync](https://img.shields.io/badge/SYNC-100%25-green?style=for-the-badge)

A high-fidelity terminal implementation of the **MAGI Supercomputer** from Neon Genesis Evangelion. This system runs on a simulated **7th Generation Personality Transplant OS**, using three distinct LLM personas (Melchior, Balthasar, and Casper) to evaluate tactical dilemmas through parallel neural synchronization.

## 🖥️ Interface Gallery

| 1. Tactical Command Center | 2. Dynamic Core Selector | 3. Multi-Turn Debate Scrollback |
| :---: | :---: | :---: |
| ![Command Center](screenshots/Screenshot1.png) | ![Core Selector](screenshots/Screenshot2.png) | ![Debate Scrollback](screenshots/Screenshot3.png) |


## 🧠 The Core Tech: Personality Transplant OS

MAGI is not just running standard code; it simulates a **7th Generation Personality Transplant OS**. In the lore, Dr. Naoko Akagi digitized three distinct, conflicting facets of her own human psyche into three separate biomechanical brains. The system solves complex logical dilemmas by simulating human internal conflict, proving that a little bit of chaos is required for perfect logic!

### 🗂️ The Three Brains (The Trilemma)

| Core Name | Naoko's Persona | Core Motivation & Bias | Role in NERV |
| :--- | :--- | :--- | :--- |
| **Melchior-1** | **The Scientist** | Pure logic, factual analysis, and scientific truth. | Analyzes Angel attack patterns and tactical probability. |
| **Balthasar-2** | **The Mother** | Empathy, protection, and preservation of life. | Prioritizes defensive strategies, base security, and pilot safety. |
| **Casper-3** | **The Woman** | Emotion, intuition, selfishness, and survival instinct. | Acts as the wildcard, prioritizing human desire and self-preservation. |

## ⚖️ The Consensus Mechanism

Instead of a single CPU crunching numbers, MAGI arrives at decisions through a high-speed digital debate.

- **The Debate Protocol:** When a strategic choice is needed, the three brains process the data through their specific personality filters and argue with each other at lightspeed to find the most optimal path forward.
- **Majority Rule:** For standard operations or defense tactics, a simple **2-to-1 majority vote** (CODE 02) is enough to execute a command.
- **The Absolute Veto:** For critical actions (like triggering the self-destruct sequence), the vote must be a **3-0 unanimous consensus** (CODE 01). If even one brain dissents (usually Casper!), the command fails entirely (CODE 03).

## 🛠️ Quantization Architecture

The system utilizes specialized quantization levels for each persona to enhance their unique behavioral profiles:

- **Melchior (High Precision):** Uses `q8_0` for maximum logical consistency and technical fidelity.
- **Balthasar (Standard):** Uses `q4_K_M` for balanced, nuanced ethical reasoning.
- **Casper (Chaos Mode):** Uses `q3_K_L`. Higher perplexity introduces the creative, unconventional variables essential for Casper's "Woman" persona.

## ⌨️ Advanced Input

The neural link is optimized for high-speed tactical entry powered by `prompt_toolkit`.
- Standard terminal navigation and editing commands supported.

## 💬 Stateful Multi-Turn Chat & Continuous Scrollback

The MAGI system now supports continuous debate dialogs and stateful multi-turn history.
- **Neural Link Memory:** Cores maintain conversation history so you can type follow-up questions to query details of their decision logic or ask for clarification.
- **Continuous Scrollback:** Instead of clearing your terminal screen after a consensus is resolved, the main debate runs inside the alternate terminal buffer (using `rich.live`), and prints a permanent NERV tactical report to standard scrollback upon close. The prompt for your next dilemma appears right below!
- **Interactive Shortcuts:**
  - Type `config` or `settings` to open the Model Configuration menu.
  - Type `reset` or `/reset` to completely flush history memory and reset the console layout.

## ⚙️ Dynamic Model Configuration

You can dynamically override the model files mapped to each of the three neural cores directly in the interactive console!
- **Command Shortcut:** Type `config` inside the interactive console.
- **Configuration Modes:**
  - **Specialized Cores:** Uses Naoko Akagi's specific cores (`melchior`, `balthasar`, `casper`) with customized system prompt and parameters.
  - **Single Base Model:** Select any locally installed Ollama model (e.g. `llama3`, `gemma`) to serve as the base model for all three cores (preserving their distinct persona prompts and temperatures).
- **Persistence:** Selections are automatically saved to `~/.magi_config.json`.

## 📦 PyInstaller Standalone Binary Compilation

MAGI can be compiled into a single, standalone executable binary:
1. Install requirements and pyinstaller in your environment:
   ```bash
   pip install pyinstaller
   ```
2. Build the executable:
   ```bash
   pyinstaller --onefile --name magi magi/magi_system.py
   ```
3. Run the standalone binary:
   ```bash
   ./dist/magi
   ```

## 🚀 Deployment

### Prerequisites
- [Ollama](https://ollama.com/) installed and running.

### Tactical Installation (Recommended)
Run the automated installer to set up dependencies and initialize the specialized neural cores:
- **Linux/macOS:** `bash install.sh`
- **Windows:** `install.bat`

**Deployment Modes:**
- **Mode 1: NERV Elite (Full Tactical Sync):** Pulls 3 unique quantization levels (q8_0, q4_K_M, q3_K_L) for maximum persona authenticity. (Heavy ~15.0 GB)
- **Mode 2: NERV Standard (Single-Model Sync):** Uses a single base `llama3` model for all cores. High performance with a minimal footprint. (Light ~5.0 GB)
- **Mode 3: Neural Link Scan:** Verifies if the MAGI cores are already initialized in Ollama.

### Execution
Launch the interactive Command Center:
```bash
magi
```

**Tactical Bypass (Single Query):**
Run a dilemma directly from the shell:
```bash
magi --prompt "Should I skip sleep tonight to finish coding?"
```
*Short flag:* `magi -p "..."`

## 📊 Consensus Codes
- **CODE 01:** UNANIMOUS CONSENSUS (3-0) - OPERATION APPROVED
- **CODE 02:** MAJORITY DECISION (2-1) - PROCEED WITH CAUTION
- **CODE 03:** OPERATION REJECTED BY MAGI (INSUFFICIENT CONSENSUS)

---
*God's in his heaven—all's right with the world.*
