# Business Banking RM Copilot Prototype

A controlled agentic workflow that prepares explainable Relationship Manager briefings by
combining fictional customer analytics with fictional policy and product guidance.

> **Safety and data statement:** Every customer, balance, identifier, policy, rule, and
> example is fictional. The repository contains no real customer information, internal bank
> documents, credentials, or confidential business rules.

## Business problem

Relationship Managers often assemble customer facts, financial movements, product gaps,
and procedural guidance from different sources before a relationship review. This prototype
demonstrates how an AI-assisted workflow can coordinate those read-only tasks while retaining
evidence, control boundaries, and human accountability.

The copilot does not approve credit, determine compliance outcomes, contact customers,
update a CRM, or execute transactions.

## Capabilities

- Select a fictional customer and reporting month.
- Execute six allowlisted read-only tools in a visible sequence.
- Analyze deposits, credit exposure, profitability, and transparent product-gap indicators.
- Retrieve relevant fictional RM guidance with document-section citations.
- Separate observed facts, rules, guidance, and proposed actions.
- Require an explicit named human decision for each proposed action.
- Record a local decision audit stating that no external action was executed.
- Block representative prompt-injection and unauthorized-action requests.
- Expose the workflow through Streamlit and FastAPI.
- Evaluate tool completion, citations, pending approvals, and limitations.

## Controlled workflow

```text
validated request
      ↓
profile → deposits → credit → profitability → opportunities → knowledge
      ↓
evidence-backed briefing
      ↓
pending proposed actions
      ↓
human approve/reject → local audit record only
```

See [architecture and control boundaries](docs/architecture.md) for the full design.

## Technology

- Python 3.13 and `uv`
- DuckDB and Pandas for structured analytics
- Scikit-learn feature hashing for reproducible local document retrieval
- Pydantic schemas and a deterministic state-machine orchestrator
- Streamlit interface and FastAPI service
- Pytest, Ruff, and GitHub Actions

No API key is required.

## Run locally

```powershell
git clone https://github.com/nandinikawale/business-banking-rm-copilot-prototype.git
cd business-banking-rm-copilot-prototype
py -3.13 -m pip install uv==0.12.24
py -3.13 -m uv sync --locked
py -3.13 -m uv run --locked streamlit run streamlit_app/app.py
```

Open `http://localhost:8501` and generate a briefing for any listed fictional customer.

Run the API:

```powershell
py -3.13 -m uv run --locked uvicorn rm_copilot.api:app --reload
```

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Test and evaluate

```powershell
py -3.13 -m uv run --locked ruff check .
py -3.13 -m uv run --locked ruff format --check .
py -3.13 -m uv run --locked pytest
py -3.13 -m uv run --locked rm-copilot-evaluate
```

The deterministic evaluation runs ten fictional customer briefings and checks that:

- all six allowlisted tools complete;
- citations are present;
- proposed actions remain pending human approval; and
- limitations are included.

### Baseline evaluation results

| Control metric | Result |
| --- | ---: |
| All six tools completed | 100% |
| Required citations present | 100% |
| All proposed actions pending approval | 100% |
| Limitations present | 100% |

This small deterministic benchmark verifies control behavior and does not establish
production accuracy, security, suitability, or regulatory compliance.

## Repository structure

```text
data/synthetic/       Consistent fictional 100-customer portfolio slice
data/knowledge/       Fictional policy, product, and RM guidance
src/rm_copilot/       Tools, orchestration, approval, API, and evaluation
streamlit_app/        Interactive briefing and approval interface
tests/                Orchestration, safety, and approval tests
docs/                 Architecture and control boundaries
.github/workflows/    Continuous integration
```

See [data lineage and limitations](data/README.md).

## Portfolio series

1. `business-banking-rm-intelligence-hub` — portfolio analytics and RM opportunities.
2. `business-banking-rag-knowledge-assist` — retrieval and cited fictional guidance.
3. **This repository** — controlled orchestration, evidence, and human approval.

## Limitations and future work

- The state machine is deterministic and does not use an LLM planner.
- Prompt-injection protection uses a small explicit pattern set, not a complete security layer.
- Approval state and audit records are in memory and are not durable.
- Retrieval uses local feature hashing rather than a production semantic embedding service.
- Authentication, role-based access, persistent audit storage, observability, expanded agent
  evaluation, and real service integration are intentionally absent.

## License

MIT License. Copyright (c) 2026 nandinikawale.
