#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const root = process.cwd();

const required = [
  "README.md",
  "POLICY.md",
  "RULES.md",
  "AGENTS.md",
  "package.json",
  "scripts/bootstrap.js",
  "scripts/verify-workspace.js",
  "scripts/agent-context.js",
  "Job Hunt/AGENTS.md",
  "Job Hunt/resumes",
  "reconciled-tracker-build/current_tracker.xlsx",
  "reconciled-tracker-build/gmail-sent-audit-2026-07-06.csv",
  "drive-extraction",
  ".planning/codebase/STRUCTURE.md",
];

const optional = [
  "Job Hunt/.git-nested-backup",
  "Job Hunt/pymupdf-venv",
];

const missing = required.filter((entry) => !fs.existsSync(path.join(root, entry)));

if (missing.length) {
  console.error("Workspace verification failed. Missing required paths:");
  for (const entry of missing) console.error(`  - ${entry}`);
  process.exit(1);
}

console.log("Workspace verification passed.");
console.log("");
console.log("Required paths are present.");
console.log("");
console.log("Machine-local paths intentionally not required:");
for (const entry of optional) {
  const exists = fs.existsSync(path.join(root, entry));
  console.log(`  - ${entry}: ${exists ? "present locally" : "not present, OK"}`);
}

