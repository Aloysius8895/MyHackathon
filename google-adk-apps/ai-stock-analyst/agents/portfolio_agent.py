from typing import Literal

class PortfolioAdvisor:
    def recommend_allocation(
        self,
        risk_profile: Literal["low", "medium", "high"],
        insights: str
    ) -> str:
        base_strategy = {
            "low": "60% bonds, 30% large-cap, 10% cash",
            "medium": "50% stocks, 40% ETFs, 10% crypto",
            "high": "70% growth stocks, 20% sector ETFs, 10% derivatives"
        }.get(risk_profile, "50% stocks, 50% bonds")
        
        return f"""Based on {risk_profile} risk profile:
        Recommended Allocation: {base_strategy}
        AI Insights: {insights}"""
