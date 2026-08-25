import { existsSync, readFileSync, statSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = process.cwd();
const readProjectFile = (path: string) => readFileSync(resolve(root, path), "utf8");

describe("static GitHub Pages delivery", () => {
  it("publishes useful local-business and social metadata", () => {
    const html = readProjectFile("index.html");

    expect(html).toContain("inFAMOUS Gaming Cafe | Gaming, VR &amp; More in Lucknow");
    expect(html).toContain('property="og:image" content="./og.png"');
    expect(html).toContain('name="twitter:card" content="summary_large_image"');
    expect(html).toContain('"telephone": "+919918332386"');
    expect(html).toContain('"postalCode": "226012"');
    expect(html).toContain("https://www.instagram.com/infamousgaming_cafe/");
    expect(html).not.toMatch(/openingHours|9:30 PM/i);
  });

  it("includes every browser asset required by the static build", () => {
    for (const path of [
      "public/.nojekyll",
      "public/favicon.svg",
      "public/logo.png",
      "public/og.png",
      "public/robots.txt",
    ]) {
      expect(existsSync(resolve(root, path)), `${path} should exist`).toBe(true);
    }

    expect(statSync(resolve(root, "public/logo.png")).size).toBeLessThan(350_000);
    expect(statSync(resolve(root, "public/og.png")).size).toBeLessThan(450_000);
  });


  it("keeps Vite and documentation explicitly safe for GitHub Pages", () => {
    const viteConfig = readProjectFile("vite.config.ts");
    const readme = readProjectFile("README.md");

    expect(viteConfig).toContain('base: "./"');
    expect(readme).toContain("GitHub Actions");
    expect(readme).toContain("galleryData.ts");
    expect(readme).toContain("npm ci");
  });

  it("contains an automated GitHub Pages publishing workflow", () => {
    const workflow = readProjectFile(".github/workflows/deploy-pages.yml");

    expect(workflow).toContain("pages: write");
    expect(workflow).toMatch(/branches:\s*\[main,\s*master\]/);
    expect(workflow).toContain("npm ci");
    expect(workflow).toContain("npm test");
    expect(workflow).toContain("npm run build");
    expect(workflow).toContain("path: ./dist");
  });
});
