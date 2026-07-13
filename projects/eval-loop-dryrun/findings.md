# findings.md — Eval Loop Dry Run

## 結論

小さなカウンター UI で、`Fix` を検出して実装へ戻し、1 回の自動修正後に `Pass` へ進むログ形式を確認した。

## 分かったこと

- 評価エージェントには、成果物、実行手順、`acceptance-criteria.md`、`eval-cases.md` だけを渡せば、欠けている UI / handler を `Fix` として判定できる。
- `Fix` は明確な未実装に限定すると、自動修正へ戻しやすい。
- `eval-loop-log.md` に iteration ごとの判定を残すと、なぜ一発合格でなかったかが追える。

## 次に検証すること

- Playwright などで、ファイル検査ではなく実際のクリック操作まで評価する。
- `Needs Review` が出るサンプルも別途作り、人間確認に止まる流れを確認する。
