import { useState } from "react";

export default function MessageBubble({ role, text, agentsUsed, escalated, onFeedback }) {
  const isUser = role === "user";
  const [feedbackGiven, setFeedbackGiven] = useState(null); // "up" | "down" | null

  const handleFeedback = (rating) => {
    if (feedbackGiven || !onFeedback) return; // one rating per message
    setFeedbackGiven(rating);
    onFeedback(rating);
  };

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed whitespace-pre-wrap
          ${isUser
            ? "bg-brand-500 text-white rounded-br-sm"
            : "bg-white text-slate-800 shadow-sm rounded-bl-sm"
          }`}
      >
        {text}
        {agentsUsed && agentsUsed.length > 0 && (
          <div className={`mt-1.5 flex items-center justify-between text-xs ${escalated ? "text-red-600 font-semibold" : "text-slate-400"}`}>
            <span>
              Handled by: {agentsUsed.join(", ")}
              {escalated && " • ESCALATED to human agent"}
            </span>
            <span className="ml-2 flex gap-1">
              <button
                onClick={() => handleFeedback("up")}
                className={`rounded px-1 ${feedbackGiven === "up" ? "opacity-100" : "opacity-40 hover:opacity-70"}`}
                title="Helpful"
              >
                👍
              </button>
              <button
                onClick={() => handleFeedback("down")}
                className={`rounded px-1 ${feedbackGiven === "down" ? "opacity-100" : "opacity-40 hover:opacity-70"}`}
                title="Not helpful"
              >
                👎
              </button>
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
