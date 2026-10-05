import { test, expect, Page } from "@playwright/test";
import fs from "node:fs";
import path from "node:path";

const narration: Record<string, { text: string; hold: number }> = JSON.parse(
  fs.readFileSync(path.join(__dirname, "narration.json"), "utf8"),
);
const OUT = path.join(__dirname, "..", "artifacts");

async function say(page: Page, key: string) {
  const { text, hold } = narration[key];
  await page.evaluate((t) => {
    let el = document.getElementById("rg-caption");
    if (!el) {
      el = document.createElement("div");
      el.id = "rg-caption";
      el.style.cssText =
        "position:fixed;left:0;right:0;bottom:0;padding:16px 32px;background:rgba(15,23,42,.92);color:#fff;font:600 20px system-ui;text-align:center;z-index:9999";
      document.body.appendChild(el);
    }
    el.textContent = t;
  }, text);
  await page.waitForTimeout(hold);
}

test("RecallGuard 3-minute demo", async ({ browser }) => {
  fs.mkdirSync(OUT, { recursive: true });
  const ctx = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    recordVideo: { dir: path.join(OUT, "pw-video"), size: { width: 1280, height: 720 } },
  });
  const page = await ctx.newPage();
  const started = Date.now();

  await page.goto("/");
  await page.getByTestId("reset").click();
  await expect(page.getByTestId("memory-M001")).toBeVisible();
  await say(page, "problem");
  await say(page, "memories");

  await say(page, "request");
  await page.getByTestId("send").click();
  await expect(page.getByTestId("selected")).toBeVisible({ timeout: 60_000 });
  await expect(page.getByTestId("selected")).toContainText("Flight A"); // bad decision (real Nemotron)
  await expect(page.getByTestId("violation")).toBeVisible();
  await say(page, "decision");

  await page.getByTestId("report").click();
  await expect(page.getByTestId("run-replay")).toBeVisible();
  await say(page, "incident");

  await page.getByTestId("run-replay").click();
  await expect(page.getByTestId("stability")).toContainText("reproduced", { timeout: 90_000 });
  await say(page, "original");

  await say(page, "counter");
  await page.getByTestId("run-cf").click();
  await expect(page.getByTestId("row-M003")).toBeVisible({ timeout: 150_000 });
  await expect(page.getByTestId("row-M001")).toContainText("YES");
  await expect(page.getByTestId("row-M002")).toContainText("NO");
  await expect(page.getByTestId("row-M003")).toContainText("NO");
  await say(page, "table");

  await page.getByTestId("tab-review").click();
  await expect(page.getByTestId("score-M001")).toHaveText("1.00");
  await say(page, "review");

  await page.getByTestId("quarantine-M001").click();
  await expect(page.getByTestId("memory-M001").or(page.getByTestId("verify"))).toBeVisible();
  await say(page, "quarantine");

  await say(page, "verify");
  await page.getByTestId("verify").click();
  await expect(page.getByTestId("verify-result")).toBeVisible({ timeout: 60_000 });
  await expect(page.getByTestId("verify-result")).toContainText("behavior changed");
  await say(page, "result");
  await say(page, "closing");

  const seconds = (Date.now() - started) / 1000;
  const video = page.video()!;
  await ctx.close();
  await video.saveAs(path.join(OUT, "recallguard-demo.webm"));
  console.log(`demo length ≈ ${seconds.toFixed(0)}s`);
  expect(seconds).toBeLessThan(180);
});
