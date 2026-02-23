## NormalObjects – Strict Complaint Processor (LangGraph)
Overview
- This project implements Bloyce’s Protocol, a structured, rule-based complaint processing system for the Downside Up Complaint Bureau.
Unlike the creative LangChain agent from Lab 1, this system uses LangGraph to enforce a deterministic workflow:

intake → validate → investigate → resolve → close

## The implementation demonstrates:

Structured state management

Conditional routing

Rule enforcement

Audit-friendly execution tracing

Deterministic workflow control

## Objectives
- Build a structured agent workflow using a LangGraph state machine
- Implement defined nodes and conditional edges
- Enforce rule-based complaint processing
- Manage shared state across workflow steps
- Compare structured LangGraph orchestration vs freeform LangChain agents

## Workflow Design
Bloyce’s Protocol enforces the following mandatory flow:

1.Intake
2. Validate
3. Investigate
4. Resolve
5. Close

No complaint can skip steps.

Conditional routing occurs after validation:
- Invalid complaints → Rejected
- “Other” category complaints → Escalated for manual review
- Valid complaints → Proceed to investigation

## Project Structure

normalobjects_langgraph_protocol/
src/normalobjects_langgraph/
state.py – ComplaintState TypedDict definition
rules.py – Bloyce’s Protocol rule enforcement
nodes.py – Workflow node implementations
graph.py – LangGraph state machine wiring
visualizer.py – Workflow path summarization
data.py – Sample test complaints
scripts/
run_workflow.py – CLI entry point
requirements.txt
.gitignore

## State Management
All workflow steps operate on a shared ComplaintState object.
The state tracks:
complaint text
category
validation status
investigation evidence
resolution details
effectiveness rating
timestamps
workflow path (audit trail)
execution logs

Each node reads the state, updates it, and returns the modified version.

This ensures full traceability and deterministic behavior.

## How to Run

Install dependencies:
pip install -r requirements.txt
Create a .env file in the project root:
OPENAI_API_KEY=your_key_here
Run the workflow:
PYTHONPATH=src python scripts/run_workflow.py

## Example Output
Valid complaint:
Path: intake → validate → investigate → resolve → close
Category: portal
Status: close
Valid: True
Effectiveness: medium

Invalid complaint:
Path: intake → validate
Category: other
Status: escalated
Valid: False

## Bloyce’s Protocol Rule Enforcement
# Intake Rules
Categorize complaint into exactly one of:
portal
monster
psychic
environmental

other
Extract essential details
Flag insufficient detail

# Validation Rules
Category-specific validation logic
“Other” category auto-escalates
Complaints missing essential details are rejected

# Investigation Rules
Investigation must produce documented evidence
No investigation without successful validation

# Resolution Rules
Resolution must reference Downside Up procedures
Effectiveness rating assigned (high / medium / low)
Certain categories may require escalation

# Closure Rules
Confirmation of resolution application
Customer satisfaction verification attempt
Timestamp logging
Audit trail preserved

## LangGraph vs LangChain (Lab Comparison)
LangChain (Lab 1 – Creative Agent)
- Flexible reasoning
- Open-ended responses
- Tool usage driven by LLM decisions
- Harder to audit
- Less deterministic

LangGraph (Lab 2 – Structured Workflow)
- Explicit state machine
- Defined nodes and edges
- Conditional routing
- Full audit trail
- Deterministic and compliance-friendly

# When to Use Each
Use LangChain when:
Creative reasoning is required
Flexible problem-solving is needed
Exploration matters more than strict process

Use LangGraph when:
- Compliance and traceability are required
- Workflows must follow strict steps
- Deterministic outcomes are critical
- Auditability is important

## Success Criteria Achieved
LangGraph state machine successfully implemented
Workflow strictly follows intake → validate → investigate → resolve → close
State properly managed across nodes
Handles valid and invalid complaints
Provides traceable workflow path visualization

Author
April Atkinson

