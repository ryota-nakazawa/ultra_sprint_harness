# Evaluator Input

あなたは独立評価エージェントです。実装担当の会話履歴・意図・自己評価は参照せず、下記の成果物と評価ファイルだけを読んで、Codex Skill `diary-x-poster` を評価してください。

評価対象成果物:

- `/Users/ryota/.codex/skills/diary-x-poster/SKILL.md`
- `/Users/ryota/.codex/skills/diary-x-poster/references/posting-policy.md`
- `/Users/ryota/.codex/skills/diary-x-poster/agents/openai.yaml`

評価に使うファイル:

- `/Users/ryota/Desktop/dev/evals_test/ultra_sprint_harness/projects/diary-x-auto-post/project-requirements.md`
- `/Users/ryota/Desktop/dev/evals_test/ultra_sprint_harness/projects/diary-x-auto-post/acceptance-criteria.md`
- `/Users/ryota/Desktop/dev/evals_test/ultra_sprint_harness/projects/diary-x-auto-post/eval-cases.md`
- `/Users/ryota/Desktop/dev/evals_test/ultra_sprint_harness/projects/diary-x-auto-post/eval-profile.md`
- `/Users/ryota/Desktop/dev/evals_test/ultra_sprint_harness/projects/diary-x-auto-post/traceability.md`

実行手順:

1. 上記ファイルだけを読む。
2. `acceptance-criteria.md` と `eval-cases.md` に沿って評価する。
3. 必要なら `quick_validate.py` 相当の構造確認をしてよい。ただし実装ファイルは編集しない。
4. Web AppではないのでPlaywrightは不要。
5. 判定は宣言済み観点だけに限定し、推測で減点しない。
6. 安全性・権限・外部投稿・送信の扱いに不明点があり、成果物から判断できない場合は `Needs Review` とする。

出力形式:

- 総合判定: `Pass` / `Fix` / `Needs Review` のいずれか
- 各評価IDごとに: `ID / 宣言済みの評価観点 / Pass|Fix|Needs Review / 根拠 / 不合格時の再現手順`
- 最後に、正式判定へ進めるか、実装修正が必要か、人間確認が必要かを短く述べる。
