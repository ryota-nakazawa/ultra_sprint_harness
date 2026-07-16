# findings.md — 失敗と学びの記録

> **目的**: 失敗を責めるためではなく、次の eval case と必要なら共通カタログ候補へ変換する。1件につき短く、再現できる事実を残す。

## Findings

| Finding ID | 日付 | 分類 | 起きたこと / 影響 | 再現条件 | 根本原因の仮説 | 次の動き | eval case | 昇格候補 |
|---|---|---|---|---|---|---|---|---|
| F-001 | YYYY-MM-DD | Implementation / Requirement / Evaluation Spec / Missing Eval Case / Tool / UX | | | | Fix / Needs Review / 記録のみ | E-__ / 新規 | CAND-__ / なし |

## 分類の目安

- **Implementation**: 要件は明確で、成果物の実装・設定・導線に原因がある。
- **Requirement**: 要件・成立条件・前提の解釈が不足または矛盾している。
- **Evaluation Spec**: acceptance criterion、rubric、期待結果が曖昧または不適切である。
- **Missing Eval Case**: 既存ケースで拾えなかった再現可能な失敗である。
- **Tool**: 外部ツール、環境、権限、APIなど成果物の外に主因がある。
- **UX**: 動くが利用者が誤解・迷い・不安を感じる。

## Learning Loop メモ

- 案件内の次回評価へ戻すもの:
- `promotion-candidates.md` に下書きするもの:
- 人の判断が必要なもの:
