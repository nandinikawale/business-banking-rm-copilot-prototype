from __future__ import annotations

from rm_copilot.knowledge import KnowledgeIndex
from rm_copilot.models import Citation, ToolResult
from rm_copilot.repository import BankingRepository


class ReadOnlyRMTools:
    def __init__(self, repository: BankingRepository, knowledge: KnowledgeIndex) -> None:
        self.repository = repository
        self.knowledge = knowledge

    def customer_profile(self, customer_id: str, as_of_month: str) -> ToolResult:
        row = self.repository.customer(customer_id)
        facts = {
            key: row[key]
            for key in ["business_name", "industry", "business_size", "region", "rm_id"]
        }
        return ToolResult(
            tool="customer_profile",
            summary=f"{row['business_name']} is a {row['business_size']} {row['industry']} business in {row['region']}.",
            facts=facts,
            citations=[
                Citation(
                    source="data/synthetic/customers.csv",
                    locator=customer_id,
                    description="Fictional customer profile",
                )
            ],
        )

    def deposit_analysis(self, customer_id: str, as_of_month: str) -> ToolResult:
        history = self.repository.history("deposits.csv", customer_id, as_of_month)
        latest = history.iloc[-1]
        prior = history.iloc[-2] if len(history) > 1 else latest
        change = float(latest["closing_balance"] - prior["closing_balance"])
        pct = change / float(prior["closing_balance"]) if float(prior["closing_balance"]) else 0.0
        facts = {
            "closing_balance": float(latest["closing_balance"]),
            "month_over_month_change": change,
            "month_over_month_change_pct": pct,
            "attrition_indicator": bool(latest["attrition_indicator"]),
        }
        return ToolResult(
            tool="deposit_analysis",
            summary=f"Closing deposits were ${facts['closing_balance']:,.0f}; monthly movement was {pct:+.1%}.",
            facts=facts,
            citations=[
                Citation(
                    source="data/synthetic/deposits.csv",
                    locator=f"{customer_id} @ {as_of_month}",
                    description="Monthly fictional deposit snapshot",
                )
            ],
        )

    def credit_exposure(self, customer_id: str, as_of_month: str) -> ToolResult:
        loan = self.repository.snapshot("loans.csv", customer_id, as_of_month)
        card = self.repository.snapshot("credit_cards.csv", customer_id, as_of_month)
        facts = {
            "has_loan": bool(loan["has_loan"]),
            "loan_balance": float(loan["closing_balance"]),
            "has_credit_card": bool(card["has_credit_card"]),
            "card_balance": float(card["closing_balance"]),
            "card_limit": float(card["credit_limit"]),
        }
        return ToolResult(
            tool="credit_exposure",
            summary=f"Loan exposure was ${facts['loan_balance']:,.0f}; card exposure was ${facts['card_balance']:,.0f}.",
            facts=facts,
            citations=[
                Citation(
                    source="data/synthetic/loans.csv",
                    locator=f"{customer_id} @ {as_of_month}",
                    description="Fictional loan snapshot",
                ),
                Citation(
                    source="data/synthetic/credit_cards.csv",
                    locator=f"{customer_id} @ {as_of_month}",
                    description="Fictional card snapshot",
                ),
            ],
        )

    def profitability_analysis(self, customer_id: str, as_of_month: str) -> ToolResult:
        row = self.repository.snapshot("profitability.csv", customer_id, as_of_month)
        facts = {
            key: float(row[key]) for key in ["total_revenue", "allocated_expenses", "profitability"]
        }
        return ToolResult(
            tool="profitability_analysis",
            summary=f"Monthly relationship profitability was ${facts['profitability']:,.0f} on revenue of ${facts['total_revenue']:,.0f}.",
            facts=facts,
            citations=[
                Citation(
                    source="data/synthetic/profitability.csv",
                    locator=f"{customer_id} @ {as_of_month}",
                    description="Fictional bank profitability snapshot",
                )
            ],
        )

    def opportunity_analysis(self, customer_id: str, as_of_month: str) -> ToolResult:
        row = self.repository.snapshot("products.csv", customer_id, as_of_month)
        gaps = [
            name.replace("_cross_sell", "")
            for name in [
                "merchant_cross_sell",
                "payroll_cross_sell",
                "treasury_cross_sell",
                "card_cross_sell",
            ]
            if bool(row[name])
        ]
        facts = {"product_count": int(row["product_count"]), "product_gaps": gaps}
        summary = (
            "Potential review areas: "
            + (", ".join(gaps) if gaps else "no rule-based product gaps")
            + "."
        )
        return ToolResult(
            tool="opportunity_analysis",
            summary=summary,
            facts=facts,
            citations=[
                Citation(
                    source="data/synthetic/products.csv",
                    locator=f"{customer_id} @ {as_of_month}",
                    description="Transparent fictional product-gap rules",
                )
            ],
        )

    def knowledge_retrieval(self, query: str) -> ToolResult:
        matches = self.knowledge.search(query)
        citations = [
            Citation(source=item["source"], locator=item["section"], description=item["title"])
            for item in matches
        ]
        facts = {"matches": matches}
        return ToolResult(
            tool="knowledge_retrieval",
            summary="Retrieved fictional RM guidance with source sections.",
            facts=facts,
            citations=citations,
        )
