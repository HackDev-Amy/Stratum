import { useToasts } from "../../lib/toast";

const colors = {
  success: "border-accent text-accent",
  error: "border-danger text-danger",
  info: "border-indigo text-indigo",
};

export default function ToastHost() {
  const { items, remove } = useToasts();
  return (
    <div className="fixed bottom-6 right-6 z-[100] space-y-2">
      {items.map((t) => (
        <div
          key={t.id}
          onClick={() => remove(t.id)}
          className={`glass px-4 py-3 rounded-lg text-sm cursor-pointer border-l-4 ${colors[t.type] || colors.info} animate-slide-in`}
        >
          {t.msg}
        </div>
      ))}
    </div>
  );
}