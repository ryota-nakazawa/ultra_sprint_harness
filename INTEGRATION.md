# INTEGRATION.md — 計測テンプレートのハーネス組み込み手順

超速スプリントの効果測定（3層判定・軽量 Evals）を Ultra Sprint Harness に組み込む手順。
**作業は「フォルダを1つ置く」＋「既存ファイル4〜6箇所に追記」だけ。** 所要 15 分程度。

---

## 1. 置くもの（このフォルダをそのままコピー）

| 追加するもの | 置き場所 | 役割 |
|---|---|---|
| `harness/templates/common/` フォルダごと | リポジトリ直下の `harness/templates/` 配下 | ルート共通テンプレート置き場（既存の webapp / codex-skills / gpts / harness-design と並ぶ） |
| └ `acceptance-criteria.md` | （テンプレ原本。実物は案件開始時に `projects/{プロジェクト名}/` に複製） | PoC 成立条件と第1・2層の合否判定 |
| └ `eval-cases.md` | （テンプレ原本。実物は案件開始時に `projects/{プロジェクト名}/` に複製） | 代表・境界・失敗ケースを残す軽量 Evals ケース集 |
| └ `evaluation-run/` | （テンプレ原本。実物は LLM 評価のたびに `projects/{プロジェクト名}/evaluation-runs/` に作成） | 独立評価サブエージェントの起動証跡、入力、出力 |
| └ `sprint-metrics.md` | （テンプレ原本。実物は `projects/{プロジェクト名}/` に複製） | スプリント記録台帳 |
| └ `monthly-review.md` | （テンプレ原本。実物は月次で `metrics/YYYY-MM.md` として複製） | 月次集計と 2×2 診断 |

月次集計の実物を置くために、リポジトリ直下に空フォルダ `metrics/` を作っておく。

組み込み後のディレクトリ構成:

```
超速スプリント/
├── README.md / CLAUDE.md / AGENTS.md
├── harness/
│   ├── router.md
│   ├── flows/
│   └── templates/
│       ├── webapp/ ├── codex-skills/ ├── gpts/ ├── harness-design/
│       └── common/                      ← ★追加
│           ├── acceptance-criteria.md
│           ├── eval-cases.md
│           ├── sprint-metrics.md
│           └── monthly-review.md
├── projects/
│   └── {プロジェクト名}/
│       ├── interview-summary.md / project-requirements.md / findings.md ...
│       ├── acceptance-criteria.md       ← ★案件開始時に複製
│       ├── eval-cases.md                ← ★案件開始時に複製
│       ├── evaluation-runs/             ← ★LLM 評価ごとに作成
│       │   └── {run-id}/
│       │       ├── receipt.json
│       │       ├── evaluator-input.md
│       │       └── evaluator-result.md
│       └── sprint-metrics.md            ← ★案件開始時に複製
└── metrics/                             ← ★追加（月次集計の置き場）
    └── YYYY-MM.md
```

---

## 2. 既存ファイルへの追記（コピペ用）

### 2-1. `harness/flows/discovery.md` — 末尾（完了条件の箇所）に追記

```markdown
## 成立条件と eval ケースの判定可能化（discovery の完了条件）

「成立条件の確認」の最後に、次を行ってから routing に進む。

1. `harness/templates/common/acceptance-criteria.md` を複製して
   `projects/{プロジェクト名}/acceptance-criteria.md` を作る
2. project-requirements.md の「PoC として何ができれば十分か」を、
   **Yes / No で判定できる文**に変換して第2層の表に書く（3〜7 項目）
   各条件には `業務成功 / 誤実行 / 安全性 / 再現性 / 運用負荷` の評価観点を 1 つ付ける
3. 「このプロトで顧客のどんな意思決定を引き出したいか」を仮説欄に 1〜2 文で書く
4. `harness/templates/common/eval-cases.md` を複製して
   `projects/{プロジェクト名}/eval-cases.md` を作る
5. 代表ケース、境界ケース、失敗ケースを最低 1 件ずつ、合計 3〜7 件で書く

Yes / No の文に変換できない成立条件が残っている間は、曖昧さが残っているサイン。
そのまま実装に進まず、短くユーザーに確認する。
あわせて `harness/templates/common/sprint-metrics.md` も複製し、基本情報だけ埋めておく。
eval-cases.md は、重い自動評価基盤ではなく軽量な Evals ケース集として扱う。
```

