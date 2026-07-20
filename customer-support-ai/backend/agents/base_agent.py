from backend import llm
from backend.rag.retriever import retriever


class BaseAgent:
    # every agent shares this same retrieve -> prompt -> LLM flow
    # only the system_prompt changes per agent

    name = "Base Agent"
    system_prompt = "You are a helpful customer support assistant for TechMart Electronics."

    def handle(self, query: str, history_text: str = "") -> dict:
        retrieved = retriever.retrieve(query, top_k=3)
        context_text = "\n\n".join([f"[{r['source']}]: {r['text']}" for r in retrieved])

        full_prompt = f"""Conversation so far:
{history_text or '(no previous messages)'}

Relevant company documents:
{context_text or '(no matching documents found)'}

Customer query:
{query}

Answer the customer clearly and concisely using the documents above where relevant.
If the documents don't cover the question, say so honestly and offer to escalate to a human agent.
"""
        answer = llm.chat(self.system_prompt, full_prompt)
        return {
            "agent": self.name,
            "answer": answer,
            "sources": list({r["source"] for r in retrieved}),
        }
