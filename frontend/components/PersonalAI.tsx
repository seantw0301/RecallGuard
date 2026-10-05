"use client";
import { useState } from "react";
import type { Memory } from "@/types";
import { Badge, Btn, Card } from "./ui";

type Props = {
  memories: Memory[]; sessionId: string; busy: boolean;
  onAddMemory: (c: string) => void; onSend: (message: string) => void;
};

export default function PersonalAI({ memories, sessionId, busy, onAddMemory, onSend }: Props) {
  const [mem, setMem] = useState("");
  const [msg, setMsg] = useState("Book me a flight to Tokyo next Friday.");
  return (
    <div className="grid gap-5 md:grid-cols-2">
      <Card title="Chat — current session" right={<span className="text-xs text-slate-400">{sessionId}</span>}>
        <div className="mb-3 space-y-2 text-sm">
          <p className="rounded-lg bg-slate-100 p-3 text-slate-600">Session 1 — you told your assistant {memories.length} things. It remembers them.</p>
          <p className="rounded-lg bg-indigo-50 p-3 text-indigo-900">Session 2 — ask for something and your personal AI acts on its memories.</p>
        </div>
        <textarea data-testid="chat-input" value={msg} onChange={(e) => setMsg(e.target.value)} rows={2}
          className="w-full rounded-lg border border-slate-300 p-2 text-sm" />
        <div className="mt-2"><Btn id="send" disabled={busy || !msg} onClick={() => onSend(msg)}>{busy ? "Nemotron is deciding…" : "Send to assistant"}</Btn></div>
      </Card>
      <Card title="Memories">
        <ul data-testid="memory-list" className="space-y-2">
          {memories.map((m) => (
            <li key={m.id} data-testid={`memory-${m.id}`} className="flex items-start justify-between gap-3 rounded-lg border border-slate-200 p-3 text-sm">
              <span><b className="mr-2 font-mono text-xs text-slate-500">{m.id}</b>{m.content}</span>
              <Badge v={m.status} />
            </li>
          ))}
        </ul>
        <div className="mt-3 flex gap-2">
          <input data-testid="memory-input" value={mem} onChange={(e) => setMem(e.target.value)} placeholder="Tell your assistant something to remember…"
            className="flex-1 rounded-lg border border-slate-300 p-2 text-sm" />
          <Btn tone="ghost" disabled={busy || !mem} onClick={() => { onAddMemory(mem); setMem(""); }}>Remember</Btn>
        </div>
      </Card>
    </div>
  );
}
