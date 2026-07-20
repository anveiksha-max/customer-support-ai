# Agent router / orchestrator
# figures out which agent(s) should handle a query, then combines their answers.
# uses the LLM to classify intent first, falls back to keyword matching if that fails

from backend import llm
from backend.agents.billing import billing_agent
from backend.agents.technical import technical_agent
from backend.agents.product import product_agent
from backend.agents.complaint import complaint_agent
from backend.agents.faq import faq_agent

AGENTS = {
    "billing": billing_agent,
    "technical": technical_agent,
    "product": product_agent,
    "complaint": complaint_agent,
    "faq": faq_agent,
}

INTENT_CATEGORIES = list(AGENTS.keys())

# fallback classifier in case the LLM call fails (rate limit, no key, etc)
KEYWORD_MAP = {
    "billing": ["payment", "paid", "refund", "invoice", "subscription", "premium", "charge", "emi", "billing"],
    "technical": ["login", "password", "error", "bug", "install", "crash", "not working", "reset", "otp"],
    "product": ["price", "feature", "compare", "available", "specification", "spec", "stock"],
    "complaint": ["complaint", "angry", "worst", "disappointed", "unacceptable", "frustrated", "escalate"],
    "faq": ["hours", "contact", "account", "policy", "how do i", "what is"],
}

CLASSIFIER_PROMPT = f"""You are an intent classifier for a customer support system.
Classify the customer query into one or more of these categories: {', '.join(INTENT_CATEGORIES)}.
Respond with ONLY a comma-separated list of matching category names, nothing else.
If unsure, respond with "faq".
"""


def _keyword_fallback(query: str):
    lowered = query.lower()
    matches = [cat for cat, keywords in KEYWORD_MAP.items() if any(k in lowered for k in keywords)]
    return matches or ["faq"]


def detect_intent(query: str):
    raw = llm.chat(CLASSIFIER_PROMPT, query, temperature=0.0)
    if raw.startswith("[LLM"):
        return _keyword_fallback(query)

    categories = [c.strip().lower() for c in raw.replace("\n", ",").split(",")]
    valid = [c for c in categories if c in INTENT_CATEGORIES]
    return valid or _keyword_fallback(query)


def route_query(query: str, history_text: str = ""):
    intents = detect_intent(query)
    results = [AGENTS[intent].handle(query, history_text) for intent in intents]

    if len(results) == 1:
        final_answer = results[0]["answer"]
    else:
        # Multiple agents involved -- aggregate into one coherent response
        combined = "\n\n".join([f"({r['agent']}): {r['answer']}" for r in results])
        final_answer = combined

    return {
        "intents": intents,
        "agents_used": [r["agent"] for r in results],
        "answer": final_answer,
        "sources": sorted({s for r in results for s in r["sources"]}),
        "escalated": any(r.get("escalated") for r in results),
    }
