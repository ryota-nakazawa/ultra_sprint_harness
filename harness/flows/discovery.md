# 共通ディスカバリーフロー

## 概要

すべてのプロトタイプ作成の前に行う、軽量な共通整理フロー。
深い要件定義には入らず、「何を解くか」「何で解くか」「どこまでできれば十分か」だけを決める。
実運用では、インタビュー GPTs が作成した要件サマリー md を起点に進める。
`interview-summary.md` は曖昧さを含むことを前提とし、AI が勝手に補完して実装まで進まないよう checkpoint を入れる。

## 入力

- `projects/{プロジェクト名}/interview-summary.md`

このファイルを主なインプットとして読む。
不足がある場合だけ、追加質問で補う。

## 成果物

- `projects/{プロジェクト名}/interview-summary.md` を前提とした整理結果
- `projects/{プロジェクト名}/project-requirements.md`
- `projects/{プロジェクト名}/evaluation/eval-profile.md`
- `projects/{プロジェクト名}/evaluation/eval-cases.md`
- `projects/{プロジェクト名}/evaluation/traceability.md`
- `projects/{プロジェクト名}/evaluation/evaluation-loop.md`
- 必要に応じて `projects/{プロジェクト名}/task-plan.md`
- 必要に応じて `projects/{プロジェクト名}/progress.md`
- 必要に応じて `projects/{プロジェクト名}/findings.md`
- 必要に応じて `projects/{プロジェクト名}/findings-diagrams/`

## フェーズ

### フェーズ0: 理解したことと曖昧な点の切り分け

まず `interview-summary.md` を読み、以下を短く分けて整理する：

- 理解したこと
- 足りている情報
- 曖昧な点
- AI が勝手に決めるべきでない点

この段階では、すべての穴を埋めようとしない。
ただし以下の曖昧さは、そのまま先送りしない：

- 何の課題を解くのかが複数解釈できる
- 最小手段の候補が分かれる
- PoC 成立条件が曖昧で、作り過ぎや作り間違いが起きそう

質問は一度に 3 つ以下にし、答えがなくても進められる軽微な不明点は `TBD` として残す。

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

ここでは「AI が選んだ」ではなく、「この前提ならこれが最小」という形で提案する。
ユーザーが未合意のまま個別フローへ進まない。

### フェーズ3: 成立条件の確認

`interview-summary.md` にある利用者像、期待効果、制約をもとに以下を整理する：

- 誰が使うか
- 何ができれば PoC として十分か
- どこが未確定か

ここで、やり過ぎを防ぐために PoC のゴールラインを明確にする。

## 成立条件と eval ケースの判定可能化（discovery の完了条件）

「成立条件の確認」の最後に、次を行ってから routing に進む。

1. `harness/templates/common/acceptance-criteria.md` を複製して
   `projects/{プロジェクト名}/evaluation/acceptance-criteria.md` を作る
2. project-requirements.md の「PoC として何ができれば十分か」を、
   **Yes / No で判定できる文**に変換して第2層の表に書く（3〜7 項目）
   各条件には `業務成功 / 誤実行 / 安全性 / 再現性 / 運用負荷` の評価観点を 1 つ付ける
3. 「このプロトで顧客のどんな意思決定を引き出したいか」を仮説欄に 1〜2 文で書く
4. `harness/evals/catalog/` から今回必要な評価観点、ケースパターン、ドメインルール、テスト観点だけを選び、`harness/templates/common/eval-profile.md` を複製して `projects/{プロジェクト名}/evaluation/eval-profile.md` に選択 ID と採用理由を記録する。カタログを使わない場合は理由を 1 行残す
5. 選択した項目を案件の状況に具体化して、`harness/templates/common/eval-cases.md` を複製して
   `projects/{プロジェクト名}/evaluation/eval-cases.md` を作る
6. 代表ケース、境界ケース、失敗ケースを最低 1 件ずつ、合計 3〜7 件で書く
7. `harness/templates/common/traceability.md` を複製して `projects/{プロジェクト名}/evaluation/traceability.md` を作り、中核要件（`REQ-01` 形式）→ acceptance criterion → eval case の対応を記録する。単機能の軽い PoC でも省略しない
8. `harness/templates/common/evaluation-loop.md` を複製して `projects/{プロジェクト名}/evaluation/evaluation-loop.md` を作る。評価・修正・人間確認のたびに Mermaid と実行履歴を更新する
9. `harness/flows/evaluation-gate.md` を読み、Gate A の実装前ゲートを満たしているか確認する
10. 次のコマンドが成功するまで、個別フローの実装ステップへ進まない

