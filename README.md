# AegisOps 🚀  
**Agentic AI–Powered Incident Intelligence Platform**

AegisOps is an open-source, enterprise-inspired incident intelligence
system that demonstrates how modern production incidents can be
detected, correlated, and analyzed using **GenAI**, without relying on
paid APIs or external SaaS platforms.

The project focuses on **real ITSM and AIOps design principles**, not
toy examples.

---

## 🔍 What Problem Does AegisOps Solve?

In real production environments:

- The same error appears repeatedly in logs
- Duplicate incidents create alert fatigue
- Root cause analysis is manual and inconsistent
- AI explanations are often unstructured and unsafe

AegisOps addresses this by:
- Detecting incidents from logs
- Suppressing duplicate incidents using correlation
- Generating **structured, machine-readable RCA** using local GenAI
- Maintaining clean Git hygiene (no runtime data in repo)

---

## 🧠 Key Features

### ✅ Log-Based Incident Detection
- Reads application logs
- Detects known failure patterns (e.g. `OutOfMemoryError`)
- Creates ServiceNow-style incident records

### ✅ Incident Correlation & Deduplication
- Uses correlation IDs to suppress duplicates
- Updates existing OPEN incidents instead of creating new ones
- Mimics real enterprise ITSM behavior

### ✅ GenAI-Powered Root Cause Analysis (RCA)
- Uses **local, open-source LLMs** (via Ollama)
- Generates RCA in **strict JSON format**
- No external APIs, no data leakage

### ✅ RCA Normalization & Validation
- Extracts JSON from AI output
- Validates required RCA fields
- Stores RCA as clean, structured data

### ✅ Enterprise-Grade Design
- Vendor-agnostic
- ITSM-aligned schema
- Safe AI boundaries
- Automation-ready output

---

## 🏗️ Project Architecture

aegisops/
│
├── agent-core/
│ ├── incident_creator.py # Incident detection & correlation
│ ├── incident_explainer.py # Human-readable AI explanation
│ └── incident_rca_generator.py # Unified AI RCA pipeline
│
├── incidents/
│ └── incidents.json # Sample incident schema (runtime data ignored)
│
├── logs/
│ └── sample_app.log # Sample application logs
│
├── docs/
│ ├── incident-correlation.md
│ ├── incident-rca.md
│ ├── git_info.md
│ └── ollama-explanation.md
│
├── .gitignore
└── README.md


---

## ⚙️ Tech Stack

| Area | Technology |
|----|----|
| Language | Python 3.x |
| AI Runtime | Ollama (local) |
| LLM | Mistral (open-source) |
| OS | Windows / Linux |
| Version Control | Git + GitHub |
| ITSM Model | ServiceNow-inspired |

---

## 🚀 How to Run the Project

### 1️⃣ Prerequisites
- Python 3.10+
- Ollama installed locally
- Mistral model pulled (`ollama pull mistral`)

---

### 2️⃣ Detect & Correlate Incidents
```bash
cd agent-core
python incident_creator.py
