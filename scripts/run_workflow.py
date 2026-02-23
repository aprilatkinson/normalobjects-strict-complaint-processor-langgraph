from __future__ import annotations

from normalobjects_langgraph.graph import build_app
from normalobjects_langgraph.data import test_complaints
from normalobjects_langgraph.visualizer import summarize_run


def main():
    app = build_app()

    for i, complaint in enumerate(test_complaints, start=1):
        initial_state = {
            "complaint": complaint,
            "complainant_id": "demo-user",  # placeholder for dedupe later
            "workflow_path": [],
            "status": "new",
            "logs": [],
        }

        final_state = app.invoke(initial_state)

        print("=" * 80)
        print(f"CASE {i}: {complaint}")
        print("-" * 80)
        print(summarize_run(final_state))
        print("Logs:")
        for line in final_state.get("logs", []):
            print(" ", line)


if __name__ == "__main__":
    main()