# Evaluator Input

You are an independent Web App evaluation agent. Evaluate only `/Users/ryota/Desktop/dev/evals_test/ultra_sprint_harness/projects/rookie-connect`. Do not edit any files.

## Allowed Inputs

- Artifact: `index.html`, `styles.css`, `app.js`
- Run URL: `http://127.0.0.1:4174`
- `project-requirements.md`
- `acceptance-criteria.md`
- `eval-cases.md`
- `eval-profile.md`
- `traceability.md`

Do not read any other project file, `README`, `AGENTS`, or parent history.

## Required Evaluation

Use the locally installed Playwright package and normal browser input (click/type), not source inspection alone. Create a QA inventory from REQ/C/E IDs and visible controls. Exercise E-01 through E-04, capture console errors, inspect desktop `1600x900` and mobile `390x844` viewports, inspect initial and post-interaction states, and perform a short off-happy-path exploratory pass.

Return a Playwright Evidence section containing the QA inventory, environment, individual actions and visible outcomes, console result, desktop/mobile visual result, exploratory result, and screenshot filenames or the statement that screenshots were inspected in-memory. Then return every mechanical gate, C-01 through C-05, E-01 through E-04 with dimension, test level where applicable, verdict, evidence, and reproduction for non-Pass. For first-time-user-only checks, return `Needs Review`. End with the overall verdict and loop decision.
