# Codex Skills フロー

## 概要

Codex 用の skill を作るフロー。
ユーザーが繰り返す作業や専門手順を、再利用可能な `SKILL.md` と付随リソースに整理する。

このフローは、共通ディスカバリーで「最小解決手段は Codex Skills」と決まった後に使う。
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
【追加ファイル】scripts / references / assets が必要か
```

この整理にユーザー合意を取ってから Step 3 に進む。

### Step 3: 実装

1. `skill-creator` skill を使って、skill の骨組みを設計する
2. スキル名をハイフン区切りで決める
3. `projects/{プロジェクト名}/{スキル名}/` に skill フォルダを作る
4. `SKILL.md` に以下を含める：
   - YAML frontmatter の `name` と `description`
   - いつ使う skill か
   - どう進めるかの手順
   - 追加ファイルを読む条件
   - 出力の期待値
5. 必要な場合だけ `scripts/`, `references/`, `assets/`, `agents/openai.yaml` を追加する

合意済みのトリガーと境界の中では、実装はまとめて進めてよい。

### Step 4: テスト実行

1. 実際の依頼文に近いプロンプトで試す
2. skill が発火すべき条件と、本文の指示が噛み合っているか確認する
3. 冗長な説明がないか確認する
4. 必要なら `SKILL.md` と付随ファイルを調整する

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

## 注意事項

- `mcp_excalidraw` は初回 findings フェーズで使うが、skill 実装そのものの代替にはしない
- `Understand-Anything` は初回成果物完成直後から使い、trigger 設計前の手段選定には使わない
- 図は `findings.md` を置き換えるものではなく、文章の補助として残す

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

## 注意事項

- {やらないこと}
- {判断基準}
```