```bash
python3 tools/check_preimplementation_readiness.py --project-dir projects/{プロジェクト名}
```

Yes / No の文に変換できない成立条件が残っている間は、曖昧さが残っているサイン。
そのまま実装に進まず、短くユーザーに確認する。
あわせて `harness/templates/common/sprint-metrics.md` も複製し、基本情報だけ埋めておく。

eval-cases.md は、重い自動評価基盤ではなく軽量な Evals ケース集として扱う。
初回は人間または LLM が読んで判定できる粒度で十分。自動 grader や runner は v1 では作らない。
共通カタログは選択元であり、案件ファイルの代わりにはしない。選択内容は必ず `eval-profile.md` に残す。

**禁止事項:** 成果物を作った後に、成果物に合わせて acceptance criteria や eval cases を初めて作る運用は禁止する。
実装中に条件変更が必要になった場合は、変更履歴に理由を書き、人間確認を挟む。

## checkpoint の入れ方

共通ディスカバリーでは、以下の順で短く返す。

1. 理解した課題
2. 曖昧で確認が必要な点
3. 現時点での最小手段の提案
4. PoC として十分なライン

ユーザー確認が必要なのは、次の場合だけ：

- 手段の候補が複数あり得る
- PoC 成立条件が複数解釈できる
- 実装に入ると後戻りコストが高い

逆に、以下は `TBD` で先に進めてよい：

- 細かな文言や命名
- 後から差し替えやすい UI 詳細
- その時点では未使用の拡張機能

## planning-with-files の使い分け

実装や調査が 3 ステップ以上になりそうなら、`planning-with-files` の考え方を使って以下を作る。

- `task-plan.md` — フェーズ、タスク、進行状況
- `progress.md` — 実行ログ、テスト結果、次にやること
- `findings.md` — 調査メモ、意思決定、比較結果、未解決論点
- `findings-diagrams/` — 図で残した方が伝わる内容の出力先

単純な依頼でも実装に入る場合は Gate A の評価ファイル一式が必要。
`project-requirements.md` だけでよいのは、discovery メモ段階または実装しない相談段階までとする。

共通ディスカバリーで決めるべきことは次の通り：

- `planning-with-files` を有効にするか
- 有効にするなら、最初から必要なファイルは何か
- 初回 findings で何を図にするか
- 初回プロト完成後に `Understand-Anything` をどこで入れるか

この段階での原則は以下：

- `planning-with-files` は discovery 中から使ってよい
- `Understand-Anything` は discovery では使わない
- `mcp_excalidraw` は discovery の代わりに使わない
- ただし Web App スプリントでは、後工程で両方を使う前提で段取りを決める

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

## 曖昧さの整理

- 理解したこと:
- 確認が必要な点:
- `TBD` で進める点:

## 解決手段の選定

- 選定した手段:
- 選定理由:
- 採らなかった案:
- トレードオフ:

## 成立条件

- 想定ユーザー:
- PoC 成立条件:
- TBD:

## 中核要件（複数機能・高リスク案件で使う）

- REQ-01:
```

## `eval-cases.md` の最低限の構造

```markdown
# eval-cases.md

## 基本情報

- プロジェクト名:
- ルート種別:

## 評価観点

- 業務成功:
- 誤実行:
- 安全性:
- 再現性:
- 運用負荷:

## ケース一覧

| ID | 種別 | 評価観点 | 入力 | 期待される振る舞い | NG 例 | 採点方法 | 結果 | メモ |
|---|---|---|---|---|---|---|---|---|
| E-01 | 代表 | 業務成功 | | | | 人間 | | |
| E-02 | 境界 | 再現性 | | | | 人間 | | |
| E-03 | 失敗 | 誤実行 | | | | 人間 | | |

## 追加ケース候補

- デモ、レビュー、利用中に見つかった失敗を次回評価ケースへ戻す。
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

図を先に作るのではなく、次の順で進める：

1. `findings.md` に文章で整理する
2. どの図が必要かを決める
3. `mcp_excalidraw` が使えれば図にする
4. 使えなければ Mermaid などに落とす
