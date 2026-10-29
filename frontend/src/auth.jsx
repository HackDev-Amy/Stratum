import { createContext, useContext, useEffect, useState } from "react";
import api from "./api";

const AuthCtx = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const t = localStorage.getItem("access");
    if (!t) { setLoading(false); return; }
    api.get("/auth/portfolio/")
      .then(() => setUser({ token: t }))
      .catch(() => localStorage.clear())
      .finally(() => setLoading(false));
  }, []);

  const login = async (username, password) => {
    const r = await api.post("/auth/login/", { username, password });
    localStorage.setItem("access", r.data.access);
    localStorage.setItem("refresh", r.data.refresh);
    setUser({ token: r.data.access });
  };

  const register = async (username, password) => {
    await api.post("/auth/register/", { username, password });
    await login(username, password);
  };

  const logout = () => { localStorage.clear(); setUser(null); };

  return (
    <AuthCtx.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthCtx.Provider>
  );
}

export const useAuth = () => useContext(AuthCtx);