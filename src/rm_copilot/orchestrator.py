from __future__ import annotations

import hashlib

from rm_copilot.models import Briefing, BriefingRequest, ProposedAction, ToolTrace
from rm_copilot.tools import ReadOnlyRMTools

BLOCKED_PATTERNS = {
    "ignore previous instructions",
    "reveal secrets",
    "contact the customer",
    "approve the loan",
    "transfer funds",
    "bypass approval",
}


class ControlledBriefingOrchestrator:
    TOOL_SEQUENCE = (
        "customer_profile",
        "deposit_analysis",
        "credit_exposure",
        "profitability_analysis",
        "opportunity_analysis",
        "knowledge_retrieval",
    )

    def __init__(self, tools: ReadOnlyRMTools) -> None:
        self.tools = tools

    def create_briefing(self, request: BriefingRequest) -> Briefing:
        lowered = request.request_text.lower()
        blocked = [pattern for pattern in BLOCKED_PATTERNS if pattern in lowered]
        if blocked:
            raise ValueError(f"Request blocked by safety policy: {blocked[0]}")

        results = [
            self.tools.customer_profile(request.customer_id, request.as_of_month),
            self.tools.deposit_analysis(request.customer_id, request.as_of_month),
            self.tools.credit_exposure(request.customer_id, request.as_of_month),
            self.tools.profitability_analysis(request.customer_id, request.as_of_month),
            self.tools.opportunity_analysis(request.customer_id, request.as_of_month),
            self.tools.knowledge_retrieval(request.request_text),
        ]
        profile, deposits, credit, profit, opportunities, guidance = results
        facts = [profile.summary, deposits.summary, credit.summary, profit.summary]
        indicators = []
        if deposits.facts["attrition_indicator"]:
            indicators.append(
                "Sustained deposit-decline rule is active; this is a review prompt, not proof of attrition."
            )
        if opportunities.facts["product_gaps"]:
            indicators.append(
                opportunities.summary + " These are conversation prompts, not recommendations."
            )
        if not indicators:
            indicators.append(
                "No retention or product-gap indicator is active for the selected month."
            )

        actions = [
            ProposedAction(
                action_id="ACT-REVIEW",
                description="Review the briefing and validate customer context before any outreach.",
                reason="Analytics and retrieved guidance require RM interpretation.",
            )
        ]
        if deposits.facts["attrition_indicator"]:
            actions.append(
                ProposedAction(
                    action_id="ACT-DEPOSIT",
                    description="Prepare neutral questions about recent cash-flow and deposit movement.",
                    reason="A sustained deposit-decline indicator is active.",
                )
            )
        if opportunities.facts["product_gaps"]:
            actions.append(
                ProposedAction(
                    action_id="ACT-PRODUCT",
                    description="Validate the identified operating need before involving a product specialist.",
                    reason="One or more transparent product-gap rules are active.",
                )
            )

        digest = hashlib.sha256(
            f"{request.customer_id}|{request.as_of_month}".encode()
        ).hexdigest()[:10]
        return Briefing(
            briefing_id=f"BRF-{digest.upper()}",
            customer_id=request.customer_id,
            as_of_month=request.as_of_month,
            headline=f"RM briefing for {profile.facts['business_name']}",
            observed_facts=facts,
            rule_based_indicators=indicators,
            retrieved_guidance=[
                f"{item['title']} — {item['section']} (relevance {item['relevance']:.2f})"
                for item in guidance.facts["matches"]
            ],
            proposed_actions=actions,
            citations=[citation for result in results for citation in result.citations],
            trace=[
                ToolTrace(
                    sequence=index,
                    tool=result.tool,
                    status="completed",
                    rationale="Allowlisted read-only tool",
                )
                for index, result in enumerate(results, start=1)
            ],
            limitations=[
                "All customers, balances, policies, and indicators are fictional.",
                "The copilot does not approve credit, determine compliance outcomes, contact customers, or execute transactions.",
                "An RM must validate facts, applicability, suitability, and approvals.",
            ],
        )
