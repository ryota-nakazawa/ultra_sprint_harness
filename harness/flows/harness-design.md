# ハーネス設計フロー（メタフロー）

## 概要

ハーネス（AIへの指示フロー）自体を設計するためのフロー。
業務プロセスやワークフローをAI実行可能な形に構造化する。

このフローは、共通ディスカバリーで「最小解決手段は Workflow / ハーネス設計」と決まった後に使う。
評価成果物と評価runは必ず [評価ディレクトリ標準](../evaluation-layout.md) の `evaluation/` 配下に置く。
デフォルトでは、設計方針と checkpoint の位置が固まるまで詳細フローを書き始めない。

## 成果物

- ハーネス定義ファイル一式（router.md, flows/*.md, templates/）
- 必要に応じてCLAUDE.mdの更新

## 変更運用

ハーネス自体の修正は、原則として作業ブランチまたは Git worktree で行う。
動作や読みやすさを確認し、良さそうなものだけ `main` に統合する。
小さな文言修正でも、後から判断理由を追えるように重要な変更意図は `project-requirements.md`、`progress.md`、または該当フロー本文に残す。

## ステップ

### Step 1: 目的のヒアリング（対話）

**必須：**
- このハーネスで何を実現したいか？
- 対象ユーザーは誰か？（AIを使う人のスキルレベル）
- どんな種類のタスクを扱うか？

**任意：**
- 既存のワークフローや手順書はあるか？
- 成果物の品質基準はあるか？

### Step 2: フロー構造の設計

以下を整理する：

```
【ハーネス名】
【目的】〇〇を簡単に作れるようにする
【対象ユーザー】〇〇
【タスク種別】
  - 種別A: 〇〇 → 成果物A
  - 種別B: 〇〇 → 成果物B
【共通ステップ】
  1. ヒアリング
  2. 曖昧さ確認
  3. 設計確認
  4. 実行
  5. フィードバック
【種別固有のステップ】
  - 種別Aでは〇〇も行う
```

### Step 3: ルーター設計

ルーターやフロー定義を実装し始める前に、共通の [評価ゲート](./evaluation-gate.md) の Gate A を必ず通す。

```bash
python3 tools/check_preimplementation_readiness.py --project-dir projects/{プロジェクト名}
```

失敗した場合はフロー本文の変更に進まない。`acceptance-criteria.md`、`eval-cases.md`、`eval-profile.md`、`traceability.md`、`evaluation-loop.md` を先に直す。

- 種別の判定ロジックを定義
- ユーザーへの選択肢提示文を作成
- 自動判定キーワードを設定
- 外部 skill / tool を呼ぶ条件を定義

### Step 4: 各フローの詳細設計

種別ごとに：
1. ヒアリング項目の定義
2. 確認フォーマットの定義
3. 実行手順の定義
4. フィードバックループの定義
5. `planning-with-files` / `Understand-Anything` / `mcp_excalidraw` をいつ呼ぶかの定義
6. UI や見た目の納得感が重要なフローでは、実装前に画像生成で方向性確認を行うかの定義

外部 skill / tool の定義は、最低でも次を含める：

- 呼ぶ前提条件
- 呼ばない条件
- 入力
- 出力
- どの checkpoint の前後で呼ぶか

このスプリントでは、少なくとも次を標準にする：

- `Web App` `Codex Skills` `GPTs` の初回 findings フェーズで `mcp_excalidraw`
- `Web App` `Codex Skills` `GPTs` の初回成果物完成直後で `Understand-Anything`

### Step 5: テンプレート作成

各種別の成果物テンプレートを作成

### Step 6: 統合テスト

1. サンプル要件で各フローを通しで実行
2. 非エンジニアの視点で分かりにくい箇所を修正

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

評価エージェントの起動時には `projects/{プロジェクト名}/evaluation/runs/{run-id}/` を作る。起動 API が返した agent ID、`fresh_context`、評価時点の commit・要件・eval cases・成果物のhash、モデル設定を `receipt.json` に、実際の評価依頼を `evaluator-input.md` に、返答全文を `evaluator-result.md` に保存する。

評価結果に `Fix` がある場合は、実装へ戻して修正し、再評価する。自動修正は最大 2 回まで。3 回目の実装・評価には入らない。
`Needs Review` が 1 件でも出た場合、run全体の `Fix` が 2 回発生した場合、または修正にスコープ変更や評価基準変更が必要な場合は、自動ループを止める。
止めた理由と要チェック項目は `eval-cases.md` と `sprint-metrics.md` に記録する。

`Fix` にしてよいのは、明らかな未実装、文言ミス、壊れた導線やエラー、条件に照らして明確に No のものだけ。
要件や評価基準が曖昧、顧客判断が必要、スコープを広げないと直せない、主観的な良し悪し、安全性の高い判断は `Needs Review` にする。**成果物に合わせて条件を緩めない**
（条件を変える場合は acceptance-criteria.md の変更履歴に理由を残す）。

### Step 6.6: 第3層の記録

1. `sprint-metrics.md` のセクション 3 を追記する
   （意思決定に足る学びを得たか / 決まったこと / 決まらなかったこと）
2. 成立条件をすべて満たしたのに意思決定につながらなかった場合は、
   どの条件が顧客の関心とズレていたかを `findings.md` に残し、
   `acceptance-criteria.md` の「デモ後のふりかえり」欄にも 1 行書く
3. デモ、レビュー、利用中に見つかった失敗や違和感は、
   次回から必ず評価するケースとして `eval-cases.md` の「追加ケース候補」に戻す
4. 新しい失敗や学びがあれば、AI に `findings.md`、`eval-cases.md`、`eval-profile.md` を読ませて `promotion-candidates.md` を下書きさせる。AI は共通カタログを直接編集せず、人が承認した候補だけを `harness/evals/catalog/` へ反映する

## 設計原則（ハーネスを設計する際のガイドライン）

1. **質問は3つ以下に** — 一度に聞く質問は最大3つ
2. **専門用語を使わない** — 技術的な概念は裏側に隠す
3. **デフォルトを用意する** — 判断を求めない。迷ったらこちらが決める
4. **確認ポイントを設ける** — 作り始める前に必ず「これで合っていますか？」
5. **やり直しを前提にする** — 一発で完璧を目指さない。フィードバックループを必ず入れる
