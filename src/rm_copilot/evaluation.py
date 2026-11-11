from rm_copilot.config import settings
from rm_copilot.factory import build_orchestrator
from rm_copilot.models import BriefingRequest


def evaluate() -> dict:
    orchestrator = build_orchestrator()
    customer_ids = orchestrator.tools.repository.customers()["customer_id"].head(10).tolist()
    results = []
    for customer_id in customer_ids:
        briefing = orchestrator.create_briefing(
            BriefingRequest(customer_id=customer_id, as_of_month=settings.default_month)
        )
        results.append(
            {
                "customer_id": customer_id,
                "all_tools_completed": len(briefing.trace) == 6
                and all(item.status == "completed" for item in briefing.trace),
                "citations_present": len(briefing.citations) >= 7,
                "all_actions_pending": all(
                    item.status == "pending_human_approval" for item in briefing.proposed_actions
                ),
                "limitations_present": bool(briefing.limitations),
            }
        )
    metrics = {
        key: sum(bool(item[key]) for item in results) / len(results)
        for key in [
            "all_tools_completed",
            "citations_present",
            "all_actions_pending",
            "limitations_present",
        ]
    }
    return {"cases": len(results), "metrics": metrics, "details": results}
