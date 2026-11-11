from typing import Any, Literal

from pydantic import BaseModel, Field

ToolName = Literal[
    "customer_profile",
    "deposit_analysis",
    "credit_exposure",
    "profitability_analysis",
    "opportunity_analysis",
    "knowledge_retrieval",
]


class Citation(BaseModel):
    source: str
    locator: str
    description: str


class ToolResult(BaseModel):
    tool: ToolName
    summary: str
    facts: dict[str, Any]
    citations: list[Citation]


class ToolTrace(BaseModel):
    sequence: int
    tool: ToolName
    status: Literal["completed", "blocked"]
    rationale: str


class ProposedAction(BaseModel):
    action_id: str
    description: str
    reason: str
    status: Literal["pending_human_approval", "approved", "rejected"] = "pending_human_approval"


class BriefingRequest(BaseModel):
    customer_id: str = Field(pattern=r"^SYN-C\d{6}$")
    as_of_month: str = Field(pattern=r"^\d{4}-\d{2}-01$")
    request_text: str = Field(
        default="Prepare a comprehensive RM relationship briefing", max_length=500
    )


class Briefing(BaseModel):
    briefing_id: str
    customer_id: str
    as_of_month: str
    headline: str
    observed_facts: list[str]
    rule_based_indicators: list[str]
    retrieved_guidance: list[str]
    proposed_actions: list[ProposedAction]
    citations: list[Citation]
    trace: list[ToolTrace]
    limitations: list[str]


class ApprovalRequest(BaseModel):
    action_id: str
    decision: Literal["approved", "rejected"]
    reviewer: str = Field(min_length=2, max_length=80)


class ApprovalRecord(BaseModel):
    briefing_id: str
    action_id: str
    decision: Literal["approved", "rejected"]
    reviewer: str
    audit_message: str
