#!/usr/bin/env node

const { classify } = require("../../projects/contact-triage-dryrun/triageRules.js");

let input = "";

process.stdin.setEncoding("utf8");
process.stdin.on("data", (chunk) => {
  input += chunk;
});

process.stdin.on("end", () => {
  try {
    const payload = JSON.parse(input || "{}");
    const result = classify(payload.text || "");
    process.stdout.write(JSON.stringify({
      urgency: result.urgency,
      category: result.category
    }));
  } catch (error) {
    process.stderr.write(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  }
});
