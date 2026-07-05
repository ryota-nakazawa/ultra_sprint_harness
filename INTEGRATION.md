# INTEGRATION.md — 計測テンプレートのハーネス組み込み手順

超速スプリントの効果測定（3層判定・CoP 計測）を Ultra Sprint Harness に組み込む手順。
**作業は「フォルダを1つ置く」＋「既存ファイル4〜6箇所に追記」だけ。** 所要 15 分程度。

---

## 1. 置くもの（このフォルダをそのままコピー）

| 追加するもの | 置き場所 | 役割 |
|---|---|---|
| `harness/templates/common/` フォルダごと | リポジトリ直下の `harness/templates/` 配下 | ルート共通テンプレート置き場（既存の webapp / codex-skills / gpts / harness-design と並ぶ） |
| └ `acceptance-criteria.md` | （テンプレ原本。実物は案件開始時に `projects/{プロジェクト名}/` に複製） | PoC 成立条件と第1・2層の合否判定 |
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
│           ├── sprint-metrics.md
│           └── monthly-review.md
├── projects/
│   └── {プロジェクト名}/
│       ├── interview-summary.md / project-requirements.md / findings.md ...
│       ├── acceptance-criteria.md       ← ★案件開始時に複製
│       └── sprint-metrics.md            ← ★案件開始時に複製
└── metrics/                             ← ★追加（月次集計の置き場）
    └── YYYY-MM.md
```

---

## 2. 既存ファイルへの追記（コピペ用）

### 2-1. `harness/flows/discovery.md` — 末尾（完了条件の箇所）に追記

```markdown
## 成立条件の判定可能化（discovery の完了条件）

「成立条件の確認」の最後に、次を行ってから routing に進む。

1. `harness/templates/common/acceptance-criteria.md` を複製して
   `projects/{プロジェクト名}/acceptance-criteria.md` を作る
2. project-requirements.md の「PoC として何ができれば十分か」を、
   **Yes / No で判定できる文**に変換して第2層の表に書く（3〜7 項目）
3. 「このプロトで顧客のどんな意思決定を引き出したいか」を仮説欄に 1〜2 文で書く

Yes / No の文に変換できない成立条件が残っている間は、曖昧さが残っているサイン。
そのまま実装に進まず、短くユーザーに確認する。
あわせて `harness/templates/common/sprint-metrics.md` も複製し、基本情報だけ埋めておく。
```

### 2-2. `harness/flows/webapp.md` `codex-skills.md` `gpts.md` `harness-design.md` — 各フローの「動作確認（テスト実行）」の直後に追記（4ファイル共通）

```markdown
## 合否判定と記録（動作確認の直後に行う）

1. `projects/{プロジェクト名}/acceptance-criteria.md` の第1層・第2層を判定し、
   結果と判定日を記入する（判定方法が LLM の項目は、成果物と条件文を渡して項目別に判定させてよい）
2. 判定サマリー（合格数・一発合格の Yes/No）を埋める
3. `sprint-metrics.md` のセクション 1〜2（試行回数、一発合格、フォールバック、手戻り主因）を記入する

不合格項目が残る場合はここで再試行に戻る。**成果物に合わせて条件を緩めない**
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
```

### 2-4. `AGENTS.md` と `CLAUDE.md` — 末尾に追記（エージェントへの常時ルール）

```markdown
## 計測ルール

このハーネスでは、スプリントの効果測定のため次を必ず守る。

- discovery の完了条件に `acceptance-criteria.md` の作成を含める
  （PoC 成立条件はすべて Yes / No で判定できる文にする）
- 成果物の動作確認後、第1・2層を判定し `sprint-metrics.md` に記録する
- 生成を伴う成果物では、token manifest を作成し `tools/count_tokens.py` で累積トークンを計算して `sprint-metrics.md` に記録する
- 成果物に合わせて成立条件を後から緩めない。変更する場合は変更履歴に理由を残す
- 金額や正確な工数は書かない。第1段階では回数、Yes / No、累積トークンを残す
- 記録の記入がユーザーの負担にならないよう、埋められる項目は AI が下書きし、
  ユーザーには確認だけを求める
```

### 2-5. `README.md` — 「`projects/` に何を置くか」の共通ファイル一覧に 2 行追加

```markdown
- `acceptance-criteria.md` PoC 成立条件（Yes/No 判定可能な文）と第1・2層の合否を残す
- `sprint-metrics.md` 試行回数・一発合格・顧客デモの結果（第3層）を残す台帳
- `metrics/{project-name}-token-manifest.tsv` 累積トークン算出対象の input / output 一覧
- `metrics/{project-name}-token-usage.md` `tools/count_tokens.py` が生成する token 使用量レポート
```

### 2-6. `README.md` — 「ディレクトリ構成」の templates 配下に `common/`、直下に `metrics/` を追記

（上のディレクトリ構成図のとおり）

---

## 3. 運用の流れ（誰が・いつ・何を書くか）

| タイミング | ファイル | 記入者 |
|---|---|---|
| discovery の最後 | acceptance-criteria.md（仮説＋成立条件） | AI が下書き → 人が確認・確定 |
| 動作確認の直後 | acceptance-criteria.md（判定結果）、sprint-metrics.md §1-2 | AI が下書き → 人が確認 |
| 顧客デモの後 | sprint-metrics.md §3、findings.md | 人（1〜2 行） |
| 月次 | `metrics/YYYY-MM.md`（monthly-review を複製して集計） | 人（AI に集計させてよい） |

## 4. 最初の注意

- **金額欄は当面すべて空欄でよい**（第1段階は回数と Yes/No だけ集める）
- 件数が 10 に満たないうちは、月次の「率」は参考値。個別の findings を読む方が価値がある
- 1〜2 案件回して、記入が 5 分を超える項目があれば削る（この手順書自体も更新対象）
