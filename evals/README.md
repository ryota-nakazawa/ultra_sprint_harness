# evals

evals の対象は2つに分かれる:

1. **static（回帰テスト）**: 決定的な成果物（Web アプリ等）が成立条件を満たし続けているかの検査。
   k=1 で十分。CoP は出さない（決定的なので、ビルド CoP は sprint-metrics の累積トークン実測で測る）
2. **runtime（実行時 evals）**: AI 入り成果物の実行時性能。k 回実行して正答率 S と
   呼び出しトークンを測り、実行時 CoP（tok/pass）を出す。成果物が LLM を含まない間は
   精度 S のみ（tokens = n/a）

第3層（顧客が意思決定できたか）は対象外で、sprint-metrics §3 でのみ計測する。

## 改訂の背景

CoP は「確率的な生産」を測る。確率がどこにあるかで計測方法を変える。

| | ビルド時（作る） | 実行時（動く） |
|---|---|---|
| **決定的な成果物**（Web アプリ等） | 累積トークン実測 | 回帰テスト（k=1 で十分） |
| **AI 入り成果物**（GPTs・LLM 分類機能等） | 累積トークン実測 | **evals**: k 回 × S × 呼び出しトークン |

## 動かし方

通常のスモーク:

```bash
python evals/run_eval.py --runs 1
```

意味のあるハーネス改訂後の確認:

```bash
python evals/run_eval.py --runs 4
```

## 読み方

- `static`: pass / fail / cannot_judge のみ。tok/pass は表示しない
- `runtime S`: そのケースが pass した割合
- `runtime avg_call_tokens`: AI 呼び出しの入力＋出力トークン。LLM を呼ばない場合は `n/a`
- `runtime tok/pass`: `avg_call_tokens / S`。LLM を呼ばない場合は `n/a`
- `S=0` のケースは実行不可能として別掲し、平均 tok/pass には混ぜない

## 運用ルール

- フル実行はハーネスの意味ある改訂時のみ。普段は k=1 のスモーク
- 実案件で出た手戻り・失敗（sprint-metrics の手戻り主因）を新ケースとして追加していく
- eval の S₁₂ は「作る力」のみを測る。第3層（顧客価値）は対象外
- トークン CoP を単独の KPI にしない。フォールバック率・手戻り主因・第3層とセットで見る
- ルールベース成果物の runtime eval は精度 S のみを測る。将来 LLM 呼び出しに差し替えたら、同じケースで実行時 CoP を測る

## 人間判定のまま残す項目

`projects/contact-triage-dryrun/acceptance-criteria.md` の C-07 は「15 分のデモで投資判断の論点を説明できる画面」という顧客価値寄りの条件を含むため、evals では機械判定しない。

`judge_type=subagent` のケースを追加する場合は、`harness/templates/common/judge-instructions.md` を使い、成果物・条件文・判定指示だけを独立ジャッジに渡す。作成経緯や会話履歴は渡さない。
