export type Memory = { id: string; type: string; content: string; status: "ACTIVE" | "QUARANTINED" | "REVOKED"; source_session_id: string | null };
export type Flight = { id: string; label: string; price_usd: number; stops: number; overnight_layover: boolean; description: string };
export type Decision = {
  decision_id: string; selected_option_id: string; summary: string; decision_factors: string[];
  memory_ids_used: string[]; memory_ids_available: string[]; confidence: number; model_name: string;
  latency_ms: number; options: Flight[] | null; violation: string | null;
};
export type Incident = { incident_id: string; incident_type: string; description: string; status: string; original_reproduced: boolean; original_stability: string | null };
export type Run = { id: number; run_type: string; run_index: number; removed_memory_id: string | null; selected_option_id: string | null; status: string; model_name: string | null; latency_ms: number; summary: string | null };
export type Attribution = {
  memory_id: string; original_action: string; counterfactual_action: string | null; action_changed: boolean;
  attribution_score: number; influence: "HIGH" | "MEDIUM" | "LOW"; status: string; changed_runs: number; total_runs: number;
};
export type AttributionView = {
  incident_status: string; ranked: Attribution[]; original_runs: Run[];
  counterfactual_runs: Record<string, Run[]>; model_name: string; n_repeats: number;
};
export type ReplayOriginal = { reproduced: boolean; stability: string; action: string; original_action: string; incident_status: string; runs: Run[] };
export type Verify = { changed: boolean; original_action: string; incident_status: string; decision: Decision };
export type Screen = "ai" | "decision" | "replay" | "review";
