import { useState } from "react";
import api from "../api";
import Card from "./ui/Card";
import { toast } from "../lib/toast";

const ORDER_TYPES = [
  { value: "MARKET", label: "Market", hint: "Instant fill at current price" },
  { value: "LIMIT", label: "Limit", hint: "Execute when price hits trigger" },
  { value: "STOP_LOSS", label: "Stop-Loss", hint: "Execute when price drops to trigger" },
];

export default function TradeForm({ onTrade, className = "" }) {
  const [symbol, setSymbol] = useState("AAPL");
  const [qty, setQty] = useState(1);
  const [orderType, setOrderType] = useState("MARKET");
  const [triggerPrice, setTriggerPrice] = useState("");
  const [busy, setBusy] = useState(false);

  const send = async (side) => {
    setBusy(true);
    try {
      let r;
      if (orderType === "MARKET") {
        r = await api.post("/trading/orders/market/", { symbol, side, quantity: qty });
      } else {
        r = await api.post("/trading/orders/advanced/", {
          symbol, side, quantity: qty, order_type: orderType, trigger_price: triggerPrice,
        });
      }
      const ok = r.data.status === "EXECUTED" || r.data.status === "PENDING";
      toast(
        `${side} ${qty} ${symbol} — ${r.data.status}`,
        ok ? "success" : "error"
      );
      onTrade && onTrade();
    } catch (e) {
      toast(e.response?.data?.error || "Order failed", "error");
    } finally {
      setBusy(false);
    }
  };

  const hint = ORDER_TYPES.find((t) => t.value === orderType)?.hint;

  return (
    <Card title="Order Ticket" className={className}>
      <div className="space-y-3">
        <div>
          <label className="text-xs text-muted uppercase tracking-wider">Symbol</label>
          <input
            className="w-full mt-1 p-3 bg-elevated rounded-lg outline-none border border-border focus:border-accent transition font-semibold tracking-wider"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value.toUpperCase())}
            placeholder="AAPL"
          />
        </div>

        <div>
          <label className="text-xs text-muted uppercase tracking-wider">Quantity</label>
          <input
            className="w-full mt-1 p-3 bg-elevated rounded-lg outline-none border border-border focus:border-accent transition num"
            type="number"
            min="0.0001"
            step="any"
            value={qty}
            onChange={(e) => setQty(e.target.value)}
          />
        </div>

        <div>
          <label className="text-xs text-muted uppercase tracking-wider">Order Type</label>
          <div className="grid grid-cols-3 gap-2 mt-1">
            {ORDER_TYPES.map((t) => (
              <button
                key={t.value}
                onClick={() => setOrderType(t.value)}
                className={`p-2 rounded-lg text-xs font-medium transition ${
                  orderType === t.value
                    ? "bg-elevated border border-accent text-accent"
                    : "border border-border text-muted hover:text-white"
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>
          <div className="text-xs text-muted mt-1">{hint}</div>
        </div>

        {orderType !== "MARKET" && (
          <div>
            <label className="text-xs text-muted uppercase tracking-wider">Trigger Price</label>
            <input
              className="w-full mt-1 p-3 bg-elevated rounded-lg outline-none border border-border focus:border-accent transition num"
              type="number"
              step="any"
              value={triggerPrice}
              onChange={(e) => setTriggerPrice(e.target.value)}
              placeholder="0.00"
            />
          </div>
        )}

        <div className="grid grid-cols-2 gap-3 pt-2">
          <button
            disabled={busy}
            onClick={() => send("BUY")}
            className="py-3 rounded-lg bg-accent text-black font-bold hover:opacity-90 disabled:opacity-50 transition"
          >
            BUY
          </button>
          <button
            disabled={busy}
            onClick={() => send("SELL")}
            className="py-3 rounded-lg bg-danger text-white font-bold hover:opacity-90 disabled:opacity-50 transition"
          >
            SELL
          </button>
        </div>
      </div>
    </Card>
  );
}