# 評価ディレクトリの標準レイアウト

評価に関するMarkdownと実行証跡は、実装ファイルと分けて案件ごとの `evaluation/` 配下に置く。

```text
projects/{project}/
  project-requirements.md
  interview-summary.md
  index.html / app.js / ...
  findings.md
  evaluation/
    acceptance-criteria.md
    eval-profile.md
    eval-cases.md
    traceability.md
    evaluation-loop.md
    evaluation-status.md
    sprint-metrics.md
    promotion-candidates.md
    runs/{run-id}/
```

`tools/check_preimplementation_readiness.py`、`tools/check_evaluation_evidence.py`、`tools/check_formal_evaluation_gate.py`、`tools/create_evaluation_run.py` はこのレイアウトを前提にする。呼び出し時は従来どおり案件ディレクトリを `--project-dir` に渡す。

旧レイアウト（プロジェクト直下の評価Markdownや `evaluation-runs/`）は新規案件では使用しない。既存案件は評価ファイルを `evaluation/` に移してから検証する。
