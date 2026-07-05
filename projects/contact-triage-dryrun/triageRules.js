(function initTriageRules(root) {
  function classify(text) {
    const normalized = text.toLowerCase();
    const highWords = ["至急", "緊急", "重大", "停止", "止ま", "安全", "焦げ", "通信不可", "保存されない", "反応しない"];
    const midWords = ["エラー", "異常", "破損", "型番", "表示", "起動しない", "電源"];
    const billingWords = ["請求", "返金", "領収", "契約", "費用", "見積", "支払い", "プラン"];
    const howtoWords = ["方法", "手順", "マニュアル", "設定", "ログイン", "操作", "出力", "保存場所", "権限"];
    const defectWords = ["停止", "エラー", "異常", "破損", "起動", "電源", "センサー", "反応しない", "反応せず", "保存されない", "型番"];

    const urgency = highWords.some((word) => normalized.includes(word))
      ? "高"
      : midWords.some((word) => normalized.includes(word))
        ? "中"
        : "低";

    let category = "その他";
    if (billingWords.some((word) => normalized.includes(word))) category = "請求";
    else if (defectWords.some((word) => normalized.includes(word))) category = "製品不具合";
    else if (howtoWords.some((word) => normalized.includes(word))) category = "使い方";

    const reason = `キーワード判定: 緊急度=${urgency}、カテゴリ=${category}。本文に含まれる緊急語、障害語、請求語、操作語を優先して分類。`;
    return { urgency, category, reason };
  }

  const api = { classify };

  if (typeof module !== "undefined" && module.exports) {
    module.exports = api;
  }

  root.TriageRules = api;
})(typeof window !== "undefined" ? window : globalThis);
