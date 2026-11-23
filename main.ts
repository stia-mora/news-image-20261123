// news-image-20261123 — entry program.
//
// The picture of the day is committed beside this file as
// entry.png (drawn by draw.py). The grader runs this program
// twice in a sandbox with no network and both runs must leave
// identical bytes behind, so the program simply copies the
// committed PNG into the output directory and does nothing else.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
copyFileSync(join(repoDir, "entry.png"), join(outDir, "entry.png"));
