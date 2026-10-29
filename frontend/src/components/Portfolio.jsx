import { useEffect, useState } from "react";
import api from "../api";
import Card from "./ui/Card";
import Price from "./ui/Price";
import Skeleton from "./ui/Skeleton";

export default function Portfolio({ tick, className = "" }) {
  const [data, setData] = useState(null);
  const [err, setErr] = useState("");

  useEffect(() => {
    let cancelled = false;
    api
      .get("/trading/portfolio/")
      .then((r) => !cancelled && setData(r.data))
      .catch((e) => !cancelled && setErr(e.message));
    return () => { cancelled = true; };
  }, [tick]);

  if (err) return <Card title="Portfolio"><div className="text-danger">{err}</div></Card>;
  if (!data) return (
    <Card title="Portfolio" className={className}>
      <Skeleton className="h-10 w-40 mb-4" />
      <Skeleton className="h-4 w-full mb-2" />
      <Skeleton className="h-4 w-full mb-2" />
      <Skeleton className="h-4 w-full" />
    </Card>
  );

  const pnl = data.total_value - 10000;
  const pnlPct = (pnl / 10000) * 100;
  const positive = pnl >= 0;

  return (
    <Card
      title="Portfolio"
      className={className}
      right={
        <div className={`num text-sm font-semibold ${positive ? "text-accent" : "text-danger"}`}>
          {positive ? "▲" : "▼"} {pnlPct.toFixed(2)}%
        </div>
      }
    >
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div>
          <div className="text-xs text-muted uppercase tracking-wider">Total Value</div>
          <div className="text-3xl font-bold num mt-1">
            <Price value={data.total_value} />
          </div>
        </div>
        <div>
          <div className="text-xs text-muted uppercase tracking-wider">Cash</div>
          <div className="text-3xl font-bold num mt-1 text-muted">
            <Price value={data.cash} />
          </div>
        </div>
      </div>

      <div className="border-t border-border pt-4">
        <div className="grid grid-cols-[1fr_auto_auto] gap-4 text-xs text-muted uppercase tracking-wider mb-2">
          <span>Symbol</span>
          <span>Qty</span>
          <span className="text-right">Value</span>
        </div>
        {data.assets.length === 0 && (
          <div className="text-center py-6 text-muted text-sm">
            No holdings yet. Place your first trade →
          </div>
        )}
        {data.assets.map((a) => (
          <div
            key={a.id}
            className="grid grid-cols-[1fr_auto_auto] gap-4 text-sm py-2 border-b border-border/40 last:border-0"
          >
            <div>
              <div className="font-semibold">{a.stock.symbol}</div>
              <div className="text-xs text-muted">{a.stock.name}</div>
            </div>
            <div className="num text-right">{parseFloat(a.quantity).toFixed(4)}</div>
            <div className="num text-right font-semibold">
              <Price value={a.market_value} />
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}