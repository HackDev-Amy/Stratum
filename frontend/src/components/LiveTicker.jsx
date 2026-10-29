import { useEffect, useState, useRef } from "react";
import Card from "./ui/Card";

export default function LiveTicker() {
  const [prices, setPrices] = useState({});
  const [connected, setConnected] = useState(false);
  const prev = useRef({});

  useEffect(() => {
    const proto = window.location.protocol === "https:" ? "wss" : "ws";
    const ws = new WebSocket(`${proto}://${window.location.host}/ws/prices/`);
    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);
    ws.onmessage = (e) => {
      try {
        const { symbol, price } = JSON.parse(e.data);
        setPrices((p) => {
          prev.current = p;
          return { ...p, [symbol]: price };
        });
      } catch {}
    };
    return () => ws.close();
  }, []);

  const entries = Object.entries(prices).sort();

  return (
    <Card
      title="Live Prices"
      right={
        <div className="flex items-center gap-2 text-xs">
          <div className={`w-2 h-2 rounded-full ${connected ? "bg-accent animate-pulseDot" : "bg-danger"}`} />
          <span className={connected ? "text-accent" : "text-danger"}>
            {connected ? "LIVE" : "OFFLINE"}
          </span>
        </div>
      }
    >
      <div className="space-y-1 max-h-72 overflow-y-auto">
        {entries.length === 0 && (
          <div className="text-center py-8 text-muted text-sm">
            Awaiting market data…
          </div>
        )}
        {entries.map(([sym, p]) => {
          const old = prev.current[sym];
          const up = old !== undefined && p > old;
          const down = old !== undefined && p < old;
          return (
            <div key={sym} className="flex justify-between items-center py-1.5 border-b border-border/30 last:border-0">
              <span className="font-medium text-sm tracking-wider">{sym}</span>
              <span className={`num text-sm font-semibold ${up ? "text-accent" : down ? "text-danger" : ""}`}>
                ${Number(p).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </span>
            </div>
          );
        })}
      </div>
    </Card>
  );
}