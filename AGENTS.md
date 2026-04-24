# AGENTS.md

This repository is a Codex-first harness for rapid prototyping.

## Purpose

Use this repository to decide the smallest useful prototype approach, then execute the matching flow.

Do not jump straight into implementation.
Start with lightweight discovery, then route into the correct prototype flow.

## Default Working Order

1. Read [README.md](/Users/ryota/Desktop/エージェント作成/超速スプリント/README.md) for the human-facing overview if needed.
2. Start with [harness/flows/discovery.md](/Users/ryota/Desktop/エージェント作成/超速スプリント/harness/flows/discovery.md).
3. Create or update `projects/{project_name}/project-requirements.md`.
4. Use [harness/router.md](/Users/ryota/Desktop/エージェント作成/超速スプリント/harness/router.md) to choose the smallest viable path.
5. Follow exactly one detailed flow:
   - [harness/flows/webapp.md](/Users/ryota/Desktop/エージェント作成/超速スプリント/harness/flows/webapp.md)
   - [harness/flows/codex-skills.md](/Users/ryota/Desktop/エージェント作成/超速スプリント/harness/flows/codex-skills.md)
   - [harness/flows/gpts.md](/Users/ryota/Desktop/エージェント作成/超速スプリント/harness/flows/gpts.md)
   - [harness/flows/harness-design.md](/Users/ryota/Desktop/エージェント作成/超速スプリント/harness/flows/harness-design.md)

## Core Rules

- Keep discovery light.
- Prefer the smallest viable solution.
- Leave unknowns as `TBD` instead of over-specifying.
- Use file-based planning for anything non-trivial.
- Record important decisions instead of keeping them only in chat context.

## Discovery Rules

Discovery should only answer these three questions:

1. What problem are we solving?
2. What is the smallest solution type?
3. What counts as success for the PoC?

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
- Use `planning-with-files` style documents when the work becomes complex.
- Use `Understand-Anything` later for structure understanding or impact analysis when the app grows.
- Use diagrams for findings when helpful:
  - screen transitions
  - data flow
  - component structure
  - comparison of improvement options

### Codex Skills

- Follow [harness/flows/codex-skills.md](/Users/ryota/Desktop/エージェント作成/超速スプリント/harness/flows/codex-skills.md).
- Treat this as creating a reusable Codex skill, not a one-off prompt.
- Use the local [$skill-creator](/Users/ryota/.codex/skills/.system/skill-creator/SKILL.md) guidance.
- Prefer concise `SKILL.md` files with clear trigger descriptions.

### GPTs

- Follow [harness/flows/gpts.md](/Users/ryota/Desktop/エージェント作成/超速スプリント/harness/flows/gpts.md).
- Default to prompt-first.
- Start with `instructions.md`.
- Add `actions.json` or `knowledge/` only when truly needed.

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
