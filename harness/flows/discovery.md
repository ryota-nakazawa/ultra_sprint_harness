# 共通ディスカバリーフロー

## 概要

すべてのプロトタイプ作成の前に行う、軽量な共通整理フロー。
深い要件定義には入らず、「何を解くか」「何で解くか」「どこまでできれば十分か」だけを決める。
実運用では、インタビュー GPTs が作成した要件サマリー md を起点に進める。

## 入力

- `projects/{プロジェクト名}/interview-summary.md`

このファイルを主なインプットとして読む。
不足がある場合だけ、追加質問で補う。

## 成果物

- `projects/{プロジェクト名}/interview-summary.md` を前提とした整理結果
- `projects/{プロジェクト名}/project-requirements.md`
- 必要に応じて `projects/{プロジェクト名}/task-plan.md`
- 必要に応じて `projects/{プロジェクト名}/progress.md`
- 必要に応じて `projects/{プロジェクト名}/findings.md`
- 必要に応じて `projects/{プロジェクト名}/findings-diagrams/`

## フェーズ

### フェーズ1: 目的整理

まず `interview-summary.md` から以下を抜き出して整理する：

- 背景
- 課題
- 期待効果
- 制約
- 未確定事項

この段階では、分からないことを無理に埋めず `TBD` として残す。
要約に不足がある時だけ、追加質問を行う。

### フェーズ2: 解決手段の選定

`interview-summary.md` とフェーズ1の整理結果をもとに、以下の候補から最小実現手段を決める：

- GPTs
- Codex Skills
- Web App
- Workflow / ハーネス設計

選定時には以下を短く残す：

- なぜそれが最小か
- 他案を採らなかった理由
- 現時点のトレードオフ

### フェーズ3: 成立条件の確認

`interview-summary.md` にある利用者像、期待効果、制約をもとに以下を整理する：

- 誰が使うか
- 何ができれば PoC として十分か
- どこが未確定か

ここで、やり過ぎを防ぐために PoC のゴールラインを明確にする。

## planning-with-files の使い分け

実装や調査が 3 ステップ以上になりそうなら、`planning-with-files` の考え方を使って以下を作る。

- `task-plan.md` — フェーズ、タスク、進行状況
- `progress.md` — 実行ログ、テスト結果、次にやること
- `findings.md` — 調査メモ、意思決定、比較結果、未解決論点
- `findings-diagrams/` — 図で残した方が伝わる内容の出力先

単純な依頼では `project-requirements.md` だけでよい。

## `project-requirements.md` の最低限の構造

```markdown
# {プロジェクト名}

## 入力

- interview-summary: `interview-summary.md`

## 目的整理

- 背景:
- 課題:
- 期待効果:
- 制約:
- 未確定事項:

## 解決手段の選定

- 選定した手段:
- 選定理由:
- 採らなかった案:
- トレードオフ:

## 成立条件

- 想定ユーザー:
- PoC 成立条件:
- TBD:
```

## `interview-summary.md` の最低限の想定項目

```markdown
# Interview Summary

## 背景

## 現状課題

## 想定ユーザー

## やりたいこと

## 期待効果

## 制約

## 未確定事項
```

## `task-plan.md` の最低限の構造

```markdown
# Task Plan

## Phases

- [ ] フェーズ1:
- [ ] フェーズ2:
- [ ] フェーズ3:

## Current Focus

- いま進めていること:
- 次にやること:
```

## `progress.md` の最低限の構造

```markdown
# Progress

## Latest

- 実施したこと:
- 確認結果:
- 次にやること:
```

## `findings.md` の最低限の構造

```markdown
# Findings

## Notes

- 調査結果:
- 意思決定:
- 保留事項:
```

## `findings-diagrams/` の使い方

以下のような内容は、文章だけで残すより図にした方が伝わりやすい。

- 画面遷移
- データフロー
- コンポーネント構成
- 改善案の比較図

`mcp_excalidraw` が使える場合は、`findings.md` を元に Excalidraw で図を作る。
使えない場合は、Figma / FigJam の図生成または Mermaid を代替として使う。
