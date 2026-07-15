# GPTs フロー

## 概要

OpenAI のカスタム GPT を作るためのフロー。
まず `instructions.md` を整えることを最優先にし、やり取りを通じて system prompt を磨き、必要な場合だけ Actions や knowledge を追加する。

このフローは、共通ディスカバリーで「最小解決手段は GPTs」と決まった後に使う。
評価成果物と評価runは必ず [評価ディレクトリ標準](../evaluation-layout.md) の `evaluation/` 配下に置く。
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

実装に入る直前に、共通の [評価ゲート](./evaluation-gate.md) の Gate A を必ず通す。

```bash
python3 tools/check_preimplementation_readiness.py --project-dir projects/{プロジェクト名}
```

失敗した場合は `instructions.md` を作り始めない。`acceptance-criteria.md`、`eval-cases.md`、`eval-profile.md`、`traceability.md`、`evaluation-loop.md` を先に直す。

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

### Step 6.5: 合否判定と記録

共通の [評価ゲート](./evaluation-gate.md) の Gate B〜D に従う。
正式評価はサブエージェント前提で実施する。自己確認だけで `Pass / Fix / Needs Review` を記録してはいけない。

1. `projects/{プロジェクト名}/evaluation-status.md` を作り、自己確認、正式評価の方式、正式判定の記録可否を記入する。自己確認は参考確認としてのみ残す
2. 評価サブエージェントを `fresh_context` で起動し、`evaluation-runs/{run-id}/` に証跡を保存する
3. `python3 tools/check_evaluation_evidence.py --project-dir projects/{プロジェクト名} --run-id {run-id}` を実行する。失敗した場合は正式判定を記録せず、`evaluation-status.md` に未実施または不完全と残す
4. 証跡検査が成功した後にだけ、`projects/{プロジェクト名}/acceptance-criteria.md` の第1層・第2層を判定し、
   結果と判定日を記入する
5. `projects/{プロジェクト名}/eval-cases.md` のケースを判定し、
   代表ケース、境界ケース、失敗ケースのどこが弱いかを記録する
6. 判定サマリー（合格数・一発合格の Yes/No）を埋める
7. `sprint-metrics.md` のセクション 1〜2（試行回数、一発合格、フォールバック、手戻り主因、eval-cases の結果）を記入する

LLM で判定する項目は、実装担当とは別コンテキストの評価エージェントで行う。
評価エージェントには、成果物、実行手順、`project-requirements.md`、`acceptance-criteria.md`、`eval-cases.md`、`eval-profile.md`、必須の `traceability.md` だけを渡し、実装中の会話ログや背景説明は渡さない。
評価エージェントは、各項目について `ID / 評価観点 / Pass / Fix / Needs Review / 根拠 / 不合格時の再現手順` を返す。`acceptance-criteria.md` と `eval-cases.md` で宣言された評価観点だけを判定対象にし、安全性・権限・送信・削除などの高影響操作に不明点があれば `Needs Review` とする。

評価エージェントの起動時には `projects/{プロジェクト名}/evaluation-runs/{run-id}/` を作る。起動 API が返した agent ID と `fresh_context` を `receipt.json` に、実際の評価依頼を `evaluator-input.md` に、返答全文を `evaluator-result.md` に保存する。

評価結果に `Fix` がある場合は、実装へ戻して修正し、再評価する。自動修正は最大 2 回まで。3 回目の実装・評価には入らない。
`Needs Review` が 1 件でも出た場合、同じ ID が 2 回連続で `Fix` になった場合、または修正にスコープ変更や評価基準変更が必要な場合は、自動ループを止める。
止めた理由と要チェック項目は `eval-cases.md` と `sprint-metrics.md` に記録する。

`Fix` にしてよいのは、明らかな未実装、文言ミス、壊れた導線やエラー、条件に照らして明確に No のものだけ。
要件や評価基準が曖昧、顧客判断が必要、スコープを広げないと直せない、主観的な良し悪し、安全性の高い判断は `Needs Review` にする。**成果物に合わせて条件を緩めない**
（条件を変える場合は acceptance-criteria.md の変更履歴に理由を残す）。

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

### Step 10.5: 第3層の記録

1. `sprint-metrics.md` のセクション 3 を追記する
   （意思決定に足る学びを得たか / 決まったこと / 決まらなかったこと）
2. 成立条件をすべて満たしたのに意思決定につながらなかった場合は、
   どの条件が顧客の関心とズレていたかを `findings.md` に残し、
   `acceptance-criteria.md` の「デモ後のふりかえり」欄にも 1 行書く
3. デモ、レビュー、利用中に見つかった失敗や違和感は、
   次回から必ず評価するケースとして `eval-cases.md` の「追加ケース候補」に戻す
4. 新しい失敗や学びがあれば、AI に `findings.md`、`eval-cases.md`、`eval-profile.md` を読ませて `promotion-candidates.md` を下書きさせる。AI は共通カタログを直接編集せず、人が承認した候補だけを `harness/evals/catalog/` へ反映する

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
