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
    auth: "https://huggingface.co/spaces/wahb-amir/auth-service/health",
  },

  cron: {
    pingInterval: "*/25 * * * *",
    timeoutMs: 5000,
  },

  lb: {
  timeoutMs: 30_000,        
  summaryTimeoutMs: 30_000, 
}
} as const;