import { useEffect, useState } from "react";
import api from "../api";
import { useAuth } from "../auth";
import Portfolio from "./Portfolio";
import TradeForm from "./TradeForm";
import LiveTicker from "./LiveTicker";
import BacktestPanel from "./BacktestPanel";
import OrderHistory from "./OrderHistory";
import BotManager from "./BotManager";
import StrategyConfig from "./StrategyConfig";
import Card from "./ui/Card";

const TABS = [
  ["overview", "Overview", "◈"],
  ["trade", "Trade", "⇅"],
  ["backtest", "Backtest", "⏱"],
  ["orders", "Orders", "☰"],
  ["bots", "Bots", "⚙"],
  ["strategy", "Strategy", "◬"],
];

export default function Dashboard() {
  const { logout } = useAuth();
  const [tab, setTab] = useState("overview");
  const [tick, setTick] = useState(0);
  const bump = () => setTick((value) => value + 1);
  const label = TABS.find(([id]) => id === tab)?.[1] || "";

  return (
    <div className="min-h-screen relative z-10 flex">
      <aside className="w-64 shrink-0 p-6 flex flex-col border-r border-border">
        <div className="mb-10">
          <div className="flex items-center gap-3 mb-2">
            
              <img src="/logo.png" alt="Logo" className="w-8 h-8 object-contain" />
            
            <div>
              <div className="font-bold text-lg leading-none">STRATUM</div>
              <div className="text-[10px] text-muted uppercase tracking-widest">by hackdev</div>
            </div>
          </div>
        </div>
        <nav className="space-y-1 flex-1">
          {TABS.map(([id, name, icon]) => (
            <button
              key={id}
              onClick={() => setTab(id)}
              className={`w-full text-left px-4 py-2.5 rounded-lg text-sm font-medium transition flex items-center gap-3 ${
                tab === id ? "bg-elevated text-white shadow-glow" : "text-muted hover:text-white hover:bg-elevated/50"
              }`}
            >
              <span>{icon}</span>{name}
            </button>
          ))}
        </nav>
        <button onClick={logout} className="mt-4 px-4 py-2.5 rounded-lg text-sm text-muted hover:text-danger border border-border hover:border-danger transition">
          Sign Out
        </button>
      </aside>

      <main className="flex-1 p-8 overflow-y-auto max-h-screen">
        <div className="mb-8">
          <h1 className="text-3xl font-bold">{label}</h1>
          <p className="text-sm text-muted mt-1">Live market data · Paper trading · Real strategy signals</p>
        </div>
        {tab === "overview" && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <Portfolio tick={tick} className="lg:col-span-2" />
            <LiveTicker />
            <TradeForm onTrade={bump} className="lg:col-span-2" />
            <Card title="Quick Stats"><QuickStats tick={tick} /></Card>
          </div>
        )}
        {tab === "trade" && <div className="grid grid-cols-1 lg:grid-cols-2 gap-6"><TradeForm onTrade={bump} /><Portfolio tick={tick} /></div>}
        {tab === "backtest" && <BacktestPanel />}
        {tab === "orders" && <OrderHistory tick={tick} />}
        {tab === "bots" && <BotManager />}
        {tab === "strategy" && <StrategyConfig />}
      </main>
    </div>
  );
}

function QuickStats({ tick }) {
  const [data, setData] = useState(null);
  useEffect(() => {
    let active = true;
    api.get("/trading/portfolio/").then((response) => {
      if (active) setData(response.data);
    }).catch(() => {
      if (active) setData(null);
    });
    return () => { active = false; };
  }, [tick]);

  if (!data) return <div className="text-muted text-sm">—</div>;
  return (
    <div className="space-y-3 text-sm">
      <Row label="Equity" value={`$${Number(data.total_value).toFixed(2)}`} />
      <Row label="Cash" value={`$${Number(data.cash).toFixed(2)}`} />
      <Row label="Holdings" value={data.assets.length} />
    </div>
  );
}

function Row({ label, value }) {
  return <div className="flex justify-between"><span className="text-muted">{label}</span><span className="num">{value}</span></div>;
}