### 2-2. `harness/flows/webapp.md` `codex-skills.md` `gpts.md` `harness-design.md` — 各フローの「動作確認（テスト実行）」の直後に追記（4ファイル共通）

```markdown
## 合否判定と記録（動作確認の直後に行う）

1. `projects/{プロジェクト名}/acceptance-criteria.md` の第1層・第2層を判定し、
   結果と判定日を記入する
2. `projects/{プロジェクト名}/eval-cases.md` のケースを判定し、
   代表ケース、境界ケース、失敗ケースのどこが弱いかを記録する
3. 判定サマリー（合格数・一発合格の Yes/No）を埋める
4. `sprint-metrics.md` のセクション 1〜2（試行回数、一発合格、フォールバック、手戻り主因、eval-cases の結果）を記入する

LLM で判定する項目は、実装担当とは別コンテキストの評価エージェントで行う。
評価エージェントには、成果物、実行手順、`project-requirements.md`、`acceptance-criteria.md`、`eval-cases.md`、`eval-profile.md`、必要時の `traceability.md` だけを渡し、実装中の会話ログや背景説明は渡さない。
評価エージェントは、各項目について `ID / 宣言済みの評価観点 / Pass / Fix / Needs Review / 根拠 / 不合格時の再現手順` を返す。
`acceptance-criteria.md` と `eval-cases.md` で宣言した評価観点だけを判定対象にし、未定義の品質を推測して減点しない。
安全性・権限・送信・削除などの高影響操作に不明点があれば、`Fix` ではなく `Needs Review` とする。

評価サブエージェントを起動したオーケストレーターは、評価ごとに
`projects/{プロジェクト名}/evaluation-runs/{run-id}/` を作る。起動 API が返した agent ID と
`fresh_context` は `receipt.json`、実際の評価依頼は `evaluator-input.md`、返答全文は
`evaluator-result.md` に保存する。評価ログだけでなく、独立サブエージェントの起動と入力制限を確認するための証跡として扱う。

評価結果に `Fix` がある場合は、実装へ戻して修正し、再評価する。自動修正は最大 2 回まで。3 回目の実装・評価には入らない。
`Needs Review` が 1 件でも出た場合、同じ ID が 2 回連続で `Fix` になった場合、または修正にスコープ変更や評価基準変更が必要な場合は、自動ループを止める。
止めた理由と要チェック項目は `eval-cases.md` と `sprint-metrics.md` に記録する。**成果物に合わせて条件を緩めない**
（条件を変える場合は acceptance-criteria.md の変更履歴に理由を残す）。
```

### 2-3. 同じ4ファイルの「顧客フィードバック反映」の箇所に追記（4ファイル共通）

```markdown
## 第3層の記録（顧客デモの後に行う）

1. `sprint-metrics.md` のセクション 3 を追記する
   （意思決定に足る学びを得たか / 決まったこと / 決まらなかったこと）
2. 成立条件をすべて満たしたのに意思決定につながらなかった場合は、
   どの条件が顧客の関心とズレていたかを `findings.md` に残し、
   `acceptance-criteria.md` の「デモ後のふりかえり」欄にも 1 行書く
3. デモ、レビュー、利用中に見つかった失敗や違和感は、
   次回から必ず評価するケースとして `eval-cases.md` の「追加ケース候補」に戻す
```

### 2-4. `AGENTS.md` と `CLAUDE.md` — 末尾に追記（エージェントへの常時ルール）

