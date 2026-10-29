import { useEffect, useState } from "react";
import api from "../api";
import Card from "./ui/Card";
import { toast } from "../lib/toast";

export default function BotManager() {
  const [bots, setBots] = useState([]);
  const [logs, setLogs] = useState([]);
  const [symbol, setSymbol] = useState("AAPL");
  const [qty, setQty] = useState(1);

  const load = async () => {
    const [b, l] = await Promise.all([
      api.get("/bot/"),
      api.get("/bot/logs/"),
    ]);
    setBots(b.data.results || b.data);
    setLogs(l.data.results || l.data);
  };

  useEffect(() => {
    load();
    const i = setInterval(load, 15000);
    return () => clearInterval(i);
  }, []);

  const create = async () => {
    try {
      await api.post("/bot/", {
        symbol, quantity: qty,
        strategy_params: { short: 10, long: 30, rsi: 14 },
        risk_params: { risk_pct: 1, stop_loss_pct: 2 },
        is_active: false,
      });
      toast("Bot created", "success");
      load();
    } catch (e) {
      toast(e.response?.data?.error || "Failed", "error");
    }
  };

  const toggle = async (bot) => {
    await api.patch(`/bot/${bot.id}/`, { is_active: !bot.is_active });
    load();
  };

  const runOnce = async (bot) => {
    const r = await api.post(`/bot/${bot.id}/run/`);
    toast(`Signal: ${r.data.signal || "none"}`, "info");
    load();
  };

  const remove = async (id) => {
    if (!confirm("Delete bot?")) return;
    await api.delete(`/bot/${id}/`);
    load();
  };

  return (
    <div className="space-y-6">
      <Card title="Create Bot">
        <div className="grid grid-cols-3 gap-3">
          <input className="p-2.5 bg-elevated rounded-lg border border-border focus:border-accent outline-none font-semibold tracking-wider"
                 value={symbol} onChange={(e) => setSymbol(e.target.value.toUpperCase())} />
          <input className="p-2.5 bg-elevated rounded-lg border border-border focus:border-accent outline-none num"
                 type="number" value={qty} onChange={(e) => setQty(e.target.value)} />
          <button onClick={create}
                  className="py-2.5 rounded-lg bg-gradient-to-r from-accent to-indigo text-black font-semibold">
            + New Bot
          </button>
        </div>
      </Card>

      <Card title="Active Bots">
        <div className="space-y-2">
          {bots.length === 0 && <div className="text-muted text-sm py-4 text-center">No bots configured</div>}
          {bots.map((b) => (
            <div key={b.id} className="flex items-center justify-between p-3 rounded-lg bg-elevated/40 border border-border/40">
              <div>
                <div className="font-semibold tracking-wider">{b.stock?.symbol || b.symbol}</div>
                <div className="text-xs text-muted num">qty {parseFloat(b.quantity)} · {b.last_run ? new Date(b.last_run).toLocaleString() : "never"}</div>
              </div>
              <div className="flex items-center gap-2">
                <button onClick={() => toggle(b)}
                        className={`px-3 py-1 rounded-lg text-xs font-bold ${
                          b.is_active ? "bg-accent text-black" : "bg-elevated text-muted"
                        }`}>
                  {b.is_active ? "ON" : "OFF"}
                </button>
                <button onClick={() => runOnce(b)} className="text-xs text-indigo hover:underline">run</button>
                <button onClick={() => remove(b.id)} className="text-xs text-danger hover:underline">del</button>
              </div>
            </div>
          ))}
        </div>
      </Card>

      <Card title="Bot Logs">
        <div className="max-h-96 overflow-auto text-xs space-y-1">
          {logs.length === 0 && <div className="text-muted text-center py-4">No logs yet</div>}
          {logs.map((l) => (
            <div key={l.id} className="py-1.5 border-b border-border/30">
              <span className="text-muted num">[{new Date(l.created_at).toLocaleTimeString()}]</span>{" "}
              {l.message}
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}