## ⚙️ Safe Execution Framework (Simulation Mode)

### Purpose
Enable AegisOps to generate safe, auditable “execution intents”
based on the action plan, without running real system commands.

### What It Does
- Reads the action plan
- Generates a simulated execution log
- Marks whether approval is required
- Does not run any command

### Safety Controls
- No real command execution
- No system modification
- Fully auditable output

### Output
Creates an `execution_preview` block in the incident record.
