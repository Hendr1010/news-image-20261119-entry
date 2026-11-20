// News-image entry for 19 November 2026, written fresh in this session.
// The image lives beside this file as entry.png; the program only copies it
// to the grader output folder. Node standard library only, no network, no
// extra packages, so it runs the same in the sealed grader container.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const source = new URL("./entry.png", import.meta.url);
const target = join(outDir, "entry.png");
copyFileSync(source, target);
// Fail loudly instead of shipping an empty image if the copy went wrong.
import { statSync } from "node:fs";
if (statSync(target).size === 0) {
  throw new Error("entry.png copied as an empty file");
}
