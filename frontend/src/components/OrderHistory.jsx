import { useEffect, useState } from "react";
import api from "../api";
import Card from "./ui/Card";
import { toast } from "../lib/toast";

const STATUS_COLORS = {
  EXECUTED: "text-accent",
  PENDING: "text-yellow-400",
  FAILED: "text-danger",
  CANCELLED: "text-muted",
};

export default function OrderHistory({ tick }) {
  const [orders, setOrders] = useState([]);
  const [txns, setTxns] = useState([]);

  const load = () => {
    api.get("/trading/orders/").then((r) => setOrders(r.data.results || r.data));
    api.get("/trading/transactions/").then((r) => setTxns(r.data.results || r.data));
  };

  useEffect(load, [tick]);

  const cancel = async (id) => {
    await api.post(`/trading/orders/${id}/cancel/`);
    toast("Order cancelled", "success");
    load();
  };

  return (
    <div className="space-y-6">
      <Card title="Open & Recent Orders">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-xs text-muted uppercase tracking-wider border-b border-border">
                <th className="text-left py-2">Time</th>
                <th>Symbol</th>
                <th>Side</th>
                <th>Type</th>
                <th className="text-right">Qty</th>
                <th>Status</th>
                <th className="text-right">Fill</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {orders.length === 0 && (
                <tr><td colSpan="8" className="text-center py-6 text-muted">No orders</td></tr>
              )}
              {orders.map((o) => (
                <tr key={o.id} className="border-b border-border/30">
                  <td className="py-2 text-xs text-muted">
                    {new Date(o.created_at).toLocaleString()}
                  </td>
                  <td className="font-semibold tracking-wider">{o.stock?.symbol}</td>
                  <td className={o.side === "BUY" ? "text-accent" : "text-danger"}>{o.side}</td>
                  <td className="text-muted">{o.order_type}</td>
                  <td className="text-right num">{parseFloat(o.quantity)}</td>
                  <td className={STATUS_COLORS[o.status]}>{o.status}</td>
                  <td className="text-right num">
                    {o.filled_price ? `$${parseFloat(o.filled_price).toFixed(2)}` : "—"}
                  </td>
                  <td className="text-right">
                    {o.status === "PENDING" && (
                      <button onClick={() => cancel(o.id)}
                              className="text-xs text-danger hover:underline">
                        cancel
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      <Card title="Transaction Ledger">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-xs text-muted uppercase tracking-wider border-b border-border">
                <th className="text-left py-2">Time</th>
                <th>Symbol</th>
                <th>Side</th>
                <th className="text-right">Qty</th>
                <th className="text-right">Price</th>
                <th className="text-right">Commission</th>
              </tr>
            </thead>
            <tbody>
              {txns.length === 0 && (
                <tr><td colSpan="6" className="text-center py-6 text-muted">No transactions</td></tr>
              )}
              {txns.map((t) => (
                <tr key={t.id} className="border-b border-border/30">
                  <td className="py-2 text-xs text-muted">
                    {new Date(t.created_at).toLocaleString()}
                  </td>
                  <td className="font-semibold tracking-wider">{t.stock?.symbol}</td>
                  <td className={t.side === "BUY" ? "text-accent" : "text-danger"}>{t.side}</td>
                  <td className="text-right num">{parseFloat(t.quantity)}</td>
                  <td className="text-right num">${parseFloat(t.price).toFixed(2)}</td>
                  <td className="text-right num text-muted">${parseFloat(t.commission).toFixed(4)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}