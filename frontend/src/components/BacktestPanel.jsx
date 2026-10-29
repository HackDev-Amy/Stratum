import { useState } from "react";
import api from "../api";
import Card from "./ui/Card";
import { toast } from "../lib/toast";
import {
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid,
} from "recharts";

const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="glass rounded-lg px-3 py-2 text-xs">
      <div className="text-muted">Equity</div>
      <div className="num text-accent font-semibold">
        ${Number(payload[0].value).toFixed(2)}
      </div>
    </div>
  );
};

export default function BacktestPanel() {
  const [symbol, setSymbol] = useState("AAPL");
  const [period, setPeriod] = useState("6mo");
  const [interval, setInterval] = useState("1h");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const run = async () => {
    setLoading(true);
    setResult(null);
    try {
      const r = await api.post("/backtest/run/", {
        symbol, period, interval, risk_pct: 1, stop_loss_pct: 2,
      });
      if (r.data.error) toast(r.data.error, "error");
      else setResult(r.data);
    } catch (e) {
      toast(e.response?.data?.error || "Backtest failed", "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <Card title="Backtest Configuration">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div>
            <label className="text-xs text-muted uppercase tracking-wider">Symbol</label>
            <input
              className="w-full mt-1 p-2.5 bg-elevated rounded-lg border border-border focus:border-accent outline-none font-semibold tracking-wider"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value.toUpperCase())}
            />
          </div>
          <div>
            <label className="text-xs text-muted uppercase tracking-wider">Period</label>
            <select
              className="w-full mt-1 p-2.5 bg-elevated rounded-lg border border-border focus:border-accent outline-none"
              value={period}
              onChange={(e) => setPeriod(e.target.value)}
            >
              {["1mo", "3mo", "6mo", "1y", "2y"].map((p) => <option key={p}>{p}</option>)}
            </select>
          </div>
          <div>
            <label className="text-xs text-muted uppercase tracking-wider">Interval</label>
            <select
              className="w-full mt-1 p-2.5 bg-elevated rounded-lg border border-border focus:border-accent outline-none"
              value={interval}
              onChange={(e) => setInterval(e.target.value)}
            >
              {["15m", "30m", "1h", "1d"].map((i) => <option key={i}>{i}</option>)}
            </select>
          </div>
          <div className="flex items-end">
            <button
              onClick={run}
              disabled={loading}
              className="w-full py-2.5 rounded-lg bg-gradient-to-r from-accent to-indigo text-black font-semibold hover:opacity-90 disabled:opacity-50 transition"
            >
              {loading ? "Running…" : "Run Backtest"}
            </button>
          </div>
        </div>
      </Card>

      {result?.metrics && (
        <>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Stat label="Total Return" value={`${result.metrics.total_return_pct}%`}
                  positive={result.metrics.total_return_pct >= 0} />
            <Stat label="Sharpe Ratio" value={result.metrics.sharpe_ratio} />
            <Stat label="Max Drawdown" value={`${result.metrics.max_drawdown_pct}%`} negative />
            <Stat label="Win Rate" value={`${result.metrics.win_rate_pct}%`}
                  positive={result.metrics.win_rate_pct > 50} />
          </div>

          <Card title="Equity Curve">
            <ResponsiveContainer width="100%" height={320}>
              <AreaChart data={result.equity_curve}>
                <defs>
                  <linearGradient id="eqGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#00E5A0" stopOpacity={0.4} />
                    <stop offset="100%" stopColor="#00E5A0" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid stroke="#1F2A3A" strokeDasharray="3 3" />
                <XAxis dataKey="time" hide />
                <YAxis stroke="#9CA3AF" tick={{ fontSize: 11 }} domain={["auto", "auto"]} />
                <Tooltip content={<CustomTooltip />} />
                <Area type="monotone" dataKey="equity" stroke="#00E5A0"
                      strokeWidth={2} fill="url(#eqGrad)" />
              </AreaChart>
            </ResponsiveContainer>
          </Card>
        </>
      )}
    </div>
  );
}

function Stat({ label, value, positive, negative }) {
  const color = positive ? "text-accent" : negative ? "text-danger" : "text-white";
  return (
    <div className="glass rounded-xl p-4">
      <div className="text-xs text-muted uppercase tracking-wider">{label}</div>
      <div className={`text-2xl font-bold num mt-1 ${color}`}>{value}</div>
    </div>
  );
}