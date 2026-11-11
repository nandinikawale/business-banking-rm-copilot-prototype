# Architecture and control boundaries

## Workflow

```text
RM request
   │
   ▼
request validation and safety patterns
   │
   ▼
fixed state machine
   ├── customer profile tool ───────┐
   ├── deposit analysis tool ──────┤
   ├── credit exposure tool ───────┤
   ├── profitability tool ─────────┼── evidence register
   ├── opportunity tool ───────────┤
   └── knowledge retrieval tool ───┘
   │
   ▼
briefing: facts + indicators + guidance + proposed actions
   │
   ▼
human approval or rejection
   │
   ▼
local audit record; no external banking action
```

## Trust boundaries

- CSV analytics and document retrieval are read-only.
- Tool names and execution order are allowlisted in code.
- User text cannot introduce a new tool.
- Known unsafe requests are blocked before tool execution.
- Every proposed action starts as `pending_human_approval`.
- A decision changes only in-memory application state.
- No email, CRM, payment, underwriting, or customer-contact integration exists.

## Evidence model

The briefing keeps four concepts separate:

1. **Observed facts** come from customer-specific CSV records.
2. **Rule-based indicators** come from transparent fictional analytics rules.
3. **Retrieved guidance** comes from fictional versioned knowledge documents.
4. **Proposed actions** are review suggestions that require a named human decision.

This separation prevents a product-gap flag or retrieved paragraph from being represented as
an approved customer recommendation.
