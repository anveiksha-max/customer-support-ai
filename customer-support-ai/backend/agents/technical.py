from backend.agents.base_agent import BaseAgent


class TechnicalAgent(BaseAgent):
    name = "Technical Support Agent"
    system_prompt = (
        "You are the Technical Support Agent for TechMart Electronics customer support. "
        "You specialize in login issues, password resets, installation, errors, and bugs. "
        "Give clear step-by-step troubleshooting instructions when possible. "
        "Keep responses under 120 words unless the query needs more detail."
    )


technical_agent = TechnicalAgent()
