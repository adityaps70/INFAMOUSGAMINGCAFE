import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

const dist = resolve(process.cwd(), "dist");
const indexPath = resolve(dist, "index.html");

if (!existsSync(indexPath)) {
  throw new Error("dist/index.html was not generated");
}

const html = readFileSync(indexPath, "utf8");
const localReferences = [...html.matchAll(/(?:src|href)="([^"]+)"/g)]
  .map((match) => match[1])
  .filter((reference) => !/^(?:https?:|mailto:|tel:|#|data:)/.test(reference));

for (const reference of localReferences) {
  if (reference.startsWith("/")) {
    throw new Error(`Root-relative build asset is not GitHub Pages safe: ${reference}`);
  }

  const cleanReference = reference.replace(/^\.\//, "").split(/[?#]/, 1)[0];
  if (!existsSync(resolve(dist, cleanReference))) {
    throw new Error(`Referenced build asset is missing: ${reference}`);
  }
}

for (const file of [".nojekyll", "favicon.svg", "og.png", "robots.txt"]) {
  if (!existsSync(resolve(dist, file))) {
    throw new Error(`Required static file is missing from dist: ${file}`);
  }
}

console.log(`Verified ${localReferences.length} relative references and GitHub Pages static assets.`);
