# Codex Skills フロー

## 概要

Codex 用の skill を作るフロー。
ユーザーが繰り返す作業や専門手順を、再利用可能な `SKILL.md` と付随リソースに整理する。

このフローは、共通ディスカバリーで「最小解決手段は Codex Skills」と決まった後に使う。
評価成果物と評価runは必ず [評価ディレクトリ標準](../evaluation-layout.md) の `evaluation/` 配下に置く。
デフォルトでは、trigger と入力/出力の境界が固まるまで実装に入らない。
このスプリントでは、初回 findings フェーズで `mcp_excalidraw` を使い、初回成果物完成直後に `Understand-Anything` を使う。

## 成果物

- skill フォルダ一式
- `SKILL.md`
- 必要に応じて `agents/openai.yaml`
- 必要に応じて `scripts/`, `references/`, `assets/`

## ステップ

### Step 1: trigger と作業境界の整理

共通ディスカバリーで整理した内容を前提に、skill として再利用するための条件を詰める。

**必須：**
- どんな作業を自動化したいか？
- その作業はいつ、どんな時にやるか？
- ユーザーは Codex に何と頼みそうか？
- 入力は何か？（ファイル、テキスト、URL 等）
- 出力は何か？（ファイル生成、コード修正、レポート等）
- Codex のチャット本文には何を、どの見た目で返すか？

**任意：**
- 今その作業にどれくらい時間がかかっているか？
- 作業の中で判断が必要な部分はあるか？
- 決まった手順や参照資料はあるか？

次が曖昧な場合は `SKILL.md` を書き始めない：

- どんな依頼で発火するか
- 入力は何か
- 出力は何か
- どこまでを skill の責任にするか

### Step 2: スキル設計の整理と確認

```
【スキル名】〇〇
【一言で】〇〇を安定して進める Codex skill
【想定トリガー】ユーザーがこう言ったら使う
【入力】Codex が受け取るもの
【処理の流れ】
  1. 〇〇を読み取る
  2. 〇〇を分析する
  3. 必要なら references や scripts を使う
  4. 〇〇を生成/修正する
【出力】〇〇
【チャット表示】Codex の返答本文で見せる要約、表、セクション、絵文字・アイコン等
【追加ファイル】scripts / references / assets が必要か
```

この整理にユーザー合意を取ってから Step 3 に進む。

### Step 3: 実装

実装に入る直前に、共通の [評価ゲート](./evaluation-gate.md) の Gate A を必ず通す。

```bash
python3 tools/check_preimplementation_readiness.py --project-dir projects/{プロジェクト名}
```

失敗した場合は `SKILL.md` を書き始めない。`acceptance-criteria.md`、`eval-cases.md`、`eval-profile.md`、`traceability.md`、`evaluation-loop.md` を先に直す。

1. `skill-creator` skill を使って、skill の骨組みを設計する
2. スキル名をハイフン区切りで決める
3. `projects/{プロジェクト名}/{スキル名}/` に skill フォルダを作る
4. `SKILL.md` に以下を含める：
   - YAML frontmatter の `name` と `description`
   - いつ使う skill か
   - どう進めるかの手順
   - 追加ファイルを読む条件
   - 出力の期待値
   - Codex チャット本文での表示形式
5. 必要な場合だけ `scripts/`, `references/`, `assets/`, `agents/openai.yaml` を追加する

合意済みのトリガーと境界の中では、実装はまとめて進めてよい。

### Step 4: テスト実行

1. 実際の依頼文に近いプロンプトで試す
2. skill が発火すべき条件と、本文の指示が噛み合っているか確認する
3. テスト用の入力 artifact と出力 artifact を必要に応じて保存する
4. Codex の最終チャット返信にも、ユーザーがファイルを開かなくても価値が分かる代表出力を直接表示する
5. 出力がレポート、議事録、レビュー、分析、要約などの読ませる成果物なら、チャット本文で以下を満たすか確認する
   - 冒頭に何が分かったか、または結論がある
   - 見出し、表、太字ラベル、必要に応じた絵文字・アイコンでスキャンしやすい
   - ファイルリンクは補助であり、本文の代替になっていない
   - 次にユーザーが判断・確認すべき点が分かる
6. 冗長な説明がないか確認する
7. 必要なら `SKILL.md`、サンプル出力、付随ファイルを調整する

### Step 4.5: 合否判定と記録

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
`Needs Review` が 1 件でも出た場合、同じ ID が 2 回連続で `Fix` になった場合、または修正にスコープ変更や評価基準変更が必要な場合は、自動ループを止める。
止めた理由と要チェック項目は `eval-cases.md` と `sprint-metrics.md` に記録する。

