import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
const here = dirname(fileURLToPath(import.meta.url));
const out = process.env.OUTPUT_PATH ?? join(process.env.MAKEFUN_OUTPUT_DIR ?? "/output", "entry.png");
mkdirSync(dirname(out), { recursive: true });
copyFileSync(join(here, "entry.png"), out);
console.log("wrote", out);
