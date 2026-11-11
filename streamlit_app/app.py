import pandas as pd
import streamlit as st

from rm_copilot.approval import HumanApprovalService
from rm_copilot.factory import build_orchestrator
from rm_copilot.models import ApprovalRequest, BriefingRequest

st.set_page_config(
    page_title="Business Banking RM Copilot Prototype", page_icon="🧭", layout="wide"
)


@st.cache_resource
def get_orchestrator():
    return build_orchestrator()


orchestrator = get_orchestrator()
approval_service = HumanApprovalService()
customers = orchestrator.tools.repository.customers().sort_values("business_name")
labels = {
    f"{row.business_name} ({row.customer_id})": row.customer_id
    for row in customers.itertuples(index=False)
}

st.title("Business Banking RM Copilot Prototype")
st.caption("Controlled customer briefing workflow over entirely fictional data and guidance")
st.warning(
    "Demonstration only. The copilot cannot approve credit, determine compliance outcomes, "
    "contact customers, or execute transactions. Human review is mandatory."
)

with st.sidebar:
    st.header("Briefing inputs")
    selected_label = st.selectbox("Fictional customer", list(labels))
    month = st.selectbox("Reporting month", ["2025-12-01", "2025-11-01", "2025-10-01"])
    request_text = st.text_area(
        "RM request",
        "Prepare a comprehensive RM relationship briefing with relevant guidance.",
        height=110,
    )
    generate = st.button("Generate controlled briefing", type="primary", use_container_width=True)

if generate:
    try:
        st.session_state.briefing = orchestrator.create_briefing(
            BriefingRequest(
                customer_id=labels[selected_label],
                as_of_month=month,
                request_text=request_text,
            )
        )
        st.session_state.decisions = []
    except ValueError as exc:
        st.error(str(exc))

briefing = st.session_state.get("briefing")
if briefing is None:
    st.info("Select a fictional customer and generate a briefing.")
    st.stop()

st.subheader(briefing.headline)
st.caption(f"Briefing ID: {briefing.briefing_id} · As of {briefing.as_of_month}")

summary_tab, guidance_tab, actions_tab, trace_tab = st.tabs(
    ["Briefing", "Guidance & citations", "Human approval", "Tool trace"]
)

with summary_tab:
    left, right = st.columns(2)
    with left:
        st.markdown("### Observed facts")
        for fact in briefing.observed_facts:
            st.markdown(f"- {fact}")
    with right:
        st.markdown("### Rule-based indicators")
        for indicator in briefing.rule_based_indicators:
            st.markdown(f"- {indicator}")
    st.markdown("### Limitations")
    for limitation in briefing.limitations:
        st.markdown(f"- {limitation}")

with guidance_tab:
    st.markdown("### Retrieved fictional guidance")
    for item in briefing.retrieved_guidance:
        st.markdown(f"- {item}")
    st.markdown("### Evidence register")
    st.dataframe(
        pd.DataFrame([item.model_dump() for item in briefing.citations]), use_container_width=True
    )

with actions_tab:
    st.markdown("### Proposed actions")
    st.caption(
        "A decision updates only this local session. It does not execute an external action."
    )
    reviewer = st.text_input("Reviewer name", value="Relationship Manager")
    for action in briefing.proposed_actions:
        with st.container(border=True):
            st.markdown(f"**{action.action_id}: {action.description}**")
            st.write(action.reason)
            st.caption(f"Status: {action.status}")
            if action.status == "pending_human_approval":
                approve_col, reject_col = st.columns(2)
                if approve_col.button("Approve", key=f"approve-{action.action_id}"):
                    record = approval_service.decide(
                        briefing,
                        ApprovalRequest(
                            action_id=action.action_id, decision="approved", reviewer=reviewer
                        ),
                    )
                    st.session_state.decisions.append(record.model_dump())
                    st.rerun()
                if reject_col.button("Reject", key=f"reject-{action.action_id}"):
                    record = approval_service.decide(
                        briefing,
                        ApprovalRequest(
                            action_id=action.action_id, decision="rejected", reviewer=reviewer
                        ),
                    )
                    st.session_state.decisions.append(record.model_dump())
                    st.rerun()
    if st.session_state.get("decisions"):
        st.markdown("### Decision audit")
        st.dataframe(pd.DataFrame(st.session_state.decisions), use_container_width=True)

with trace_tab:
    st.markdown("### Allowlisted read-only tool execution")
    st.dataframe(
        pd.DataFrame([item.model_dump() for item in briefing.trace]), use_container_width=True
    )
    st.code(" → ".join(item.tool for item in briefing.trace), language=None)
