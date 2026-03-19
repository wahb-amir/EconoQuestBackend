import { createHash } from "crypto";

// deterministic order — all 18 state values
const STATE_KEYS = [
  "round", "ctx", "itr", "spd", "rnd", "fln", "wfr", "tar", "prt",
  "swf", "gdp", "inf", "unemp", "dbt", "cur", "trd", "inn", "sal", "mood",
];

export function hashState(state: Record<string, unknown>): string {
  const ordered = STATE_KEYS
    .map(k => `${k}:${state[k] ?? ""}`)
    .join("|");
  return createHash("sha256").update(ordered).digest("hex");
}