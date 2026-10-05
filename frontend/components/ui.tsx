import type { ReactNode } from "react";

export const label = (id: string | null | undefined) => (id ? id.replace("FLIGHT_", "Flight ") : "—");

export function Card({ title, children, right }: { title?: string; children: ReactNode; right?: ReactNode }) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      {(title || right) && (
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500">{title}</h2>
          {right}
        </div>
      )}
      {children}
    </section>
  );
}

export function Btn({ children, onClick, disabled, tone = "primary", id }: {
  children: ReactNode; onClick?: () => void; disabled?: boolean; tone?: "primary" | "danger" | "ghost"; id?: string;
}) {
  const tones = {
    primary: "bg-indigo-600 text-white hover:bg-indigo-700",
    danger: "bg-rose-600 text-white hover:bg-rose-700",
    ghost: "border border-slate-300 bg-white text-slate-700 hover:bg-slate-100",
  };
  return (
    <button data-testid={id} onClick={onClick} disabled={disabled}
      className={`rounded-lg px-4 py-2 text-sm font-medium transition disabled:cursor-not-allowed disabled:opacity-40 ${tones[tone]}`}>
      {children}
    </button>
  );
}

const badge: Record<string, string> = {
  ACTIVE: "bg-emerald-100 text-emerald-800", QUARANTINED: "bg-amber-100 text-amber-800",
  REVOKED: "bg-slate-200 text-slate-600", HIGH: "bg-rose-100 text-rose-800",
  MEDIUM: "bg-amber-100 text-amber-800", LOW: "bg-slate-100 text-slate-600",
  STABLE: "bg-emerald-100 text-emerald-800", UNSTABLE: "bg-rose-100 text-rose-800", INCOMPLETE: "bg-amber-100 text-amber-800",
};
export const Badge = ({ v }: { v: string }) => (
  <span className={`rounded-full px-2 py-0.5 text-xs font-semibold ${badge[v] ?? "bg-slate-100 text-slate-700"}`}>{v}</span>
);

export const Err = ({ msg }: { msg: string | null }) =>
  msg ? <p data-testid="error" className="rounded-lg bg-rose-50 p-3 text-sm text-rose-700">{msg}</p> : null;
