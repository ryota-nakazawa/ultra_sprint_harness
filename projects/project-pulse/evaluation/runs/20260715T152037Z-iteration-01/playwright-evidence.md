# Playwright evidence

- Browser: Chrome via Playwright normal UI input; app URL `http://127.0.0.1:3000`.
- E-01 (partial): navigated to **タスク**, clicked **＋ タスクを追加**, then filled task name `評価用期限超過タスク`, owner `評価者`, due date `2026-07-10`, status `進行中`, and progress `50`; clicked **登録する**. The resulting task row was observed: `評価用期限超過タスク / 評価者 / 2026-07-10 / 超過 / 進行中 / 50%`.
- The task add dialog closed after save.
- Dashboard initial visual evidence showed distinct `期限超過` and `未解決の高リスク` panels, each with labelled items and navigation buttons.
- Console: not fully collected before the evaluation time limit.
- Screenshots: browser session captured screenshots during dashboard, task list, task modal and post-save state; no stable filesystem screenshot path was made available by the browser surface.
- E-02, E-03 and E-04 could not be completed in the available evaluator run time; no localStorage was directly inspected or modified.
