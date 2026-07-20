import { useState, useEffect, useCallback } from "react";
import { loginUser, registerUser } from "../services/auth";

const TOKEN_KEY = "techmart_token";
const USER_KEY = "techmart_user";

export function useAuth() {
  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  // Restore session on page load
  useEffect(() => {
    const storedToken = localStorage.getItem(TOKEN_KEY);
    const storedUser = localStorage.getItem(USER_KEY);
    if (storedToken && storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const persistSession = (data) => {
    localStorage.setItem(TOKEN_KEY, data.access_token);
    localStorage.setItem(USER_KEY, JSON.stringify({ name: data.name, email: data.email }));
    setUser({ name: data.name, email: data.email });
  };

  const login = useCallback(async (email, password) => {
    setError(null);
    setLoading(true);
    try {
      const data = await loginUser(email, password);
      persistSession(data);
      return true;
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed. Please try again.");
      return false;
    } finally {
      setLoading(false);
    }
  }, []);

  const register = useCallback(async (name, email, password) => {
    setError(null);
    setLoading(true);
    try {
      const data = await registerUser(name, email, password);
      persistSession(data);
      return true;
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed. Please try again.");
      return false;
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    localStorage.removeItem("techmart_session_id");
    setUser(null);
  }, []);

  return { user, error, loading, login, register, logout };
}
