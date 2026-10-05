"use client";
import { useCallback, useEffect, useState } from "react";
import DecisionView from "@/components/DecisionView";
import MemoryReview from "@/components/MemoryReview";
import PersonalAI from "@/components/PersonalAI";
import ReplayLab from "@/components/ReplayLab";
import { Btn, Err } from "@/components/ui";
import { api } from "@/lib/api";
import type { AttributionView, Decision, Incident, Memory, ReplayOriginal, Screen, Verify } from "@/types";

const TABS: [Screen, string][] = [["ai", "1 · Personal AI"], ["decision", "2 · Decision"], ["replay", "3 · Replay Lab"], ["review", "4 · Memory Review"]];

export default function Home() {
  const [screen, setScreen] = useState<Screen>("ai");
  const [session, setSession] = useState("S002");
  const [memories, setMemories] = useState<Memory[]>([]);
  const [message, setMessage] = useState("");
  const [decision, setDecision] = useState<Decision | null>(null);
  const [incident, setIncident] = useState<Incident | null>(null);
  const [original, setOriginal] = useState<ReplayOriginal | null>(null);
  const [attribution, setAttribution] = useState<AttributionView | null>(null);
  const [verify, setVerify] = useState<Verify | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refreshMemories = useCallback(async () => setMemories(await api.memories()), []);
  useEffect(() => { refreshMemories().catch((e) => setError(String(e))); }, [refreshMemories]);

  const run = async (fn: () => Promise<void>) => {
    setBusy(true); setError(null);
    try { await fn(); } catch (e) { setError(String(e)); } finally { setBusy(false); }
  };

  const reset = () => run(async () => {
    const r = await api.reset();
    setSession(r.session2); setDecision(null); setIncident(null); setOriginal(null); setAttribution(null); setVerify(null);
    setMessage(""); await refreshMemories(); setScreen("ai");
  });

  const send = (m: string) => run(async () => {
    setMessage(m); setIncident(null); setOriginal(null); setAttribution(null); setVerify(null);
    setDecision(await api.decide(session, m)); setScreen("decision");
  });

  const report = () => run(async () => {
    setIncident(await api.report(decision!.decision_id)); setScreen("replay");
  });

  const replay = () => run(async () => {
    const r = await api.replay(incident!.incident_id);
    setOriginal(r); setIncident({ ...incident!, status: r.incident_status, original_reproduced: r.reproduced });
  });

  const counterfactual = () => run(async () => {
    await api.counterfactual(incident!.incident_id);
    const a = await api.attribution(incident!.incident_id);
    setAttribution(a); setIncident({ ...incident!, status: a.incident_status });
  });

  const setStatus = (fn: (id: string) => Promise<Memory>) => (id: string) => run(async () => { await fn(id); await refreshMemories(); });

  return (
    <main className="mx-auto max-w-5xl px-4 py-8">
      <header className="mb-6 flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold">RecallGuard</h1>
          <p className="text-sm text-slate-500">Find the memory that changed the agent's mind.</p>
        </div>
        <Btn id="reset" tone="ghost" disabled={busy} onClick={reset}>Reset demo</Btn>
      </header>
      <nav className="mb-5 flex gap-1 rounded-xl bg-slate-200 p-1">
        {TABS.map(([k, t]) => (
          <button key={k} data-testid={`tab-${k}`} onClick={() => setScreen(k)}
            className={`flex-1 rounded-lg px-3 py-2 text-sm font-medium ${screen === k ? "bg-white shadow" : "text-slate-600 hover:bg-slate-100"}`}>{t}</button>
        ))}
      </nav>
      <div className="space-y-4">
        <Err msg={error} />
        {screen === "ai" && <PersonalAI memories={memories} sessionId={session} busy={busy} onAddMemory={(c) => run(async () => { await api.addMemory(c); await refreshMemories(); })} onSend={send} />}
        {screen === "decision" && <DecisionView message={message} decision={decision} memories={memories} incident={incident} busy={busy} onReport={report} />}
        {screen === "replay" && <ReplayLab incident={incident} original={original} attribution={attribution} memories={memories} busy={busy} onReplay={replay} onCounterfactual={counterfactual} />}
        {screen === "review" && <MemoryReview incident={incident} attribution={attribution} memories={memories} verify={verify} busy={busy}
          onQuarantine={setStatus(api.quarantine)} onRestore={setStatus(api.restore)}
          onVerify={() => run(async () => setVerify(await api.verify(incident!.incident_id)))} />}
      </div>
    </main>
  );
}
