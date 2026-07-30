#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const cp = require("child_process");

const REPO_URL = "https://github.com/lordpardonme/job-hunt-workspace-private.git";
const DEFAULT_DIR = "job-hunt-workspace-private";

function run(command, args, options = {}) {
  const result = cp.spawnSync(command, args, {
    stdio: "inherit",
    shell: process.platform === "win32",
    ...options,
  });
  if (result.status !== 0) {
    process.exit(result.status || 1);
  }
}

function commandExists(command) {
  const result = cp.spawnSync(command, ["--version"], {
    stdio: "ignore",
    shell: process.platform === "win32",
  });
  return result.status === 0;
}

function printLocalNextSteps(root) {
  console.log("");
  console.log("Job Hunt workspace is ready.");
  console.log("");
  console.log(`Workspace: ${root}`);
  console.log("");
  console.log("Next commands:");
  console.log("  npm run verify");
  console.log("  npm run agent:context");
  console.log("");
  console.log("Important files for agents:");
  console.log("  AGENTS.md   <- start here; complete handoff doc");
  console.log("  POLICY.md");
  console.log("  Job Hunt/AGENTS.md");
  console.log("  README.md");
  console.log("");
}

function verifyLocal(root) {
  const required = [
    "README.md",
    "POLICY.md",
    "AGENTS.md",
    "Job Hunt",
    "Job Hunt/resumes",
    "reconciled-tracker-build",
    "reconciled-tracker-build/current_tracker.xlsx",
    "drive-extraction",
  ];

  const missing = required.filter((entry) => !fs.existsSync(path.join(root, entry)));
  if (missing.length) {
    console.error("Workspace is missing required paths:");
    for (const entry of missing) console.error(`  - ${entry}`);
    process.exit(1);
  }
}

function main() {
  const args = process.argv.slice(2);
  const local = args.includes("--local");
  const cleanArgs = args.filter((arg) => arg !== "--local");

  if (local) {
    const root = process.cwd();
    verifyLocal(root);
    printLocalNextSteps(root);
    return;
  }

  if (!commandExists("git")) {
    console.error("Git is required before this bootstrap can clone the workspace.");
    console.error("Install Git, authenticate to GitHub, then retry.");
    process.exit(1);
  }

  const targetDir = path.resolve(process.cwd(), cleanArgs[0] || DEFAULT_DIR);

  if (fs.existsSync(targetDir)) {
    console.log(`Target already exists: ${targetDir}`);
    console.log("Skipping clone and running local verification.");
  } else {
    console.log(`Cloning private workspace into: ${targetDir}`);
    console.log("If this fails, authenticate first with: gh auth login");
    run("git", ["clone", REPO_URL, targetDir]);
  }

  run("npm", ["run", "verify"], { cwd: targetDir });
  printLocalNextSteps(targetDir);
}

main();

