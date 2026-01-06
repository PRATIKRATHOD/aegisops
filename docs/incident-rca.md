# Incident Root Cause Analysis (RCA) – AegisOps

## Overview

This document describes how AegisOps generates, validates, and stores
Root Cause Analysis (RCA) for production incidents using a local,
open-source GenAI model.

The RCA process is designed to be:
- Structured (machine-readable)
- Safe (validated and fault-tolerant)
- Vendor-agnostic
- Aligned with real enterprise ITSM practices

---

## Why RCA Is Important

In enterprise production environments, resolving incidents is not enough.
Teams must understand:
- Why the incident occurred
- Which component was affected
- What evidence supports the analysis
- What actions should be taken next

A structured RCA enables:
- Faster incident resolution
- Knowledge reuse
- Automation readiness
- ITSM and reporting integration

---

## Design Principles

The RCA system in AegisOps follows these principles:

- **AI assists analysis, not execution**
- **Raw AI output is never trusted blindly**
- **All RCA data must be structured and validated**
- **Failures are captured safely without data loss**
- **No external APIs or paid services are used**

---

## RCA Generation Flow

The RCA pipeline is executed using a single script:

# incident_rca_generator.py


### High-Level Flow

1. Load the most recent incident from storage
2. Build a structured prompt using incident data
3. Invoke a local LLM (Mistral via Ollama)
4. Receive AI-generated RCA output
5. Extract and parse JSON from the AI response
6. Validate required RCA fields
7. Store RCA as structured JSON within the incident

This ensures that every RCA is consistent and automation-ready.

---

## AI Model & Execution

### Model Used
- **Mistral** (open-source LLM)
- Executed locally using **Ollama**

### Why Local AI
- No internet dependency
- No data leakage
- No API costs
- Enterprise security compliant

### Integration Method
- Python `subprocess` is used to invoke the LLM
- Keeps AI runtime decoupled from application logic

---

## RCA Prompt Strategy

The AI is instructed to behave as a:
> *Senior Site Reliability Engineer*

The prompt explicitly enforces:
- Output in **strict JSON format**
- A predefined set of RCA fields
- No free-text explanations

This minimizes hallucinations and ensures predictable output.

---

## RCA Schema (Final Structured Format)

Each incident contains an `rca` object in the following format:

```json
"rca": {
  "generated_at": "ISO-8601 timestamp",
  "root_cause_type": "Category of root cause",
  "affected_component": "System or component impacted",
  "probable_cause": "Most likely underlying cause",
  "evidence": [
    "Log lines or signals supporting the analysis"
  ],
  "impact": "Business or system impact",
  "recommended_next_steps": [
    "Actionable remediation or investigation steps"
  ]
}
