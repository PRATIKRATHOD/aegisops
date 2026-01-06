# AegisOps 🚀
### Agentic AI–Powered Incident Intelligence Platform

---

## 📌 Overview

AegisOps is an open-source, enterprise-inspired incident intelligence
platform that demonstrates how production incidents can be detected,
correlated, and analyzed using **local, open-source GenAI**.

The project is designed around **real ITSM and AIOps principles**,
focusing on safe AI integration, structured data, and clean engineering
practices—without relying on paid APIs or external SaaS tools.

---

## ❓ Why AegisOps?

Modern production environments face several challenges:

- Repeated log-based failures
- Duplicate incidents causing alert fatigue
- Manual and inconsistent root cause analysis
- Unstructured and unsafe AI outputs

AegisOps addresses these problems by combining **incident correlation**
with **structured, validated AI-powered RCA**.

---

## ✨ Key Features

### 🔹 Incident Detection & Correlation
- Log-based incident detection
- ServiceNow-style incident schema
- Correlation logic to suppress duplicate incidents

### 🔹 AI-Powered Root Cause Analysis
- Local GenAI using **Ollama + Mistral**
- Strict JSON-based RCA output
- Schema validation and normalization

### 🔹 Enterprise-Grade Design
- Vendor-agnostic architecture
- No cloud dependencies
- Runtime data excluded from version control
- Automation-ready outputs

---

## 🏗️ Project Architecture

aegisops/
├── agent-core/
│   ├── incident_creator.py        # Log-based incident detection & correlation
│   ├── incident_explainer.py      # Human-readable AI incident explanation
│   └── incident_rca_generator.py  # Unified GenAI RCA pipeline
│
├── incidents/
│   └── incidents.sample.json      # Sample incident schema (runtime data ignored)
│
├── logs/
│   └── sample_app.log             # Sample application logs
│
├── docs/
│   ├── incident-correlation.md    # Incident creation & correlation logic
│   ├── incident-rca.md            # AI-powered RCA design & validation
│   ├── git_info.md                # Git setup and workflow documentation
│   └── ollama-explanation.md      # Local GenAI setup guide
│
├── .gitignore                     # Excludes runtime data, logs, caches
└── README.md                      # Project overview and usage guide

## ⚙️ Tech Stack

| Layer | Technology |
|------|------------|
| Language | Python |
| AI Runtime | Ollama |
| LLM | Mistral (Open Source) |
| OS | Windows / Linux |
| Version Control | Git & GitHub |
| ITSM Model | ServiceNow-inspired |

---

## 🚀 How to Run

### 1️⃣ Prerequisites

- Python 3.10+
- Ollama installed locally
- Mistral model pulled using:
  ```bash
  ollama pull mistral

## 2️⃣ Detect & Correlate Incidents
 - cd agent-core
 - python incident_creator.py

# What this does:
 - Creates a new incident if none exists
 - Correlates with existing OPEN incidents if detected

 3️⃣ Generate Structured RCA
python incident_rca_generator.py


What this does:

Invokes the local LLM

Generates structured RCA

Validates and stores machine-readable JSON

📄 Sample RCA Output
{
  "generated_at": "2026-01-07T00:15:00",
  "root_cause_type": "Software Issue",
  "affected_component": "Application",
  "probable_cause": "Exceeding Java Heap Space",
  "evidence": [
    "ERROR OutOfMemoryError: Java heap space"
  ],
  "impact": "Application Crash",
  "recommended_next_steps": [
    "Investigate memory leaks",
    "Increase JVM heap size",
    "Optimize application memory usage"
  ]
}

🔐 Security & Data Safety

All AI inference runs locally

No external API calls

No incident data committed to Git

Safe AI boundaries with strict validation

🛣️ Roadmap

RCA confidence scoring

Multi-incident reasoning

Automated remediation with guardrails

ITSM tool integrations

👤 Author

Pratik Rathod
Software Engineer | Production Support | AIOps Enthusiast

⭐ Final Note

AegisOps demonstrates how GenAI can be responsibly integrated into
production-grade systems using clean design, structured data, and
enterprise ITSM principles.