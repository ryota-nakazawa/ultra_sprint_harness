# Evaluator Input

> This file is the exact evaluation request given to the separate evaluator. Do not include implementation chat history or rationale.
> This file is mandatory evidence for formal `Pass / Fix / Needs Review`. Without a completed fresh-context subagent run, no formal verdict may be recorded.

## Artifact

- `{artifact paths or revision}`

## Run Instructions

1. {how to run or inspect the artifact}

## Evaluation Sources

- `project-requirements.md`
- `acceptance-criteria.md`
- `eval-cases.md`
- `eval-profile.md`
- `traceability.md`

## Evaluation Dimensions

Use the evaluation dimension declared for each acceptance criterion and eval case, such as `業務成功`, `誤実行`, `安全性`, `再現性`, or `運用負荷`.

- Judge only the dimensions declared in the evaluation sources. Do not infer extra quality requirements or fail an undeclared dimension.
- Include the applicable evaluation dimension and test level with every result.
- Treat uncertainty involving safety, permissions, sending, deletion, or other high-impact actions as `Needs Review`, not `Fix`.

## Traceability Check

`traceability.md` is required. Check that every `Must` requirement has at least one linked acceptance criterion and eval case. A missing link is `Needs Review`; do not invent a missing requirement or case.

## Web App User-Journey Evaluation

For a Web App, use Playwright and normal browser input before returning a verdict. Build a QA inventory from the requirements, acceptance criteria, eval cases, visible controls, and user-visible claims. Then:

- execute every applicable eval case with real clicks, typing, or touch input
- capture browser console errors during the primary flow
- inspect the initial screen and at least one meaningful post-interaction screen at desktop viewport; inspect a mobile viewport when the project claims mobile support
- complete a short exploratory pass outside the happy path
- record the inventory, environment, actions, visible outcomes, console result, and screenshot references in `playwright-evidence.md`

If Playwright cannot run, return `Needs Review` for every case that requires UI interaction. Source inspection is supporting evidence only and cannot replace a user-journey evaluation.

## Required Response

For every applicable criterion and case, return only:

- ID, evaluation dimension, test level, and `Pass`, `Fix`, or `Needs Review`
- Evidence
- Reproduction steps for `Fix` or `Needs Review`

Do not edit the artifact. Do not rely on information outside this request.
