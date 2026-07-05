# evals

Ultra Sprint Harness の第1・2層（作る力）を軽量に測るための evals。
第3層（顧客が意思決定できたか）は対象外で、`sprint-metrics.md` セクション 3 でのみ計測する。

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

- `S`: そのケースが pass した割合
- `avg_tokens`: 1 run あたりの平均トークン下限推定
- `tok/pass`: `avg_tokens / S`
- `S=0` のケースは実行不可能として別掲し、平均 tok/pass には混ぜない

## 運用ルール

- フル実行はハーネスの意味ある改訂時のみ。普段は k=1 のスモーク
- 実案件で出た手戻り・失敗（sprint-metrics の手戻り主因）を新ケースとして追加していく
- eval の S₁₂ は「作る力」のみを測る。第3層（顧客価値）は対象外
- トークン CoP を単独の KPI にしない。フォールバック率・手戻り主因・第3層とセットで見る

## 人間判定のまま残す項目

`projects/contact-triage-dryrun/acceptance-criteria.md` の C-07 は「15 分のデモで投資判断の論点を説明できる画面」という顧客価値寄りの条件を含むため、evals では機械判定しない。

`judge_type=subagent` のケースを追加する場合は、`harness/templates/common/judge-instructions.md` を使い、成果物・条件文・判定指示だけを独立ジャッジに渡す。作成経緯や会話履歴は渡さない。
