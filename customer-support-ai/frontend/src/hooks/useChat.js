import { useState, useEffect, useCallback } from "react";
import { sendMessage, sendFeedback } from "../services/api";

const SESSION_STORAGE_KEY = "techmart_session_id";

export function useChat() {
  const [messages, setMessages] = useState([
    {
      role: "bot",
      text: "Hi! I'm TechMart's AI support assistant. Ask me about billing, orders, products, or anything else.",
    },
  ]);
  const [sessionId, setSessionId] = useState(null);
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const stored = localStorage.getItem(SESSION_STORAGE_KEY);
    if (stored) setSessionId(stored);
  }, []);

  const send = useCallback(
    async (text) => {
      if (!text.trim()) return;

      setMessages((prev) => [...prev, { role: "user", text }]);
      setIsTyping(true);
      setError(null);

      try {
        const data = await sendMessage(sessionId, text);
        setSessionId(data.session_id);
        localStorage.setItem(SESSION_STORAGE_KEY, data.session_id);

        setMessages((prev) => [
          ...prev,
          {
            role: "bot",
            text: data.answer,
            agentsUsed: data.agents_used,
            escalated: data.escalated,
          },
        ]);
      } catch (err) {
        setError("Couldn't reach the server. Is the backend running on localhost:8000?");
        setMessages((prev) => [
          ...prev,
          { role: "bot", text: "Sorry, I couldn't reach the server. Please check the backend is running." },
        ]);
      } finally {
        setIsTyping(false);
      }
    },
    [sessionId]
  );

  const submitFeedback = useCallback(
    async (agent, rating) => {
      try {
        await sendFeedback(sessionId, agent, rating);
      } catch (err) {
        // feedback failing silently is fine -- not critical to the chat flow
        console.error("Feedback submission failed:", err);
      }
    },
    [sessionId]
  );

  return { messages, isTyping, error, send, submitFeedback };
}
