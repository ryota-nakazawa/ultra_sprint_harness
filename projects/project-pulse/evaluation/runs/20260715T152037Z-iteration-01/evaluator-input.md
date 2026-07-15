# 独立評価依頼

以下のWebアプリを、実装会話や実装者の判断を参照せずに独立評価してください。

## 成果物と実行手順

- 成果物: `/Users/ryota/Desktop/dev/evals_test/ultra_sprint_harness/projects/project-pulse/`
- 実行中のURL: `http://127.0.0.1:3000`
- Playwrightで通常のUI操作のみを用いて評価してください。直接localStorageを編集してはいけません。

## 評価に使用してよい資料

- `project-requirements.md`
- `acceptance-criteria.md`
- `eval-cases.md`
- `eval-profile.md`
- `traceability.md`

## 必須作業

1. PlaywrightでE-01からE-04を操作して確認する。
2. コンソールエラーと主要画面の視覚確認を行う。
3. 操作内容、確認結果、コンソール確認、スクリーンショットのパスを `playwright-evidence.md` に保存する。
4. C-01〜C-05およびE-01〜E-04について、`ID / 宣言済みの評価観点 / テストレベル（Eのみ） / Pass|Fix|Needs Review / 根拠 / 不合格時の再現手順` を返す。定義されていない観点は評価しない。
5. 返答全文を `evaluator-result.md` にも保存する。
