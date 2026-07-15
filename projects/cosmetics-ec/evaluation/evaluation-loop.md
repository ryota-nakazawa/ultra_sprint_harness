# evaluation-loop.md — 評価ループ記録

## 現在のループ

```mermaid
flowchart TD
  requirements["要件とトレーサビリティ"] --> implementation["実装"]
  implementation --> selfCheck["自己確認（参考）"]
  selfCheck --> evaluator["独立評価サブエージェント"]
  evaluator --> uiEval["Playwright ユーザー操作評価"]
  uiEval --> decision{"判定"}
  decision -->|"Pass"| demo["デモ・利用確認"]
  decision -->|"Fix"| implementation
  decision -->|"Needs Review"| human["人間確認"]
  demo --> learning["findings と昇格候補"]
  human --> learning
```

## 実行履歴

| 時刻 | iteration / run ID | 実行者 | 操作 | 結果 | 証跡 / 次の動き |
|---|---|---|---|---|---|
| 2026-07-14 | iteration-00 | 実装担当 | Playwright による自己確認 | 参考確認: Pass | 正式独立評価は未実施 |

## 停止状態

| 項目 | 記録 |
|---|---|
| 現在の判定 | 参考確認: Pass / 正式評価未実施 |
| 停止理由 | ユーザー依頼への初回構築を優先。独立評価サブエージェントは未実施。 |
| 人に確認したいこと | 実ブランド、商品画像、決済、法務表記を次スプリントで扱うか。 |
