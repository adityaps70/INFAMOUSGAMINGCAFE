import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const css = readFileSync(resolve(process.cwd(), "src/styles.css"), "utf8");

describe("responsive and accessible stylesheet contract", () => {
  it("preserves keyboard focus and reduced-motion preferences", () => {
    expect(css).toContain(":focus-visible");
    expect(css).toContain("@media (prefers-reduced-motion: reduce)");
  });

  it("includes explicit compact and wide layout breakpoints", () => {
    expect(css).toMatch(/@media\s*\(max-width:\s*760px\)/);
    expect(css).toMatch(/@media\s*\(min-width:\s*1000px\)/);
  });

  it("keeps the mobile action bar clear of device safe areas", () => {
    expect(css).toContain("env(safe-area-inset-bottom)");
  });


  it("prevents horizontal page drift and offsets sticky anchor targets", () => {
    expect(css).toContain("overflow-x: clip");
    expect(css).toContain("scroll-margin-top");
  });

  it("keeps quick mobile actions comfortably touchable", () => {
    expect(css).toMatch(/\.mobile-actions[\s\S]*min-height:\s*44px/);
  });

  it("locks the cafe palette and keeps the logo header pure black", () => {
    expect(css).toContain("--lime: #c8ff2e");
    expect(css).toContain("--orange: #ff1717");
    expect(css).toMatch(/\.site-header\s*\{[^}]*background:\s*#000/s);
  });
});
