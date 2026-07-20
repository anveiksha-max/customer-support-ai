import { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble";

export default function ChatWindow({ messages, isTyping, onFeedback }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  return (
    <div className="flex-1 overflow-y-auto scrollbar-thin bg-slate-50 p-4 space-y-3">
      {messages.map((m, i) => (
        <MessageBubble
          key={i}
          {...m}
          onFeedback={
            m.role === "bot" && m.agentsUsed
              ? (rating) => onFeedback(m.agentsUsed.join(","), rating)
              : undefined
          }
        />
      ))}
      {isTyping && (
        <div className="text-xs text-slate-400 pl-1">Assistant is typing...</div>
      )}
      <div ref={bottomRef} />
    </div>
  );
}
