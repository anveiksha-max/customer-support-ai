import { useEffect, useState } from "react";
import { getAnalytics } from "../services/api";

export default function AnalyticsPage({ onBack }) {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getAnalytics()
      .then(setStats)
      .catch(() => setError("Couldn't load analytics. Is the backend running?"));
  }, []);

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-100">
      <div className="w-[420px] rounded-2xl bg-white p-6 shadow-xl">
        <div className="mb-4 flex items-center justify-between">
          <h1 className="text-lg font-semibold text-slate-800">Analytics</h1>
          <button onClick={onBack} className="text-sm text-brand-500 hover:underline">
            Back to chat
          </button>
        </div>

        {error && <p className="text-sm text-red-600">{error}</p>}

        {!stats && !error && <p className="text-sm text-slate-500">Loading...</p>}

        {stats && (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <StatCard label="Conversations" value={stats.total_conversations} />
              <StatCard label="Messages" value={stats.total_messages} />
            </div>

            <div>
              <h2 className="mb-2 text-sm font-medium text-slate-600">Agent usage</h2>
              {Object.keys(stats.agent_usage).length === 0 ? (
                <p className="text-sm text-slate-400">No data yet.</p>
              ) : (
                <div className="space-y-1.5">
                  {Object.entries(stats.agent_usage).map(([agent, count]) => (
                    <div key={agent} className="flex items-center justify-between text-sm">
                      <span className="text-slate-700">{agent}</span>
                      <span className="font-medium text-slate-900">{count}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div>
              <h2 className="mb-2 text-sm font-medium text-slate-600">Customer satisfaction</h2>
              {stats.satisfaction_rate === null ? (
                <p className="text-sm text-slate-400">No feedback submitted yet.</p>
              ) : (
                <div className="text-sm text-slate-700">
                  <span className="text-2xl font-semibold text-slate-900">{stats.satisfaction_rate}%</span>
                  <span className="ml-2 text-slate-500">
                    ({stats.thumbs_up} 👍 / {stats.thumbs_down} 👎)
                  </span>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function StatCard({ label, value }) {
  return (
    <div className="rounded-lg bg-slate-50 p-3 text-center">
      <div className="text-2xl font-semibold text-slate-900">{value}</div>
      <div className="text-xs text-slate-500">{label}</div>
    </div>
  );
}
