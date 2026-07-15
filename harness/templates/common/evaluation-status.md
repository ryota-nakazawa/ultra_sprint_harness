# evaluation-status.md — 評価ゲート

> **書くタイミング**: 実装後の自己確認を始める前。正式な `Pass / Fix / Needs Review` を acceptance criteria、eval cases、sprint metrics に記録する前に更新する。
> **目的**: 実装担当の自己確認と、独立した評価を混同しない。
> **必須**: 正式な `Pass / Fix / Needs Review` は、`fresh_context` の評価サブエージェントによる独立 LLM 評価runがある場合だけ記録できる。

## 現在の状態

| 項目 | 記入 |
|---|---|
| 実装 | ☐ 未完了 ／ ☐ 完了 |
| 実装担当による自己確認 | ☐ 未実施 ／ ☐ 実施済み（参考確認） |
| 正式評価の方式 | ☐ 独立 LLM 評価（必須） ／ ☐ 未実施 |
| 独立 LLM 評価 | ☐ 未開始 ／ ☐ 実行中 ／ ☐ 完了 ／ ☐ 該当なし |
| Playwright ユーザー操作評価（Web App） | ☐ 未開始 ／ ☐ 実行中 ／ ☐ 完了 ／ ☐ 該当なし |
| トレーサビリティ | ☐ 未作成 ／ ☐ 作成済み ／ ☐ 不備あり |
| 正式判定の記録可否 | ☐ 不可 ／ ☐ 可 |

## ゲート規則

- 実装担当の自己確認は、技術的な参考確認であり正式な `Pass / Fix / Needs Review` ではない。
- すべての案件で `traceability.md` を作り、中核要件の `REQ`、acceptance criterion の `C`、eval case の `E` を対応させる。対応しない要件は理由を残す。
- `evaluation-runs/{run-id}/` に `receipt.json`、`evaluator-input.md`、`evaluator-result.md` がそろい、証跡検査が成功するまで正式判定の記録可否は `不可` とする。Web App ではさらに Playwright の操作証跡が必要である。
- 人間レビューは追加確認として記録してよいが、通常の AI 実装ループでは独立 LLM 評価の代替にしない。
- 証跡がない場合は、acceptance criteria と eval cases の結果を `未判定` とし、自己確認の内容は下の表にだけ記録する。

## 自己確認（参考確認）

| 日付 | 実施者 | 確認内容 | 結果 | 制約 |
|---|---|---|---|---|
| YYYY-MM-DD | 実装担当 | | 参考確認済み / 未確認 | 独立評価ではない |

## 正式評価の記録

| 日付 | 方式 | 評価者 / run ID | 証跡検査 | 結果の反映先 |
|---|---|---|---|---|
| | 独立 LLM 評価 | | Pass / Fail / N/A | acceptance-criteria.md / eval-cases.md / sprint-metrics.md |
