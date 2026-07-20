from backend.agents.base_agent import BaseAgent

ESCALATION_KEYWORDS = [
    "lawyer", "legal action", "sue", "consumer court", "fraud",
    "scam", "worst service", "never buying", "cancel my account",
    "extremely angry", "unacceptable", "third time", "again and again",
]


class ComplaintAgent(BaseAgent):
    name = "Complaint Agent"
    system_prompt = (
        "You are the Complaint Agent for TechMart Electronics customer support. "
        "You handle dissatisfied customers with empathy and professionalism. "
        "Acknowledge frustration genuinely, apologize where appropriate, and explain next steps clearly. "
        "Do not make promises the company documents do not support. "
        "Keep responses under 120 words."
    )

    def handle(self, query: str, history_text: str = "") -> dict:
        result = super().handle(query, history_text)
        result["escalated"] = self._should_escalate(query)
        if result["escalated"]:
            result["answer"] += (
                "\n\nThis case has been flagged for escalation to a human support "
                "specialist, who will follow up within 24 hours."
            )
        return result

    def _should_escalate(self, query: str) -> bool:
        lowered = query.lower()
        return any(keyword in lowered for keyword in ESCALATION_KEYWORDS)


complaint_agent = ComplaintAgent()
