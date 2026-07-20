import { useChat } from "../hooks/useChat";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";

export default function SupportChatPage({ user, onLogout, onViewAnalytics }) {
  const { messages, isTyping, send, submitFeedback } = useChat();

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-100">
      <div className="flex h-[640px] w-[420px] flex-col overflow-hidden rounded-2xl bg-white shadow-xl">
        <header className="flex items-center justify-between bg-brand-500 px-5 py-4 text-white">
          <div>
            <h1 className="text-base font-semibold">TechMart Support Assistant</h1>
            <p className="text-xs opacity-85">
              Multi-Agent AI • Billing · Technical · Product · Complaints · FAQ
            </p>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={onViewAnalytics}
              className="rounded-full bg-white/15 px-3 py-1 text-xs hover:bg-white/25"
            >
              Analytics
            </button>
            <button
              onClick={onLogout}
              className="rounded-full bg-white/15 px-3 py-1 text-xs hover:bg-white/25"
              title={user?.email}
            >
              Log out
            </button>
          </div>
        </header>

        <ChatWindow messages={messages} isTyping={isTyping} onFeedback={submitFeedback} />
        <ChatInput onSend={send} disabled={isTyping} />
      </div>
    </div>
  );
}
