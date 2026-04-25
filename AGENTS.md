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
- Use `planning-with-files` style documents when the work becomes complex.
- Use `Understand-Anything` once the first prototype exists, then use it again later for structure understanding or impact analysis as needed.
- Use diagrams for findings when helpful:
  - screen transitions
  - data flow
  - component structure
  - comparison of improvement options

Call timing:

- `planning-with-files`: when the work is multi-step, has handoff risk, or needs decision history
- `Understand-Anything`: immediately after the first working prototype exists, then later when you need structure or impact analysis
- `mcp_excalidraw`: in the first findings phase after the prototype is shown, then later when a diagram will explain updates faster

### Codex Skills

- Follow [harness/flows/codex-skills.md](/Users/ryota/Desktop/エージェント作成/超速スプリント/harness/flows/codex-skills.md).
- Treat this as creating a reusable Codex skill, not a one-off prompt.
- Extract triggers, inputs, outputs, and reusable steps from `interview-summary.md` first.
- Use the local [$skill-creator](/Users/ryota/.codex/skills/.system/skill-creator/SKILL.md) guidance and treat it as the standard path for implementation.
- Prefer concise `SKILL.md` files with clear trigger descriptions.
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
