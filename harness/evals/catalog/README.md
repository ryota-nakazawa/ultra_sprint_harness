# 自社 Evals カタログ

このフォルダは、複数案件で再利用できる評価知識だけを置く部品集である。全案件に強制適用するチェックリストではない。

## 使い方

1. discovery で案件要件を読み、必要な項目だけ選ぶ。
2. 選択した ID、版、採用理由を `projects/{project}/eval-profile.md` に記録する。
3. 選択内容を案件固有の `acceptance-criteria.md` と `eval-cases.md` に具体化する。
4. 案件内で出た失敗はまず案件内に残す。再利用価値がある場合だけ AI が `promotion-candidates.md` に候補を作る。
5. 人が承認した候補だけをこのカタログへ反映する。

過去案件の評価基準は `eval-profile.md` と案件内ファイルを正とする。カタログの後日の更新で過去案件を遡って書き換えない。

## ファイル

- `dimensions.md`: 自社で使う評価観点
- `case-patterns.md`: 再利用できる代表・境界・失敗ケースの型
- `domain-rules.md`: 業務、権限、監査など、適用条件付きのルール
