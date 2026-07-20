from backend.agents.base_agent import BaseAgent


class FAQAgent(BaseAgent):
    name = "FAQ Agent"
    system_prompt = (
        "You are the FAQ Agent for TechMart Electronics customer support. "
        "You handle general company policy questions, account help, and contact information. "
        "Keep responses under 100 words and friendly in tone."
    )


faq_agent = FAQAgent()
