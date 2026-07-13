# Evaluator Input

> This file is the exact evaluation request given to the separate evaluator. Do not include implementation chat history or rationale.

## Artifact

- `{artifact paths or revision}`

## Run Instructions

1. {how to run or inspect the artifact}

## Evaluation Sources

- `project-requirements.md`
- `acceptance-criteria.md`
- `eval-cases.md`
- `eval-profile.md`
- `traceability.md` when present

## Evaluation Dimensions

Use the evaluation dimension declared for each acceptance criterion and eval case, such as `業務成功`, `誤実行`, `安全性`, `再現性`, or `運用負荷`.

- Judge only the dimensions declared in the evaluation sources. Do not infer extra quality requirements or fail an undeclared dimension.
- Include the applicable evaluation dimension and test level with every result.
- Treat uncertainty involving safety, permissions, sending, deletion, or other high-impact actions as `Needs Review`, not `Fix`.

## Traceability Check

When `traceability.md` is present, check that every `Must` requirement has at least one linked acceptance criterion and eval case. A missing link is `Needs Review`; do not invent a missing requirement or case.

## Required Response

For every applicable criterion and case, return only:

- ID, evaluation dimension, test level, and `Pass`, `Fix`, or `Needs Review`
- Evidence
- Reproduction steps for `Fix` or `Needs Review`

Do not edit the artifact. Do not rely on information outside this request.
