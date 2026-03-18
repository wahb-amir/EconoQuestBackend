export const config = {
  port: Number(process.env.PORT ?? 7860),
  internalToken: process.env.INTERNAL_TOKEN ?? "",
  jwtSecret: process.env.JWT_SECRET ?? "",

  spaces: {
    hint: [
      process.env.HF_HINT_SPACE_1 ?? "",
      process.env.HF_HINT_SPACE_2 ?? "",
    ],
    summary: [
      process.env.HF_SUMMARY_SPACE_1 ?? "",
      process.env.HF_SUMMARY_SPACE_2 ?? "",
    ],
  },

  cron: {
    pingInterval: "*/25 * * * *",  // every 25 min
    timeoutMs: 5000,
  },

  lb: {
    timeoutMs: 15000,   // hint timeout
    summaryTimeoutMs: 40000,  // summary needs longer — 1.5B model
  },
} as const;