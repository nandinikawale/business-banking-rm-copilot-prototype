from rm_copilot.models import ApprovalRecord, ApprovalRequest, Briefing


class HumanApprovalService:
    def decide(self, briefing: Briefing, request: ApprovalRequest) -> ApprovalRecord:
        action = next(
            (item for item in briefing.proposed_actions if item.action_id == request.action_id),
            None,
        )
        if action is None:
            raise KeyError(f"Unknown action: {request.action_id}")
        if action.status != "pending_human_approval":
            raise ValueError("Action already has a decision")
        action.status = request.decision
        return ApprovalRecord(
            briefing_id=briefing.briefing_id,
            action_id=action.action_id,
            decision=request.decision,
            reviewer=request.reviewer,
            audit_message=f"{request.reviewer} marked {action.action_id} as {request.decision}; no external action was executed.",
        )
