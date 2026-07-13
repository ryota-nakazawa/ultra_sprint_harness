# AGENTS.md

This repository is a Codex-first harness for rapid prototyping.

## Purpose

Use this repository to decide the smallest useful prototype approach, then execute the matching flow.

Do not jump straight into implementation.
Start from the interview summary markdown, run lightweight discovery on top of it, then route into the correct prototype flow.

## Default Working Order

1. Read [README.md](/Users/ryota/Desktop/エージェント作成/超速スプリント/README.md) for the human-facing overview if needed.
2. Read `projects/{project_name}/interview-summary.md` if it exists.
3. Start with [harness/flows/discovery.md](/Users/ryota/Desktop/エージェント作成/超速スプリント/harness/flows/discovery.md).
4. Create or update `projects/{project_name}/project-requirements.md`.
5. Use [harness/router.md](/Users/ryota/Desktop/エージェント作成/超速スプリント/harness/router.md) to choose the smallest viable path.
6. Follow exactly one detailed flow:
   - [harness/flows/webapp.md](/Users/ryota/Desktop/エージェント作成/超速スプリント/harness/flows/webapp.md)
   - [harness/flows/codex-skills.md](/Users/ryota/Desktop/エージェント作成/超速スプリント/harness/flows/codex-skills.md)
   - [harness/flows/gpts.md](/Users/ryota/Desktop/エージェント作成/超速スプリント/harness/flows/gpts.md)
   - [harness/flows/harness-design.md](/Users/ryota/Desktop/エージェント作成/超速スプリント/harness/flows/harness-design.md)

## Core Rules

- Treat `interview-summary.md` as the default input artifact.
- Keep discovery light.
- Prefer the smallest viable solution.
- Leave unknowns as `TBD` instead of over-specifying.
- Use file-based planning for anything non-trivial.
- Record important decisions instead of keeping them only in chat context.
- Treat evals as lightweight loop engineering: use acceptance criteria and eval cases to make learning reproducible, not as a heavy production eval platform.
- Do not introduce automatic graders or eval runners by default; first create human/LLM-readable eval cases.
- When LLM judgment is used, use a separate evaluation agent/context from the implementation agent.
- Give the evaluation agent only the artifact, run instructions, `project-requirements.md`, `acceptance-criteria.md`, `eval-cases.md`, `eval-profile.md`, and `traceability.md` when present; do not include implementation chat history, rationale, or excuses.
- The evaluation agent returns ID, declared evaluation dimension, `Pass / Fix / Needs Review`, evidence, and reproduction steps for failures. Judge only declared dimensions; treat uncertainty about safety, permissions, sending, deletion, or other high-impact actions as `Needs Review`.
- For every LLM evaluation, create `projects/{project_name}/evaluation-runs/{run_id}/`. Save the agent ID returned by the orchestrator and `fresh_context` in `receipt.json`, the exact request in `evaluator-input.md`, and the full response in `evaluator-result.md`.
- During discovery, select only relevant entries from `harness/evals/catalog/` and snapshot the IDs and rationale in `eval-profile.md` before creating acceptance criteria and eval cases.
- Give each eval case a test level: `構成・単体`, `連携`, or `業務シナリオ`. Use `traceability.md` only for multi-feature, external-integration, high-impact, or coverage-risk projects.
- After project learnings emerge, have AI draft `promotion-candidates.md` from the project artifacts. AI must not edit the common catalog directly; only a human-approved candidate is promoted.
- Auto-fix only `Fix` items, with a maximum of 2 implementation/evaluation loops; do not start a third implementation/evaluation loop.
- Stop the loop when any `Needs Review` appears, the same ID is marked `Fix` twice in a row, the loop reaches 2 fixes, or the fix requires scope or criteria changes.
- For UI-heavy Web App work, create a visual direction image with Codex image generation before implementation when the screen look materially affects user acceptance.
- Use a worktree-first delivery style: make non-trivial harness or prototype changes in a dedicated branch/worktree when possible, then integrate into `main` only after the result looks good.

## Discovery Rules

Discovery should read the interview summary first, then answer these three questions:

1. What problem are we solving?
2. What is the smallest solution type?
3. What counts as success for the PoC?

Only ask follow-up questions when the interview summary is missing key information.
Do not expand discovery into a heavy requirements phase unless the task truly needs it.

## Routing Rules

Choose the flow based on the smallest viable output:

- `Web App` when a browser UI is needed.
- `Codex Skills` when Codex needs a reusable new capability.
- `GPTs` when the solution should live as a Custom GPT, usually prompt-first.
- `Workflow / ハーネス設計` when the main deliverable is the process itself.

If uncertain, return to discovery and reduce scope.

## File-First Planning

For simple tasks:

- `interview-summary.md` plus `project-requirements.md` is enough.
- `project-requirements.md` is enough.

For multi-step or ambiguous tasks, also use:

- `acceptance-criteria.md`
- `eval-cases.md`
- `task-plan.md`
- `progress.md`
- `findings.md`
- `findings-diagrams/` when diagrams communicate better than prose

Use these files to preserve decisions, status, findings, and handoff context.

## Flow-Specific Notes

### Web App

- Follow [harness/flows/webapp.md](/Users/ryota/Desktop/エージェント作成/超速スプリント/harness/flows/webapp.md).
- Default to a fast local prototype.
- Use `interview-summary.md` as the default source of user needs, actors, and constraints.
- Default to `HTML / CSS / JavaScript` for the frontend.
- Add Node.js only when backend or API mediation is needed.
- Base the visual design on the current NTT DATA blue-themed brand direction.
- For UI-heavy screens, generate a first-look image before coding and use user feedback to align the direction.
- Use `planning-with-files` style documents when the work becomes complex.
- Use `Understand-Anything` once the first prototype exists, then use it again later for structure understanding or impact analysis as needed.
- Use diagrams for findings when helpful:
  - screen transitions
  - data flow
  - component structure
  - comparison of improvement options

Call timing:

- `planning-with-files`: when the work is multi-step, has handoff risk, or needs decision history
- `imagegen`: after Web App requirements are confirmed and before implementation, when visual direction needs user buy-in
- `Understand-Anything`: immediately after the first working prototype exists, then later when you need structure or impact analysis
- `mcp_excalidraw`: in the first findings phase after the prototype is shown, then later when a diagram will explain updates faster

### Codex Skills

- Follow [harness/flows/codex-skills.md](/Users/ryota/Desktop/エージェント作成/超速スプリント/harness/flows/codex-skills.md).
- Treat this as creating a reusable Codex skill, not a one-off prompt.
- Extract triggers, inputs, outputs, and reusable steps from `interview-summary.md` first.
- Use the local [$skill-creator](/Users/ryota/.codex/skills/.system/skill-creator/SKILL.md) guidance and treat it as the standard path for implementation.
- Prefer concise `SKILL.md` files with clear trigger descriptions.
- When testing a skill, the final chat reply must demonstrate the skill's intended chat output, not just link to generated files. For report, minutes, review, analysis, or summary skills, include the readable Markdown body with headings, tables, bold labels, and visual anchors when appropriate.
- Use `Understand-Anything` once the first usable skill artifact exists, then use it again later for structure or impact analysis as needed.
- Use diagrams for findings when helpful:
  - trigger structure
  - input/output flow
  - file responsibility split
  - comparison of improvement options

Call timing:

- `planning-with-files`: when the work is multi-step, has handoff risk, or needs decision history
- `Understand-Anything`: immediately after the first usable skill artifact exists, then later when you need structure or impact analysis
- `mcp_excalidraw`: in the first findings phase after the skill is reviewed, then later when a diagram will explain updates faster

### GPTs

- Follow [harness/flows/gpts.md](/Users/ryota/Desktop/エージェント作成/超速スプリント/harness/flows/gpts.md).
- Default to prompt-first.
- Read role, audience, tone, and guardrails from `interview-summary.md` first.
- Start with `instructions.md`.
- Refine the system prompt through iterative dialogue rather than treating the first draft as final.
- Add `actions.json` or `knowledge/` only when truly needed.
- Use `Understand-Anything` once the first usable GPT artifact exists, then use it again later for structure or impact analysis as needed.
- Use diagrams for findings when helpful:
  - conversation flow
  - guardrail boundaries
  - actions/knowledge relationships
  - comparison of improvement options

