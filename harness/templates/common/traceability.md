# traceability.md — 要件から評価までの対応表（Vモデル Lite）

> **使う条件**: 複数機能、外部連携、高影響操作、または「要件の評価漏れ」が心配な案件で使う。単機能の軽い PoC では省略してよい。
> **目的**: 中核要件が acceptance criteria と eval cases のどちらにも紐づかず、評価から漏れることを防ぐ。

## 中核要件

`project-requirements.md` の中核要件にだけ `REQ-01` 形式の ID を付ける。すべての説明文に ID を振る必要はない。

| 要件 ID | 要件 | 優先度 |
|---|---|---|
| REQ-01 | | Must / Should |

## 対応表

| 要件 ID | 設計・実装上の対応 | acceptance criterion | eval case | テストレベル | 結果 | メモ |
|---|---|---|---|---|---|---|
| REQ-01 | | C-__ | E-__ | 構成・単体 / 連携 / 業務シナリオ | | |

## 確認

- `Must` の要件に少なくとも 1 つの acceptance criterion と eval case がある
- 高影響操作は `業務シナリオ` のケースを含む
- 対応しない要件は、理由をメモに残す
