# 🛡️ AegisOps – Agentic AIOps Incident & RCA Engine

## ⚙️ Tech Stack

| Layer | Technology |
|------|-----------|
| Language | Python |
| AI Runtime | Ollama |
| LLM | Mistral (Open Source) |
| OS | Windows / Linux |
| Version Control | Git & GitHub |
| ITSM Model | ServiceNow-inspired |

---

## 🚀 How to Run

### 1️⃣ Prerequisites

- Python **3.10+**
- Ollama installed locally
- Pull Mistral model:

```bash
ollama pull mistral
```

---

### 2️⃣ Detect & Correlate Incidents

```bash
cd agent-core
python incident_creator.py
```

**What it does:**
- Creates a new incident if none exists
- Correlates with existing **OPEN** incidents if detected

---

### 3️⃣ Generate Structured RCA

```bash
python incident_rca_generator.py
```

**What it does:**
- Invokes local LLM
- Generates structured RCA
- Validates and stores machine-readable JSON

---

## 📄 Sample RCA Output

```json
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
```

---

## 🔐 Security & Data Safety

- All AI inference runs **locally**
- **No external API calls**
- No incident data committed to Git
- Safe AI boundaries with strict validation

---

## 🛣️ Roadmap

- RCA confidence scoring
- Multi-incident reasoning
- Automated remediation with guardrails
- ITSM tool integrations

---

## 👤 Author

**Pratik Rathod**  
Software Engineer | Production Support | AIOps Enthusiast

---

## ⭐ Final Note

**AegisOps** demonstrates how GenAI can be responsibly integrated into  
production-grade systems using clean design, structured data,  
and enterprise ITSM principles.
