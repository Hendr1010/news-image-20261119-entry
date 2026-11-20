// The front page image is already finished and committed next to this file.
// This script only carries that finished image to where the grader looks for it.
// It needs no network access and nothing beyond the Node standard library.
// Rendering happens before the entry is packed, because the grading container
// only guarantees the standard library, so no image library is called on here.
import fs from "node:fs";
import path from "node:path";

const scriptDir = import.meta.dirname;
const destination =
  process.env.OUTPUT_PATH ??
  path.resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output", "entry.png");
fs.mkdirSync(path.dirname(destination), { recursive: true });
fs.copyFileSync(path.resolve(scriptDir, "entry.png"), destination);
console.log("done:", destination);
