# 評価ゲート共通ルール

## 目的

このゲートは、すべてのルートで次の順序を強制する。

1. 評価項目を作る
2. 実装する
3. 実装担当とは別コンテキストのサブエージェントで評価する
4. 証跡検査が通ってからだけ正式判定を記録する

自己確認はデバッグ用の参考確認であり、正式評価ではない。

**必須文言:** 正式な `Pass / Fix / Needs Review` を記録するには、`fresh_context` で起動した評価サブエージェントの `evaluation/runs/{run_id}/receipt.json`、`evaluator-input.md`、`evaluator-result.md` が必須である。
この証跡がない判定は正式評価ではない。

## Gate A: 実装前ゲート

実装を始める前に、必ず次を満たす。

- `project-requirements.md` がある
- `eval-profile.md` がある
- `acceptance-criteria.md` があり、Yes / No で判定できる `C-` 条件がある
- `eval-cases.md` があり、代表・境界・失敗ケースが最低 1 件ずつある
- 各 eval case に `構成・単体`、`連携`、`業務シナリオ` のいずれかのテストレベルがある
- `traceability.md` があり、すべての Must `REQ` が少なくとも 1 つの `C-` と `E-` に紐づく
- `evaluation-loop.md` があり、Mermaid 図を含む

実装直前に次を実行する。

```bash
python3 tools/check_preimplementation_readiness.py --project-dir projects/{project_name}
```

失敗した場合は、実装に進まない。足りない評価項目またはトレーサビリティを先に直す。

## Gate B: 正式評価ゲート

成果物の自己確認が終わったら、正式評価の前に `evaluation/evaluation-status.md` を作る。

正式評価は独立 LLM 評価を必須とする。自己確認は正式評価にできない。
評価サブエージェントは `fresh_context` で起動し、実装担当の会話履歴、意図、自己評価、言い訳を渡さない。
人間レビューは追加確認として記録してよいが、通常の AI 実装ループにおける独立 LLM 評価の代替にはしない。

評価サブエージェントへ渡してよいもの:

- 成果物
- 成果物の実行手順
- `project-requirements.md`
- `acceptance-criteria.md`
- `eval-cases.md`
- `eval-profile.md`
- `traceability.md`

評価サブエージェントへ渡してはいけないもの:

- 実装中の会話ログ
- 実装者の判断理由
- 未完成箇所の補足説明
- 「ここは合格にしてほしい」などの期待判定

評価サブエージェントは、各項目について次だけを返す。

```text
ID / 宣言済みの評価観点 / テストレベル / Pass|Fix|Needs Review / 根拠 / 不合格時の再現手順
```

評価観点は `acceptance-criteria.md` と `eval-cases.md` に宣言されたものだけを見る。未定義の観点を推測して減点しない。
安全性、権限、送信、削除、外部公開などの高影響操作に不明点があれば `Needs Review` とする。

## Gate C: 証跡検査ゲート

LLM 評価ごとに `projects/{project_name}/evaluation/runs/{run_id}/` を作り、次を保存する。

- `receipt.json`: サブエージェント起動で返った agent ID、`fresh_context`、許可した入力、開始・完了時刻、最終判定に加え、評価した Git commit SHA、要件・eval cases・成果物の SHA-256、評価モデル、temperature、prompt / rubric version
- `evaluator-input.md`: 実際に評価サブエージェントへ渡した依頼文
- `evaluator-result.md`: 評価サブエージェントの返答全文
- `playwright-evidence.md`: Web App の場合のみ必須

正式判定を記録する前に、必ず次を実行する。

```bash
python3 tools/check_evaluation_evidence.py --project-dir projects/{project_name} --run-id {run_id}
```

失敗した場合は、`evaluation/acceptance-criteria.md`、`evaluation/eval-cases.md`、`evaluation/sprint-metrics.md` に正式な `Pass / Fix / Needs Review` を記録しない。

リポジトリ全体で、正式判定がサブエージェント証跡を持つか確認するには次を実行する。

```bash
python3 tools/check_formal_evaluation_gate.py
```

この検査は Git hook と GitHub Actions でも実行する。正式判定だけを書いて評価サブエージェント証跡がない状態は失敗扱いにする。
新規の receipt schema v2 は再現情報が欠ける場合も失敗する。Git管理外だけは `evaluated_commit_sha: "unavailable"` と記録する。既存の schema 未記載 receipt は履歴として読めるため、直ちに失敗にはしない。

## Gate D: ループ制御

- `Pass`: 完了またはデモへ進む
- `Fix`: 明確に直せる不合格だけ実装へ戻す
- `Needs Review`: 自動ループを止め、人間確認へ回す

自動修正は最大 2 回まで。3 回目の実装・評価には入らない。

次の場合は必ず停止する。

- `Needs Review` が 1 件以上出た
- 同じ ID が 2 回連続で `Fix` になった
- 自動修正が 2 回に達した
- 修正にスコープ変更または評価基準変更が必要になった

停止後に自動で次の評価runを作らない。`check_formal_evaluation_gate.py` は、`Needs Review` の後、または 2 回目の `Fix` の後に継続したrunがあれば失敗する。

成果物に合わせて acceptance criteria や eval cases を緩めない。変更が必要な場合は変更履歴に理由を残し、人間確認を挟む。
