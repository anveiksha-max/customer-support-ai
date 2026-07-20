# wrapper around groq's llama 3, using langchain so we get proper prompt templates
# get a free key at console.groq.com/keys

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

_api_key = os.getenv("GROQ_API_KEY")
MODEL = "llama-3.1-8b-instant"

_llm = ChatGroq(model=MODEL, api_key=_api_key, temperature=0.3) if _api_key else None

_prompt_template = ChatPromptTemplate.from_messages([
    ("system", "{system_prompt}"),
    ("human", "{user_message}"),
])


def chat(system_prompt: str, user_message: str, temperature: float = 0.3) -> str:
    """Send a single-turn chat request through LangChain and return the text response."""
    if _llm is None:
        return (
            "[LLM not configured] Please add your GROQ_API_KEY to the .env file. "
            "Get a free key at https://console.groq.com/keys"
        )
    try:
        llm_with_temp = _llm.bind(temperature=temperature)
        chain = _prompt_template | llm_with_temp
        response = chain.invoke({"system_prompt": system_prompt, "user_message": user_message})
        return response.content.strip()
    except Exception as e:
        return f"[LLM error] {e}"
