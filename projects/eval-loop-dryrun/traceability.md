# traceability.md — Eval Loop Dry Run

## 中核要件

| 要件 ID | 要件 | 優先度 |
|---|---|---|
| REQ-01 | カウンターの現在値を表示し、Increment で 1 増やせる | Must |
| REQ-02 | Reset で値を 0 に戻し、結果を画面に表示できる | Must |

## 対応表

| 要件 ID | 設計・実装上の対応 | acceptance criterion | eval case | テストレベル | 結果 | メモ |
|---|---|---|---|---|---|---|
| REQ-01 | `count` と `increment` のイベント処理 | C-01, C-02 | E-01 | 構成・単体 / 業務シナリオ | Pass | 基本操作 |
| REQ-02 | `reset` のイベント処理とステータス更新 | C-03, C-04 | E-02, E-03 | 連携 / 業務シナリオ | Pass | iteration 0 では Fix、iteration 1 で Pass |

## 確認

- すべての Must 要件に acceptance criterion と eval case がある。
- 高影響操作は含まれない。