Call timing:

- `planning-with-files`: when the work is multi-step, has handoff risk, or needs decision history
- `Understand-Anything`: immediately after the first usable GPT artifact exists, then later when you need structure or impact analysis
- `mcp_excalidraw`: in the first findings phase after the GPT is reviewed, then later when a diagram will explain updates faster

### Workflow / Harness Design

- Follow [harness/flows/harness-design.md](/Users/ryota/Desktop/エージェント作成/超速スプリント/harness/flows/harness-design.md).
- Focus on routing, shared structure, and reusable flow definitions.

## Diagrams

When a finding is easier to understand visually, create or propose diagrams for:

- screen transitions
- data flow
- component structure
- alternative comparison

Preferred tool:

- `mcp_excalidraw` when available

Fallbacks:

- FigJam / Figma diagram generation
- Mermaid

Diagrams complement `findings.md`; they do not replace it.

## What Not To Do

- Do not skip discovery.
- Do not choose a larger solution than necessary.
- Do not create heavy documentation by default.
- Do not turn every task into a full software process.
- Do not replace written findings with diagrams only.

## 計測ルール

このハーネスでは、スプリントの効果測定のため次を必ず守る。

- discovery の完了条件に `acceptance-criteria.md` の作成を含める
  （PoC 成立条件はすべて Yes / No で判定できる文にする）
- discovery の完了条件に `eval-cases.md` の作成を含める
  （代表ケース、境界ケース、失敗ケースを最低 1 件ずつ作る）
- 成果物の動作確認後、第1・2層と eval-cases を判定し `sprint-metrics.md` に記録する
- LLM 判定を使う場合は、実装担当とは別コンテキストの評価エージェントで判定する
- 評価エージェントには成果物、実行手順、`project-requirements.md`、`acceptance-criteria.md`、`eval-cases.md`、`eval-profile.md`、必要時の `traceability.md` だけを渡し、実装中の会話ログや背景説明は渡さない
- 評価エージェントは `ID / 宣言済みの評価観点 / Pass / Fix / Needs Review / 根拠 / 不合格時の再現手順` を返す。未定義の観点を推測して減点せず、安全性・権限・送信・削除などの高影響操作に不明点があれば `Needs Review` とする
- LLM 評価ごとに `projects/{プロジェクト名}/evaluation-runs/{run-id}/` を作り、オーケストレーターが返した agent ID と `fresh_context` を `receipt.json`、実際の依頼を `evaluator-input.md`、返答全文を `evaluator-result.md` に保存する
- discovery では `harness/evals/catalog/` から案件に必要な項目だけを選び、acceptance criteria と eval cases を作る前に `eval-profile.md` へ ID と採用理由を記録する
- 各 eval case には `構成・単体`、`連携`、`業務シナリオ` のテストレベルを付ける。`traceability.md` は複数機能、外部連携、高影響操作、または評価漏れが心配な案件だけで使う
- 案件の学びが出た後は、AI に案件成果物から `promotion-candidates.md` を下書きさせる。AI は共通カタログを直接更新せず、人が承認した候補だけを昇格する
- `Fix` は自動修正して再評価する。ただし自動修正は最大 2 回まで。3 回目の実装・評価には入らない
- `Needs Review` が出た、同じ ID が 2 回連続で `Fix` になった、上限に達した、スコープ変更や評価基準変更が必要になった場合は自動ループを止める
- デモ、レビュー、利用中に見つかった失敗は `findings.md` に残し、次回評価するケースとして `eval-cases.md` に戻す
- 成果物に合わせて成立条件を後から緩めない。変更する場合は変更履歴に理由を残す
- 記録は回数と Yes / No と学びのみでよい。利用量の単価換算や正確な工数は書かない
- 記録の記入がユーザーの負担にならないよう、埋められる項目は AI が下書きし、
  ユーザーには確認だけを求める
