import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: ".",
  testMatch: "demo-recording.spec.ts",
  timeout: 240_000,
  workers: 1,
  reporter: "list",
  outputDir: "../artifacts/pw",
  use: { baseURL: "http://localhost:3000" },
});
