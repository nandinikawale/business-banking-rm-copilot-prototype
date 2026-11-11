from fastapi import FastAPI, HTTPException

from rm_copilot.approval import HumanApprovalService
from rm_copilot.factory import build_orchestrator
from rm_copilot.models import ApprovalRecord, ApprovalRequest, Briefing, BriefingRequest

app = FastAPI(title="Business Banking RM Copilot Prototype", version="0.1.0")
orchestrator = build_orchestrator()
approval_service = HumanApprovalService()
briefings: dict[str, Briefing] = {}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/briefings", response_model=Briefing)
def create_briefing(request: BriefingRequest) -> Briefing:
    try:
        briefing = orchestrator.create_briefing(request)
    except (KeyError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    briefings[briefing.briefing_id] = briefing
    return briefing


@app.post("/briefings/{briefing_id}/decisions", response_model=ApprovalRecord)
def decide(briefing_id: str, request: ApprovalRequest) -> ApprovalRecord:
    if briefing_id not in briefings:
        raise HTTPException(status_code=404, detail="Briefing not found")
    try:
        return approval_service.decide(briefings[briefing_id], request)
    except (KeyError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
