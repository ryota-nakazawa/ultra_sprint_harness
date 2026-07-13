# Evaluator Input

You are an independent evaluation agent. Evaluate only the artifact at `/Users/ryota/Desktop/dev/evals_test/ultra_sprint_harness/projects/eval-loop-dryrun`. Do not edit any files.

You may use only these inputs:

1. The artifact files `index.html`, `styles.css`, `app.js`
2. Run instruction: inspect the static files and reason through clicking Increment and Reset in a browser
3. `acceptance-criteria.md`
4. `eval-cases.md`

Do not read implementation conversation/history, `eval-loop-log.md`, `findings.md`, `sprint-metrics.md`, `README`, or any other context.

For every applicable criterion/case, return `Pass`, `Fix`, or `Needs Review`, evidence, and reproduction steps for non-Pass results. End with overall verdict and loop decision.
