# Playwright Evidence

## QA Inventory

| 要件 / ケース ID | 操作する UI | 期待する見える結果 | 実施結果 |
|---|---|---|---|
| REQ-01 / C-01 / E-04 | 初期タイムラインと導線 | 投稿、話題、プロフィールが見える | Needs Review（初見ユーザー確認が必要） |
| REQ-02 / C-02 / E-01 | 投稿欄と投稿ボタン | 新規投稿が先頭に表示される | Pass |
| REQ-03 / C-03 / E-01, E-02 | いいね、返信 | 状態が切り替わり返信欄が開閉する | Fix（返信欄の hidden が無効） |
| REQ-04 / C-04 / E-03 | 空・上限超過の入力 | 投稿されない | Pass |

## 実行環境

| 項目 | 記録 |
|---|---|
| URL | `http://127.0.0.1:4174` |
| Playwright / Chromium | local Playwright Chromium |
| Desktop viewport | `1600x900` |
| Mobile viewport | `390x844` |

## 操作結果

| 操作 | 結果 | コンソールエラー | スクリーンショット / 根拠 |
|---|---|---|---|
| 投稿、いいね、空投稿、返信、モバイル投稿を通常のクリック・入力で操作 | E-02 以外 Pass | なし | `desktop-initial.png`、`desktop-post-interaction.png`、`mobile-initial.png`、`mobile-post-interaction.png` を in-memory で確認 |

## 視覚確認

- 初期表示、投稿後、モバイル表示を確認した。
- モバイルに横方向のあふれはなかった。
- 返信入力が `hidden` 属性にもかかわらず初期表示され、開閉操作でも見え続ける不具合を検出した。
