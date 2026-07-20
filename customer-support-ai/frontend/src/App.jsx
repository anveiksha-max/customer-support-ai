import { useState } from "react";
import { useAuth } from "./hooks/useAuth";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import SupportChatPage from "./pages/SupportChatPage";
import AnalyticsPage from "./pages/AnalyticsPage";

function App() {
  const { user, error, loading, login, register, logout } = useAuth();
  const [view, setView] = useState("login"); // "login" | "register"
  const [showAnalytics, setShowAnalytics] = useState(false);

  if (user) {
    if (showAnalytics) {
      return <AnalyticsPage onBack={() => setShowAnalytics(false)} />;
    }
    return (
      <SupportChatPage
        user={user}
        onLogout={logout}
        onViewAnalytics={() => setShowAnalytics(true)}
      />
    );
  }

  if (view === "register") {
    return (
      <RegisterPage
        onRegister={register}
        onSwitchToLogin={() => setView("login")}
        error={error}
        loading={loading}
      />
    );
  }

  return (
    <LoginPage
      onLogin={login}
      onSwitchToRegister={() => setView("register")}
      error={error}
      loading={loading}
    />
  );
}

export default App;
