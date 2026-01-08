## 🧠 Incident Knowledge Base (Memory Engine)

### Purpose
Enable AegisOps to learn from past incidents and reuse previous RCA
and action recommendations.

### What It Does
- Stores historical incidents and RCA summaries
- Detects similar incidents based on error patterns
- Reuses known RCA and actions when applicable
- Improves confidence scoring automatically

### Benefits
- Faster RCA for repeated incidents
- Reduced SME dependency
- Enterprise-ready learning behavior

### Current Scope
- Read-only memory
- No automatic overwrites
- Used as decision-support only

### Future
- Vector similarity (RAG)
- Confidence boosting from history
- Cross-incident pattern detection

### 🔥 Confidence Boosting from Memory

If a new incident matches a previous incident in the knowledge base,
AegisOps automatically boosts the RCA confidence score.

Benefits:
- Faster RCA for repeated issues
- Trust based on historical patterns
- Lower SME dependency

Boost Logic:
- +0.10 confidence for a memory match
- Capped at 0.95 for safety

