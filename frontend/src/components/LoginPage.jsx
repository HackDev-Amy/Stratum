import { useState } from "react";
import { useAuth } from "../auth";
import { toast } from "../lib/toast";

export default function LoginPage() {
  const { login, register } = useAuth();
  const [u, setU] = useState("");
  const [p, setP] = useState("");
  const [mode, setMode] = useState("login");
  const [busy, setBusy] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    try {
      if (mode === "login") await login(u, p);
      else {
        await register(u, p);
        toast("Account created", "success");
      }
    } catch (err) {
      toast(err.response?.data?.detail || "Authentication failed", "error");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 relative z-10">
      <div className="w-full max-w-md">
        <div className="text-center mb-10">
          <div className="inline-block mb-4">
            <img src="/logo.png" alt="Logo" className="w-14 h-14 object-contain" />
          </div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-accent to-indigo bg-clip-text text-transparent">
            STRATUM
          </h1>
          <p className="text-xs text-muted mt-1 tracking-widest uppercase">
            by hackdev
          </p>
        </div>

        <form onSubmit={submit} className="glass rounded-2xl p-8 space-y-4">
          <div className="flex gap-2 mb-2">
            {["login", "register"].map((m) => (
              <button
                key={m}
                type="button"
                onClick={() => setMode(m)}
                className={`flex-1 py-2 rounded-lg text-sm font-medium capitalize transition ${
                  mode === m
                    ? "bg-indigo text-white"
                    : "text-muted hover:text-white"
                }`}
              >
                {m}
              </button>
            ))}
          </div>

          <div>
            <label className="text-xs text-muted uppercase tracking-wider">Username</label>
            <input
              className="w-full mt-1 p-3 bg-elevated rounded-lg outline-none border border-border focus:border-accent transition"
              value={u}
              onChange={(e) => setU(e.target.value)}
              autoComplete="username"
              required
            />
          </div>

          <div>
            <label className="text-xs text-muted uppercase tracking-wider">Password</label>
            <input
              className="w-full mt-1 p-3 bg-elevated rounded-lg outline-none border border-border focus:border-accent transition"
              type="password"
              value={p}
              onChange={(e) => setP(e.target.value)}
              autoComplete={mode === "login" ? "current-password" : "new-password"}
              minLength={6}
              required
            />
          </div>

          <button
            disabled={busy}
            className="w-full py-3 rounded-lg bg-gradient-to-r from-accent to-indigo text-black font-semibold hover:opacity-90 disabled:opacity-50 transition"
          >
            {busy ? "…" : mode === "login" ? "Sign In" : "Create Account"}
          </button>

          <p className="text-xs text-center text-muted">
            New accounts start with <span className="num text-accent">$10,000.00</span> virtual cash
          </p>
        </form>
      </div>
    </div>
  );
}