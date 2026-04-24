# GPTs フロー

## 概要

OpenAI のカスタム GPT を作るためのフロー。
まず `instructions.md` を整えることを最優先にし、必要な場合だけ Actions や knowledge を追加する。

このフローは、共通ディスカバリーで「最小解決手段は GPTs」と決まった後に使う。

## 成果物

- `instructions.md` — GPT のシステムプロンプト
- `conversation_starters.md` — 会話の開始例（推奨）
- `actions.json` — OpenAPI 形式の Actions スキーマ（必要な場合のみ）
- `knowledge/` — アップロード用のナレッジファイル（必要な場合のみ）

## モード

### Prompt-only（デフォルト）

- まず system prompt だけを整えたい場合
- 成果物は `instructions.md` を中心に作る
- 必要なら `conversation_starters.md` だけ追加する

### GPT package（拡張）

- 外部 API やアップロード知識も含めて整えたい場合
- `instructions.md` に加えて `actions.json` や `knowledge/` を扱う

## ステップ

### Step 1: GPT の振る舞い整理

**必須：**
- このGPTは何をするものか？
- 誰が使うか？
- GPTはどんな口調・キャラクターで話すか？
- 絶対にやらないことは何か？

**任意：**
- 参考にしたい既存のGPTやチャットボットはあるか？
- 外部のAPIやデータを使う必要はあるか？
- アップロードしたい資料やドキュメントはあるか？

### Step 2: GPT設計の整理と確認

```
【GPT名】
【一言で】〇〇のためのアシスタント
【モード】Prompt-only / GPT package
【ユーザー】〇〇
【キャラクター】
  - 口調: 〇〇（丁寧 / カジュアル / 専門的）
  - 役割: 〇〇
【できること】
  - 〇〇
  - 〇〇
【やらないこと】
  - 〇〇
【会話の開始例】
  - 「〇〇について教えて」
  - 「〇〇を分析して」
```

### Step 3: Instructions生成

以下の構造で `instructions.md` を作成する：

1. **役割定義** — あなたは〇〇です
2. **行動指針** — こう振る舞ってください
3. **知識範囲** — こういう知識を持っています
4. **制約** — こういうことはしないでください
5. **出力形式** — 回答はこの形式で

### Step 4: Actions設計（必要な場合）

外部 API 連携が必要な場合だけ実施する：
1. 必要なAPIエンドポイントを特定
2. OpenAPI形式のスキーマを生成
3. 認証方式を設定

### Step 5: Knowledge整理（必要な場合）

アップロード資料が必要な場合だけ実施する：
1. 何を knowledge に入れるか決める
2. GPT が読む前提で、資料を短く整理する
3. 不要な重複やノイズを削る

### Step 6: テスト用の会話シミュレーション

Codex 上で GPT の振る舞いをシミュレーションする：
1. 会話の開始例を使って対話をテスト
2. エッジケース（想定外の質問）への対応を確認
3. `instructions.md` を調整

### Step 7: デプロイガイド

GPTの作成手順をユーザーに案内：
1. ChatGPTでGPT作成画面を開く
2. 生成された `instructions.md` を貼り付ける
3. `conversation_starters.md` があれば設定する
4. Actions があればスキーマを設定する
5. ナレッジファイルがあればアップロードする
6. 公開設定を選択する

## Codexとの連携

GPTs の設計では Codex を以下で活用する：
- `instructions.md` の推敲と構造化
- `conversation_starters.md` の作成
- Actions スキーマの生成と検証
- knowledge 用ファイルの整理と加工
