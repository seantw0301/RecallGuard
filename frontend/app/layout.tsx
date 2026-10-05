import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "RecallGuard",
  description: "Counterfactual memory replay for personal AI",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