```markdown
## 計測ルール

このハーネスでは、スプリントの効果測定のため次を必ず守る。

- discovery の完了条件に `acceptance-criteria.md` の作成を含める
  （PoC 成立条件はすべて Yes / No で判定できる文にする）
- discovery の完了条件に `eval-cases.md` の作成を含める
  （代表ケース、境界ケース、失敗ケースを最低 1 件ずつ作る）
- 成果物の動作確認後、第1・2層と eval-cases を判定し `sprint-metrics.md` に記録する
- LLM 判定を使う場合は、実装担当とは別コンテキストの評価エージェントで判定する
- 評価エージェントには成果物、実行手順、`project-requirements.md`、`acceptance-criteria.md`、`eval-cases.md`、`eval-profile.md`、必要時の `traceability.md` だけを渡し、実装中の会話ログや背景説明は渡さない
- 評価エージェントは `ID / 宣言済みの評価観点 / Pass / Fix / Needs Review / 根拠 / 不合格時の再現手順` を返す。未定義の観点を推測して減点せず、高影響操作に不明点があれば `Needs Review` とする
- `Fix` は自動修正して再評価する。ただし自動修正は最大 2 回まで。3 回目の実装・評価には入らない
- `Needs Review` が出た、同じ ID が 2 回連続で `Fix` になった、上限に達した、スコープ変更や評価基準変更が必要になった場合は自動ループを止める
- デモ、レビュー、利用中に見つかった失敗は `findings.md` に残し、次回評価するケースとして `eval-cases.md` に戻す
- 成果物に合わせて成立条件を後から緩めない。変更する場合は変更履歴に理由を残す
- 記録は回数と Yes / No と学びのみでよい。利用量の単価換算や正確な工数は書かない
- 記録の記入がユーザーの負担にならないよう、埋められる項目は AI が下書きし、
  ユーザーには確認だけを求める
```

### 2-5. `README.md` — 「`projects/` に何を置くか」の共通ファイル一覧に 2 行追加

```markdown
- `acceptance-criteria.md` PoC 成立条件（Yes/No 判定可能な文）、評価観点、第1・2層の合否を残す
- `eval-cases.md` 代表ケース、境界ケース、失敗ケースを残す軽量 Evals ケース集
- `sprint-metrics.md` 試行回数・一発合格・eval-cases の結果・顧客デモの結果（第3層）を残す台帳
```

### 2-6. `README.md` — 「ディレクトリ構成」の templates 配下に `common/`、直下に `metrics/` を追記

（上のディレクトリ構成図のとおり）

---

## 3. 運用の流れ（誰が・いつ・何を書くか）

| タイミング | ファイル | 記入者 |
|---|---|---|
| discovery の最後 | acceptance-criteria.md（仮説＋成立条件）、eval-cases.md（初期ケース） | AI が下書き → 人が確認・確定 |
| 動作確認の直後 | acceptance-criteria.md（判定結果）、eval-cases.md（ケース判定）、sprint-metrics.md §1-2 | AI が下書き → 人が確認 |
| LLM 評価の直後 | `evaluation-runs/{run-id}/`（receipt、評価依頼、返答全文） | オーケストレーターが記録 |
| 顧客デモの後 | sprint-metrics.md §3、findings.md、eval-cases.md（追加ケース候補） | 人（1〜2 行） |
| 月次 | `metrics/YYYY-MM.md`（monthly-review を複製して集計） | 人（AI に集計させてよい） |

## 4. 最初の注意

- 件数が 10 に満たないうちは、月次の「率」は参考値。個別の findings を読む方が価値がある
- 1〜2 案件回して、記入が 5 分を超える項目があれば削る（この手順書自体も更新対象）

## 5. 自社 Evals カタログ

`harness/evals/catalog/` を、自社で再利用する評価観点、ケースパターン、ドメインルールの選択元として置く。
discovery では案件に必要な項目だけを選び、`projects/{プロジェクト名}/eval-profile.md` に選択 ID と採用理由を残す。

`test-viewpoints.md` は Vモデル Lite のテスト観点カタログである。各 eval case には `構成・単体 / 連携 / 業務シナリオ` のテストレベルを付ける。複数機能、外部連携、高影響操作、または評価漏れが心配な案件だけは `traceability.md` を作り、中核要件（`REQ-01`）から acceptance criteria と eval cases への対応を記録する。

案件内の失敗や学びは、まず `eval-cases.md` と `findings.md` に残す。AI はそれらと `eval-profile.md` を読んで `promotion-candidates.md` を下書きしてよいが、共通カタログは直接編集しない。人が承認した候補だけをカタログへ昇格する。
