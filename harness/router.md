# ルーター — 種別判定とフロー選択

## 役割

`interview-summary.md` を主な入力として要件を軽量な共通ディスカバリーで整理し、4つのプロトタイプ種別のどれに該当するかを判定し、
対応するフローに誘導する。

## 進め方

まず `projects/{プロジェクト名}/interview-summary.md` を読み、その後 [discovery.md](./flows/discovery.md) を使って以下の3点だけを整理する。

1. 目的整理
2. 解決手段の選定
3. 成立条件の確認

この内容は `projects/{プロジェクト名}/project-requirements.md` に残す。
要件が足りない時だけ補足質問を行う。

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
3. 対応するフロー定義を読み込む
   - Web App → `harness/flows/webapp.md`
   - Codex Skills → `harness/flows/codex-skills.md`
   - Workflow / ハーネス設計 → `harness/flows/harness-design.md`
   - GPTs → `harness/flows/gpts.md`
4. 個別フローの Step 1 から開始する

## 自動判定（オプション）

`interview-summary.md` に具体的な要件がまとまっている場合、以下のキーワードで自動判定する：

| キーワード | 種別 |
|-----------|------|
| Webアプリ, サイト, 画面, UI, ブラウザ, ダッシュボード | Web App |
| Codex, skill, スキル, 自動化, SKILL.md | Codex Skills |
| ハーネス, フロー, Workflow, 設計, プロンプト体系 | Workflow / ハーネス設計 |
| GPT, ChatGPT, instructions, system prompt, ボット, アシスタント | GPTs |

自動判定した場合も「〇〇を作るということで合っていますか？」と確認する。
