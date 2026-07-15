# Evaluator Input

You are an independent evaluation agent. Evaluate only the Rookie Connect artifact at `/Users/ryota/Desktop/dev/evals_test/ultra_sprint_harness/projects/rookie-connect`. Do not edit any files.

## Allowed Inputs

1. Artifact files: `index.html`, `styles.css`, `app.js`
2. Run instruction: the static app is available at `http://localhost:4174`. Inspect source and, if possible, exercise the UI through normal browser interactions. You may run JavaScript syntax checks.
3. `project-requirements.md`
4. `acceptance-criteria.md`
5. `eval-cases.md`
6. `eval-profile.md`

Do not read `interview-summary.md`, `findings.md`, `task-plan.md`, `promotion-candidates.md`, `evaluation-status.md`, `subagent-evaluation-omission.md`, `README`, `AGENTS.md`, or any parent implementation conversation/history.

For every applicable mechanical gate, `C-01` through `C-05`, and `E-01` through `E-04`, return: ID, declared evaluation dimension, test level when applicable, `Pass` / `Fix` / `Needs Review`, evidence, and reproduction steps for non-Pass. Judge only declared dimensions. Treat uncertainty about safety, permissions, sending, deletion, or other high-impact actions as `Needs Review`. Do not edit the artifact. End with overall verdict and loop decision.
