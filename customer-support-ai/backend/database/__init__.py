# mongodb connection + helper functions for users and chat history
# need MONGODB_URI set in .env (free cluster from mongodb atlas)

import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME", "techmart_support")

_client = MongoClient(MONGODB_URI) if MONGODB_URI else None
_db = _client[DB_NAME] if _client is not None else None

users_collection = _db["users"] if _db is not None else None
messages_collection = _db["messages"] if _db is not None else None
feedback_collection = _db["feedback"] if _db is not None else None


def is_connected() -> bool:
    return _db is not None


# users (for login/register)

def create_user(name: str, email: str, hashed_password: str):
    user = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "created_at": datetime.utcnow().isoformat(),
    }
    users_collection.insert_one(user)
    return user


def get_user_by_email(email: str):
    return users_collection.find_one({"email": email})


# chat history

def save_message(session_id: str, role: str, content: str, agent: str = None):
    messages_collection.insert_one({
        "session_id": session_id,
        "role": role,
        "content": content,
        "agent": agent,
        "timestamp": datetime.utcnow().isoformat(),
    })


def get_history(session_id: str, limit: int = 20):
    cursor = messages_collection.find({"session_id": session_id}).sort("_id", 1).limit(limit)
    return [
        {
            "role": m["role"],
            "content": m["content"],
            "agent": m.get("agent"),
            "timestamp": m["timestamp"],
        }
        for m in cursor
    ]


# customer satisfaction feedback (thumbs up/down per response)

def save_feedback(session_id: str, agent: str, rating: str):
    # rating is either "up" or "down"
    feedback_collection.insert_one({
        "session_id": session_id,
        "agent": agent,
        "rating": rating,
        "timestamp": datetime.utcnow().isoformat(),
    })


def get_analytics():
    total_conversations = len(messages_collection.distinct("session_id"))
    total_messages = messages_collection.count_documents({"role": "user"})

    # how many times each agent has been used
    agent_usage = {}
    for doc in messages_collection.find({"role": "assistant", "agent": {"$ne": None}}):
        for agent_name in doc["agent"].split(","):
            agent_usage[agent_name] = agent_usage.get(agent_name, 0) + 1

    total_feedback = feedback_collection.count_documents({})
    thumbs_up = feedback_collection.count_documents({"rating": "up"})
    satisfaction_rate = round((thumbs_up / total_feedback) * 100, 1) if total_feedback > 0 else None

    return {
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "agent_usage": agent_usage,
        "total_feedback": total_feedback,
        "thumbs_up": thumbs_up,
        "thumbs_down": total_feedback - thumbs_up,
        "satisfaction_rate": satisfaction_rate,
    }
