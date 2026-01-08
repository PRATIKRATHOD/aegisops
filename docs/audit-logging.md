## 📜 Audit Logging Engine

### Purpose
Maintain a complete audit trail of every agent action, ensuring
transparency, compliance, and traceability.

### What It Logs
- RCA generation
- Confidence scoring
- Agent decisions
- Action recommendations
- Action plan creation
- Execution simulation events

### What It Does Not Log
- No sensitive data
- No runtime secrets
- No system environment details

### Output
Writes a timestamped audit entry into `audit_log.json`.

### Benefits
- ITIL-compliant traceability  
- Enterprise readiness  
- Full event history for debugging and reporting
