# ルーター — 種別判定とフロー選択

## 役割

`interview-summary.md` を主な入力として要件を軽量な共通ディスカバリーで整理し、4つのプロトタイプ種別のどれに該当するかを判定し、
対応するフローに誘導する。
ただしデフォルトでは、判定したらそのまま実装まで進まず、種別提案とスコープだけ確認する。

## 進め方

まず `projects/{プロジェクト名}/interview-summary.md` を読み、その後 [discovery.md](./flows/discovery.md) を使って以下の3点だけを整理する。

1. 目的整理
2. 曖昧さの整理
3. 成立条件の確認

この内容は `projects/{プロジェクト名}/project-requirements.md` に残す。
要件が足りない時だけ補足質問を行う。
補足質問は一度に 3 つ以下にする。

## 判定フロー

共通ディスカバリーの結果を踏まえて、必要なら以下の選択肢で確認する：

```
何を作りたいですか？

1. Webアプリ — ブラウザで動くアプリを作りたい
   例：タスク管理、ダッシュボード、フォーム、LP
   
2. Codexのスキル — Codexに新しい能力を追加したい
   例：特定の作業を自動化する skill、専門ワークフロー、レビュー支援
   
3. Workflow / ハーネス設計 — AIへの指示の仕組み自体を設計したい
   例：業務フローの自動化設計、プロンプト体系の構築
   
4. GPTs — ChatGPTのカスタムGPT用 prompt を作りたい
   例：社内Q&Aボット、専門アドバイザー、業務支援ツール
```

## 判定後のアクション

種別が決まったら：

1. `projects/{プロジェクト名}/` を作成する
2. `project-requirements.md` に共通ディスカバリー結果を記録する
3. 以下を短くユーザーに返し、合意を取る
   - 今回解く問題
   - 最小手段の提案
   - 作る範囲
   - 今は作らない範囲
4. 対応するフロー定義を読み込む
   - Web App → `harness/flows/webapp.md`
   - Codex Skills → `harness/flows/codex-skills.md`
   - Workflow / ハーネス設計 → `harness/flows/harness-design.md`
   - GPTs → `harness/flows/gpts.md`
5. 個別フローの Step 1 から開始する

## デフォルト進行モード

- `checkpointed`（デフォルト）
  ルーティング後に必ず一度止まり、ユーザー確認を取る。合意後はそのスコープの中でまとめて進める。
- `full-auto`（明示指示時のみ）
  ユーザーが一気通貫を希望した時だけ、確認を省略して次へ進む。

`interview-summary.md` が曖昧な場合は `full-auto` にしない。

## 自動判定（オプション）

`interview-summary.md` に具体的な要件がまとまっている場合、以下のキーワードで自動判定する：

| キーワード | 種別 |
|-----------|------|
| Webアプリ, サイト, 画面, UI, ブラウザ, ダッシュボード | Web App |
| Codex, skill, スキル, 自動化, SKILL.md | Codex Skills |
| ハーネス, フロー, Workflow, 設計, プロンプト体系 | Workflow / ハーネス設計 |
| GPT, ChatGPT, instructions, system prompt, ボット, アシスタント | GPTs |

自動判定した場合も、次の形で確認する。

```text
理解した課題: 〇〇
最小手段の提案: 〇〇
今回作る範囲: 〇〇
今回は作らない範囲: 〇〇

この前提で進めてよいですか？
```
