# 📝 Operation Quantization Sync: Implementation Plan

To implement the **Quantization Architecture** and truly differentiate the MAGI cores, we will follow this tactical blueprint.

## Phase 1: Core Identity Differentiation (Ollama Setup)
Instead of all three cores using a generic `llama3`, we will create specialized NERV Modelfiles for each persona.

- [x] **MAGI-1 (Melchior):** Create `melchior.modelfile` using `FROM llama3:8b-instruct-q8_0`. 
- [x] **MAGI-2 (Balthasar):** Create `balthasar.modelfile` using `FROM llama3:8b-instruct-q4_K_M`.
- [x] **MAGI-3 (Casper):** Create `casper.modelfile` using `FROM llama3:8b-instruct-q3_K_L`.

## Phase 2: Neural Link Refactoring (Codebase)
We need to update the system to support per-core model routing.

- [x] **Update `config.py`:** Add a `CORE_MODELS` mapping.
- [x] **Refactor `orchestrator.py` & `main.py`:** Update `query_core` to use the mapping.
- [x] **Update `magi_system.py`:** Apply routing logic to the monolithic script.

## Phase 3: Calibration & Prompt Tuning
- [x] **Melchior Tuning:** Calibrated for high-precision logic.
- [x] **Casper Tuning:** Calibrated for abstract, high-risk intuition.

## Phase 4: Battle Readiness (Validation)
- [x] **Install Script Enhancement:** Added "Full Tactical" vs "Standard" mode selector.
- [ ] **Sync Testing:** Verify vote tag detection.
- [ ] **Perplexity Check:** Confirm persona differentiation.

---
**ESTIMATED COMPLETION: READY FOR IMPACT.** (๑˃ᴗ˂)ﻭ
