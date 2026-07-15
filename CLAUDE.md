# 超速スプリント — Codexプロトタイピングハーネス

## このプロジェクトについて

非エンジニアが Codex を使って素早くプロトタイプを作るためのハーネス（フロー制御）システム。
要件の聞き取りから成果物のたたき台生成までを、迷いにくい定型フローに落とし込む。

すべてのプロトタイプ作成は、最初に軽量な共通ディスカバリーを通してから個別フローに入る。

## プロトタイプ種別

| 種別 | 成果物 | 実行環境 |
|------|--------|----------|
| Web App | ローカルで動くWebアプリ（Next.js等） | Codex |
| Codex Skills | Codex 用の skill フォルダ（`SKILL.md` + 必要な付随リソース） | Codex |
| ハーネス設計 | ハーネス定義ファイル一式（メタフロー） | Codex |
| GPTs | Custom GPT 用の `instructions.md` を中心にした prompt パッケージ | Codex |

## 設計原則

1. **非エンジニアが迷わない** — 専門用語を避け、必要な選択肢だけを見せる
2. **最小限の入力で最大の成果物** — まず動くたたき台を優先し、後から広げる
3. **軽量ディスカバリー** — まず目的整理、解決手段の選定、成立条件の確認だけを行う
4. **File-first planning** — 複雑な実装では `project-requirements.md`, `task-plan.md`, `progress.md`, 必要なら `findings.md` に重要事項を残す
5. **Prompt-first** — 特に GPTs は、まず system prompt を整えてから拡張する
6. **段階的な確認** — 要件→設計→実装→確認の順で進める
7. **やり直しが安い** — git で各ステップをコミットし、いつでも戻れる
8. **軽量 Evals** — 成立条件と代表・境界・失敗ケースを使い、失敗を次の評価ケースへ戻す

## ディレクトリ構造

```
超速スプリント/
├── CLAUDE.md                  # このファイル
├── harness/                   # ハーネス定義
│   ├── router.md              # 種別判定・ルーティングロジック
│   ├── flows/                 # 各種別のフロー定義
│   │   ├── discovery.md
│   │   ├── webapp.md
│   │   ├── codex-skills.md
│   │   ├── harness-design.md
│   │   └── gpts.md
│   └── templates/             # 各種別のテンプレート
│       ├── webapp/
│       ├── codex-skills/
│       ├── harness-design/
│       ├── gpts/
│       └── common/             # 共通の計測テンプレート
├── projects/                  # 生成されたプロトタイプの出力先
└── metrics/                   # 月次集計の置き場
```

## 計測ルール

このハーネスでは、スプリントの効果測定のため次を必ず守る。

- discovery の完了条件に `acceptance-criteria.md` の作成を含める
  （PoC 成立条件はすべて Yes / No で判定できる文にする）
- discovery の完了条件に `eval-cases.md` の作成を含める
  （代表ケース、境界ケース、失敗ケースを最低 1 件ずつ作る）
- 成果物の動作確認後、第1・2層と eval-cases を判定し `sprint-metrics.md` に記録する
- LLM 判定を使う場合は、実装担当とは別コンテキストの評価エージェントで判定する
- 評価エージェントには成果物、実行手順、`project-requirements.md`、`acceptance-criteria.md`、`eval-cases.md`、`eval-profile.md`、必須の `traceability.md` だけを渡し、実装中の会話ログや背景説明は渡さない
- 評価エージェントは `ID / 宣言済みの評価観点 / Pass / Fix / Needs Review / 根拠 / 不合格時の再現手順` を返す。未定義の観点を推測して減点せず、安全性・権限・送信・削除などの高影響操作に不明点があれば `Needs Review` とする
- LLM 評価ごとに `projects/{プロジェクト名}/evaluation-runs/{run-id}/` を作り、オーケストレーターが返した agent ID と `fresh_context` を `receipt.json`、実際の依頼を `evaluator-input.md`、返答全文を `evaluator-result.md` に保存する
- 評価前に `evaluation-status.md` を作る。実装担当の自己確認は参考確認としてのみ扱い、独立 LLM 評価では `tools/check_evaluation_evidence.py` が成功するまで正式な `Pass / Fix / Needs Review` を記録しない。人間評価の場合は評価者を記録してから正式判定を記録する
- discovery では `harness/evals/catalog/` から案件に必要な項目だけを選び、acceptance criteria と eval cases を作る前に `eval-profile.md` へ ID と採用理由を記録する
- 各 eval case には `構成・単体`、`連携`、`業務シナリオ` のテストレベルを付ける。すべての案件で `traceability.md` を作り、中核要件の `REQ` を少なくとも 1 つの `C` と `E` に対応させる
- Web App の独立評価では、評価サブエージェントが Playwright で通常の UI 操作を行い、コンソール・視覚確認の証跡を `playwright-evidence.md` に保存する。Playwright が動かない場合は `Pass` にせず `Needs Review` とする
- 案件の学びが出た後は、AI に案件成果物から `promotion-candidates.md` を下書きさせる。AI は共通カタログを直接更新せず、人が承認した候補だけを昇格する
- `Fix` は自動修正して再評価する。ただし自動修正は最大 2 回まで。3 回目の実装・評価には入らない
- `Needs Review` が出た、同じ ID が 2 回連続で `Fix` になった、上限に達した、スコープ変更や評価基準変更が必要になった場合は自動ループを止める
- デモ、レビュー、利用中に見つかった失敗は `findings.md` に残し、次回評価するケースとして `eval-cases.md` に戻す
- 成果物に合わせて成立条件を後から緩めない。変更する場合は変更履歴に理由を残す
- 記録は回数と Yes / No と学びのみでよい。利用量の単価換算や正確な工数は書かない
- 記録の記入がユーザーの負担にならないよう、埋められる項目は AI が下書きし、
  ユーザーには確認だけを求める

## Evals の扱い

- このハーネスでの evals は、本番投入可否を判定する重い評価基盤ではなく、超速スプリントの学習ループを再現可能にする軽量評価として扱う
- `acceptance-criteria.md` を eval spec、`eval-cases.md` を軽量 dataset、`findings.md` を production flywheel の入口として使う
- v1 では自動 grader や eval runner は作らない。人間または LLM が読んで判定できるケースを先に整える
- LLM 判定では、実装時のコンテキストを持たない評価エージェントに `Pass / Fix / Needs Review`、根拠、不合格時の再現手順だけを返させる
