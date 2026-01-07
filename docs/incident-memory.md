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
