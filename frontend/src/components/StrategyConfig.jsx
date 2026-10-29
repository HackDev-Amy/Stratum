import { useEffect, useState } from "react";
import api from "../api";
import Card from "./ui/Card";
import { toast } from "../lib/toast";

const DEFAULTS = {
  name: "SMA_RSI",
  short_window: 10,
  long_window: 30,
  rsi_period: 14,
  risk_per_trade_pct: 1.0,
  stop_loss_pct: 2.0,
  take_profit_pct: 5.0,
  is_active: true,
};

export default function StrategyConfig() {
  const [configs, setConfigs] = useState([]);
  const [form, setForm] = useState(DEFAULTS);
  const [editing, setEditing] = useState(null);

  const load = () =>
    api    .get("/strategy/configs/").then((r) => setConfigs(r.data.results || r.data));

  useEffect(load, []);

  const submit = async (e) => {
    e.preventDefault();
    try {
      if (editing)       await api.patch(`/strategy/configs/${editing}/`, form);
      else       await api.post("/strategy/configs/", form);
      toast(editing ? "Updated" : "Created", "success");
      setForm(DEFAULTS);
      setEditing(null);
      load();
    } catch (e) {
      toast(JSON.stringify(e.response?.data) || "Failed", "error");
    }
  };

  const edit = (c) => {
    setEditing(c.id);
    setForm({
      name: c.name, short_window: c.short_window, long_window: c.long_window,
      rsi_period: c.rsi_period, risk_per_trade_pct: c.risk_per_trade_pct,
      stop_loss_pct: c.stop_loss_pct, take_profit_pct: c.take_profit_pct,
      is_active: c.is_active,
    });
  };

  const remove = async (id) => {
    if (!confirm("Delete strategy?")) return;
    await api.delete(`/strategy/configs/${id}/`);
    load();
  };

  const change = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  return (
    <div className="space-y-6">
      <Card title={editing ? "Edit Strategy" : "New Strategy"}>
        <form onSubmit={submit} className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <Field label="Name" value={form.name} onChange={(v) => change("name", v)} />
          <NumField label="Short SMA" value={form.short_window} onChange={(v) => change("short_window", v)} />
          <NumField label="Long SMA" value={form.long_window} onChange={(v) => change("long_window", v)} />
          <NumField label="RSI Period" value={form.rsi_period} onChange={(v) => change("rsi_period", v)} />
          <NumField label="Risk %" step="0.1" value={form.risk_per_trade_pct} onChange={(v) => change("risk_per_trade_pct", v)} />
          <NumField label="Stop Loss %" step="0.1" value={form.stop_loss_pct} onChange={(v) => change("stop_loss_pct", v)} />
          <NumField label="Take Profit %" step="0.1" value={form.take_profit_pct} onChange={(v) => change("take_profit_pct", v)} />
          <div className="flex items-end">
            <button className="w-full py-2.5 rounded-lg bg-gradient-to-r from-accent to-indigo text-black font-semibold">
              {editing ? "Update" : "Create"}
            </button>
          </div>
        </form>
      </Card>

      <Card title="Strategy Configs">
        <div className="space-y-2">
          {configs.length === 0 && <div className="text-muted text-sm text-center py-4">No strategies</div>}
          {configs.map((c) => (
            <div key={c.id} className="flex items-center justify-between p-3 rounded-lg bg-elevated/40 border border-border/40">
              <div>
                <div className="font-semibold">{c.name}</div>
                <div className="text-xs text-muted num">
                  SMA {c.short_window}/{c.long_window} · RSI {c.rsi_period} · Risk {c.risk_per_trade_pct}%
                </div>
              </div>
              <div className="flex items-center gap-3 text-xs">
                <span className={c.is_active ? "text-accent" : "text-muted"}>
                  {c.is_active ? "● ACTIVE" : "○ IDLE"}
                </span>
                <button onClick={() => edit(c)} className="text-indigo hover:underline">edit</button>
                <button onClick={() => remove(c.id)} className="text-danger hover:underline">del</button>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}

function Field({ label, value, onChange }) {
  return (
    <div>
      <label className="text-xs text-muted uppercase tracking-wider">{label}</label>
      <input
        className="w-full mt-1 p-2.5 bg-elevated rounded-lg border border-border focus:border-accent outline-none"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}

function NumField({ label, value, onChange, step = "1" }) {
  return (
    <div>
      <label className="text-xs text-muted uppercase tracking-wider">{label}</label>
      <input
        className="w-full mt-1 p-2.5 bg-elevated rounded-lg border border-border focus:border-accent outline-none num"
        type="number"
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value) || 0)}
      />
    </div>
  );
}