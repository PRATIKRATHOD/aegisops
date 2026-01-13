import subprocess
import time

AGENTS = [
    "incident_creator.py",
    "incident_rca_generator.py",
    "action_planner.py",
    "execution_engine.py",
    "self_healing_orchestrator.py",
    "postmortem_generator.py",
    "incident_notifier.py"
]

def run_agent(agent):
    print(f"\n🚀 Running {agent}")
    result = subprocess.run(
        ["python", agent],
        capture_output=True,
        text=True
    )

    if result.stdout:
        print("OUTPUT:\n", result.stdout)
    if result.stderr:
        print("ERRORS:\n", result.stderr)

    print(f"✔ Completed: {agent}")
    print("-" * 50)
    time.sleep(1)

def main():
    print("\n🔵 Starting AegisOps Agent Pipeline...\n")

    for agent in AGENTS:
        run_agent(agent)

    print("\n🎉 Pipeline Completed Successfully\n")

if __name__ == "__main__":
    main()