`Fix` にしてよいのは、明らかな未実装、文言ミス、壊れた導線やエラー、条件に照らして明確に No のものだけ。
要件や評価基準が曖昧、顧客判断が必要、スコープを広げないと直せない、主観的な良し悪し、安全性の高い判断は `Needs Review` にする。**成果物に合わせて条件を緩めない**
（条件を変える場合は acceptance-criteria.md の変更履歴に理由を残す）。

#### Step 4 完了条件

次のどれかに当てはまる場合、テスト実行は未完了として扱い、Step 3 に戻って `SKILL.md` または出力例を修正する：

- 最終返信がファイルリンクや「作成しました」だけで、成果物の中身を読めない
- `SKILL.md` にはチャット表示ルールがあるのに、テスト時のチャット返信がその形式になっていない
- レポート型・議事録型・分析型の成果物なのに、本文がプレーンな説明だけで、表や見出しなどの読みやすさが不足している
- 不明点や `TBD` がファイル内にだけあり、チャット本文では確認すべき点が分からない

### Step 5: 初回 findings と図の整理

1. 初回成果物で分かったことを `findings.md` に整理する
2. `mcp_excalidraw` を使って、少なくとも 1 つ図を作る
3. 図の候補は次から選ぶ
   - trigger と発火条件
   - 入力から出力までの処理フロー
   - `SKILL.md` / `scripts/` / `references/` / `assets/` の責務分担
   - 改善案の比較図
4. `mcp_excalidraw` が使えない場合は、Figma / FigJam の図生成または Mermaid を代替として使う

### Step 6: 初回成果物完成後の構造理解

1. 初回成果物が成立したら `Understand-Anything` を使う
2. `SKILL.md`、関連ファイル、処理境界の構造を整理する
3. 次のフィードバック反映で壊しやすい箇所や依存関係を `findings.md` または `progress.md` に残す

### Step 7: フィードバックループ

```
動かしてみてどうですか？

- 出力を変えたいところ
- 処理を追加・変更したいところ
- 入力の形式を変えたいところ

があれば教えてください。
```

フィードバックがあれば Step 3 に戻る。

### Step 7.5: 第3層の記録

1. `sprint-metrics.md` のセクション 3 を追記する
   （意思決定に足る学びを得たか / 決まったこと / 決まらなかったこと）
2. 成立条件をすべて満たしたのに意思決定につながらなかった場合は、
   どの条件が顧客の関心とズレていたかを `findings.md` に残し、
   `acceptance-criteria.md` の「デモ後のふりかえり」欄にも 1 行書く
3. デモ、レビュー、利用中に見つかった失敗や違和感は、
   次回から必ず評価するケースとして `eval-cases.md` の「追加ケース候補」に戻す
4. 新しい失敗や学びがあれば、AI に `findings.md`、`eval-cases.md`、`eval-profile.md` を読ませて `promotion-candidates.md` を下書きさせる。AI は共通カタログを直接編集せず、人が承認した候補だけを `harness/evals/catalog/` へ反映する

## 注意事項

- `mcp_excalidraw` は初回 findings フェーズで使うが、skill 実装そのものの代替にはしない
- `Understand-Anything` は初回成果物完成直後から使い、trigger 設計前の手段選定には使わない
- 図は `findings.md` を置き換えるものではなく、文章の補助として残す
- ファイル生成型の skill でも、完了時の Codex チャット本文には、成果物へのリンクだけでなく、要点・代表出力・次の判断材料を読みやすく表示する。この確認は `SKILL.md` の記述確認ではなく、実際のテスト返信で行う
- レポート型の skill では、必要に応じて絵文字付きセクション、表、太字ラベルを使い、チャット画面だけで内容を把握できるようにする
- テスト実行後の最終回答では、作成ファイルへのリンクに加えて、skill が本来返すべきチャット表示をその場に再現する

## Skill の基本構造

```markdown
{skill-name}/
├── SKILL.md
├── agents/
│   └── openai.yaml           # 必要な場合
├── scripts/                  # 必要な場合
├── references/               # 必要な場合
└── assets/                   # 必要な場合
```

## SKILL.md の最低限の構造

```markdown
---
name: {skill-name}
description: {この skill をいつ使うか}
---

# {表示名}

## いつ使うか

- {典型的な依頼}
- {発火条件}

## 手順

1. {最初に確認すること}
2. {必要なら references や scripts を使う}
3. {生成または編集すること}

## 出力

- {期待する成果物}
- {Codex チャット本文に表示する要約または代表出力}

## 注意事項

- {やらないこと}
- {判断基準}
```
