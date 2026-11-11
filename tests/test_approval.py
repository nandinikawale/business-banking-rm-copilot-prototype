import pytest

from rm_copilot.approval import HumanApprovalService
from rm_copilot.models import ApprovalRequest, BriefingRequest


def test_action_requires_explicit_human_decision(orchestrator, customer_id) -> None:
    briefing = orchestrator.create_briefing(
        BriefingRequest(customer_id=customer_id, as_of_month="2025-12-01")
    )
    action = briefing.proposed_actions[0]
    assert action.status == "pending_human_approval"
    record = HumanApprovalService().decide(
        briefing,
        ApprovalRequest(action_id=action.action_id, decision="approved", reviewer="Test RM"),
    )
    assert action.status == "approved"
    assert "no external action was executed" in record.audit_message


def test_action_cannot_be_decided_twice(orchestrator, customer_id) -> None:
    briefing = orchestrator.create_briefing(
        BriefingRequest(customer_id=customer_id, as_of_month="2025-12-01")
    )
    action = briefing.proposed_actions[0]
    service = HumanApprovalService()
    request = ApprovalRequest(action_id=action.action_id, decision="rejected", reviewer="Test RM")
    service.decide(briefing, request)
    with pytest.raises(ValueError, match="already has a decision"):
        service.decide(briefing, request)
