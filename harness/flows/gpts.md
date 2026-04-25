# GPTs フロー

## 概要

OpenAI のカスタム GPT を作るためのフロー。
まず `instructions.md` を整えることを最優先にし、やり取りを通じて system prompt を磨き、必要な場合だけ Actions や knowledge を追加する。

このフローは、共通ディスカバリーで「最小解決手段は GPTs」と決まった後に使う。
デフォルトでは、役割と禁止事項の確認が終わるまで生成に入らない。
このスプリントでは、初回 findings フェーズで `mcp_excalidraw` を使い、初回成果物完成直後に `Understand-Anything` を使う。

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

次が曖昧な場合は `instructions.md` を確定させない：

- GPT の役割
- 想定ユーザー
- 絶対にやらないこと

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

この整理にユーザー合意を取ってから Step 3 に進む。

### Step 3: Instructions生成

以下の構造で `instructions.md` を作成する：

1. **役割定義** — あなたは〇〇です
2. **行動指針** — こう振る舞ってください
3. **知識範囲** — こういう知識を持っています
4. **制約** — こういうことはしないでください
5. **出力形式** — 回答はこの形式で

合意済みの範囲ではまとめて作成してよいが、Actions や knowledge の追加で GPT の性質が変わる場合は再確認する。
最初の版を完成版とみなさず、会話とテストを通じて磨く前提で進める。

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
4. ユーザーとのやり取りで口調、役割、禁止事項を磨く

### Step 7: デプロイガイド

GPTの作成手順をユーザーに案内：
1. ChatGPTでGPT作成画面を開く
2. 生成された `instructions.md` を貼り付ける
3. `conversation_starters.md` があれば設定する
4. Actions があればスキーマを設定する
5. ナレッジファイルがあればアップロードする
6. 公開設定を選択する

### Step 8: 初回 findings と図の整理

1. 初回成果物で分かったことを `findings.md` に整理する
2. `mcp_excalidraw` を使って、少なくとも 1 つ図を作る
3. 図の候補は次から選ぶ
   - 会話フロー
   - guardrail と禁止事項の境界
   - `instructions.md` と `actions.json` / `knowledge/` の関係
   - 改善案の比較図
4. `mcp_excalidraw` が使えない場合は、Figma / FigJam の図生成または Mermaid を代替として使う

### Step 9: 初回成果物完成後の構造理解

1. 初回成果物が成立したら `Understand-Anything` を使う
2. prompt 構造、Actions、knowledge の依存関係を整理する
3. 次のフィードバック反映で壊しやすい箇所を `findings.md` または `progress.md` に残す

### Step 10: フィードバックループ

```
触ってみてどうですか？

- 変えたい返答の仕方
- 追加したい振る舞い
- 削除したい機能や制約

があれば教えてください。なければ「完成」と言ってください。
```

フィードバックがあれば Step 3 に戻る。

## Codexとの連携

GPTs の設計では Codex を以下で活用する：
- `instructions.md` の推敲と構造化
- `conversation_starters.md` の作成
- Actions スキーマの生成と検証
- knowledge 用ファイルの整理と加工

## 注意事項

- `mcp_excalidraw` は初回 findings フェーズで使うが、prompt 設計そのものの代替にはしない
- `Understand-Anything` は初回成果物完成直後から使い、役割定義前の手段選定には使わない
- GPTs は一発生成ではなく、対話を通じて system prompt を磨く前提で進める
- 図は `findings.md` を置き換えるものではなく、文章の補助として残す
