const seedTickets = [
  ["2026-07-04 08:12", "北日本部品", "ライン停止、制御ユニットが起動しない", "昨日から生産ラインが停止しています。至急確認をお願いします。"],
  ["2026-07-04 08:18", "東都精密", "請求書の宛名変更", "6月分請求書の宛名を本社名義に変更できますか。"],
  ["2026-07-04 08:26", "三河製作所", "管理画面のログイン方法", "担当者が変わったため、初回ログインの手順を教えてください。"],
  ["2026-07-04 08:31", "西日本化工", "異音と焦げ臭い匂い", "装置から異音があり焦げ臭い匂いもします。安全確認を急ぎたいです。"],
  ["2026-07-04 08:39", "関東物流", "納品書の再発行", "先月納品分の納品書をPDFで再発行してください。"],
  ["2026-07-04 08:44", "青葉機械", "エラー E-42 が頻発", "再起動しても E-42 が出て検査工程が止まります。"],
  ["2026-07-04 08:52", "北陸パーツ", "操作マニュアルの場所", "新しい担当者向けに操作マニュアルのURLを共有してください。"],
  ["2026-07-04 09:01", "瀬戸内工業", "月額費用の確認", "契約更新前に現在の月額費用とオプション料金を確認したいです。"],
  ["2026-07-04 09:07", "甲信電装", "製品が突然停止", "朝から3台中2台が突然停止しました。出荷判定に影響しています。"],
  ["2026-07-04 09:12", "南都食品", "帳票の出し方", "検査結果の月次帳票を出す操作を教えてください。"],
  ["2026-07-04 09:19", "京浜金属", "返金処理について", "重複支払い分の返金予定日を確認したいです。"],
  ["2026-07-04 09:25", "筑波計測", "センサー値が異常", "温度センサーが実測と20度以上ずれており、不良判定が出ています。"],
  ["2026-07-04 09:33", "遠州モーター", "ユーザー追加", "新入社員2名のユーザー追加方法を確認したいです。"],
  ["2026-07-04 09:41", "大阪産機", "至急: 出荷前検査が止まった", "検査画面が固まり、本日出荷分の確認ができません。"],
  ["2026-07-04 09:48", "新潟電子", "見積書の再送", "以前いただいた保守契約の見積書を再送してください。"],
  ["2026-07-04 09:54", "神戸樹脂", "通知メールの設定", "アラート通知メールの宛先を追加する手順を知りたいです。"],
  ["2026-07-04 10:03", "千葉製鋼", "画面表示が崩れる", "一覧画面の列が重なって表示され、一部のボタンが押せません。"],
  ["2026-07-04 10:11", "山陽精工", "請求明細の内訳", "今月の請求明細で追加費用が発生した理由を教えてください。"],
  ["2026-07-04 10:16", "栃木電子", "アラーム解除不可", "安全アラームが解除できず、作業を再開できません。"],
  ["2026-07-04 10:23", "四国化成", "データ出力形式", "CSV 出力時に列順を変えられるか確認したいです。"],
  ["2026-07-04 10:31", "名古屋部材", "電源が入らない", "納入直後の端末1台で電源が入りません。交換可否を知りたいです。"],
  ["2026-07-04 10:37", "道央機工", "契約プラン変更", "来月から利用人数が増えるためプラン変更の条件を教えてください。"],
  ["2026-07-04 10:45", "広島計装", "初期設定の確認", "設置後の初期設定チェックリストが欲しいです。"],
  ["2026-07-04 10:52", "長野製作", "至急対応希望: 全端末で通信不可", "全端末でサーバー通信ができず、現場作業が止まっています。"],
  ["2026-07-04 11:00", "福岡機材", "領収書について", "クレジット決済分の領収書発行方法を教えてください。"],
  ["2026-07-04 11:08", "熊本電機", "部品交換後もエラー", "交換後も同じエラーが出ます。原因切り分けをお願いします。"],
  ["2026-07-04 11:15", "岡山精密", "権限設定", "閲覧だけ可能なアカウントを作る方法を教えてください。"],
  ["2026-07-04 11:22", "群馬加工", "請求先部署の変更", "7月分から請求先部署を購買部に変更してください。"],
  ["2026-07-04 11:30", "仙台部品", "緊急: 異常停止が連続", "午前中だけで異常停止が5回発生しています。生産に影響しています。"],
  ["2026-07-04 11:39", "鹿児島食品", "レポート保存場所", "作成した日報レポートがどこに保存されるか知りたいです。"],
  ["2026-07-04 11:47", "横浜機器", "型番違いの可能性", "納品された部品の型番が発注内容と異なるようです。確認してください。"],
  ["2026-07-04 11:55", "岐阜工材", "請求書が届かない", "今月分の請求書メールが届いていません。再送をお願いします。"],
  ["2026-07-04 12:04", "奈良測器", "操作ボタンの意味", "設定画面の自動補正ボタンの意味を教えてください。"],
  ["2026-07-04 12:13", "富山鋳造", "重大: 検査結果が保存されない", "検査結果が保存されず、品質記録が残せない状態です。"],
  ["2026-07-04 12:21", "宮城物流", "契約更新の流れ", "保守契約更新の手続きと期限を確認したいです。"],
  ["2026-07-04 12:28", "静岡電材", "ファームウェア更新手順", "最新版への更新手順と注意点を教えてください。"],
  ["2026-07-04 12:36", "愛媛産業", "破損して届いた", "交換部品が破損した状態で届きました。再送をお願いします。"],
  ["2026-07-04 12:44", "茨城機械", "請求金額が想定と違う", "見積より請求金額が高い理由を確認したいです。"],
  ["2026-07-04 12:51", "京都電子", "画面の並び替え", "一覧を担当者順に並び替える方法を知りたいです。"],
  ["2026-07-04 13:00", "大分製作所", "至急: 安全装置が反応しない", "安全装置が反応しない可能性があり、現場確認を止めています。"]
];

let tickets = seedTickets.map(toTicket);
let selectedId = tickets[0].id;

const el = {
  totalCount: document.querySelector("#totalCount"),
  highCount: document.querySelector("#highCount"),
  openCount: document.querySelector("#openCount"),
  editedCount: document.querySelector("#editedCount"),
  searchInput: document.querySelector("#searchInput"),
  urgencyFilter: document.querySelector("#urgencyFilter"),
  categoryFilter: document.querySelector("#categoryFilter"),
  categoryBars: document.querySelector("#categoryBars"),
  ticketBody: document.querySelector("#ticketBody"),
  listSummary: document.querySelector("#listSummary"),
  detailTitle: document.querySelector("#detailTitle"),
  detailBody: document.querySelector("#detailBody"),
  urgencyEdit: document.querySelector("#urgencyEdit"),
  categoryEdit: document.querySelector("#categoryEdit"),
  saveEditButton: document.querySelector("#saveEditButton"),
  classifyButton: document.querySelector("#classifyButton"),
  resetButton: document.querySelector("#resetButton"),
  csvInput: document.querySelector("#csvInput"),
  reasonText: document.querySelector("#reasonText")
};

function toTicket(row, index) {
  const [receivedAt, customer, subject, body] = row;
  const classified = classify(`${subject} ${body}`);
  return {
    id: `T-${String(index + 1).padStart(3, "0")}`,
    receivedAt,
    customer,
    subject,
    body,
    urgency: classified.urgency,
    category: classified.category,
    reason: classified.reason,
    edited: false,
    status: "要確認"
  };
}

function classify(text) {
  const normalized = text.toLowerCase();
  const highWords = ["至急", "緊急", "重大", "停止", "止ま", "安全", "焦げ", "通信不可", "保存されない", "反応しない"];
  const midWords = ["エラー", "異常", "破損", "型番", "表示", "起動しない", "電源"];
  const billingWords = ["請求", "返金", "領収", "契約", "費用", "見積", "支払い", "プラン"];
  const howtoWords = ["方法", "手順", "マニュアル", "設定", "ログイン", "操作", "出力", "保存場所", "権限"];
  const defectWords = ["停止", "エラー", "異常", "破損", "起動", "電源", "センサー", "反応しない", "保存されない", "型番"];

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

function getFilteredTickets() {
  const keyword = el.searchInput.value.trim().toLowerCase();
  return tickets.filter((ticket) => {
    const matchesKeyword = !keyword || `${ticket.customer} ${ticket.subject} ${ticket.body}`.toLowerCase().includes(keyword);
    const matchesUrgency = el.urgencyFilter.value === "all" || ticket.urgency === el.urgencyFilter.value;
    const matchesCategory = el.categoryFilter.value === "all" || ticket.category === el.categoryFilter.value;
    return matchesKeyword && matchesUrgency && matchesCategory;
  });
}

function render() {
  renderMetrics();
  renderTable();
  renderDetail();
}

function renderMetrics() {
  el.totalCount.textContent = tickets.length;
  el.highCount.textContent = tickets.filter((ticket) => ticket.urgency === "高").length;
  el.openCount.textContent = tickets.filter((ticket) => ticket.status === "要確認").length;
  el.editedCount.textContent = tickets.filter((ticket) => ticket.edited).length;

  const categories = ["製品不具合", "使い方", "請求", "その他"];
  const max = Math.max(...categories.map((category) => tickets.filter((ticket) => ticket.category === category).length), 1);
  el.categoryBars.innerHTML = categories.map((category) => {
    const count = tickets.filter((ticket) => ticket.category === category).length;
    return `
      <div class="barRow">
        <span>${category}</span>
        <div class="barTrack"><div class="barFill" style="width:${(count / max) * 100}%"></div></div>
        <strong>${count}</strong>
      </div>
    `;
  }).join("");
}

function renderTable() {
  const filtered = getFilteredTickets();
  el.listSummary.textContent = `${filtered.length} 件を表示中`;
  el.ticketBody.innerHTML = filtered.map((ticket) => `
    <tr class="${ticket.id === selectedId ? "selected" : ""}" data-id="${ticket.id}">
      <td>${ticket.receivedAt.slice(5)}</td>
      <td>${ticket.customer}</td>
      <td class="subject">${ticket.subject}</td>
      <td><span class="pill ${urgencyClass(ticket.urgency)}">${ticket.urgency}</span></td>
      <td><span class="pill category">${ticket.category}</span></td>
      <td><span class="pill ${ticket.status === "確認済み" ? "status-done" : "status-open"}">${ticket.status}</span></td>
    </tr>
  `).join("");
}

function renderDetail() {
  const ticket = tickets.find((item) => item.id === selectedId);
  if (!ticket) return;
  el.detailTitle.textContent = `${ticket.customer} / ${ticket.subject}`;
  el.detailBody.textContent = ticket.body;
  el.urgencyEdit.value = ticket.urgency;
  el.categoryEdit.value = ticket.category;
  el.reasonText.textContent = ticket.reason;
}

function urgencyClass(urgency) {
  if (urgency === "高") return "u-high";
  if (urgency === "中") return "u-mid";
  return "u-low";
}

function parseCsv(text) {
  const rows = text.trim().split(/\r?\n/).map((line) => line.split(",").map((cell) => cell.trim().replace(/^"|"$/g, "")));
  const dataRows = rows[0]?.some((cell) => ["receivedAt", "customer", "subject", "body", "受付", "顧客", "件名", "本文"].includes(cell))
    ? rows.slice(1)
    : rows;
  return dataRows.filter((row) => row.length >= 4).map(toTicket);
}

el.ticketBody.addEventListener("click", (event) => {
  const row = event.target.closest("tr");
  if (!row) return;
  selectedId = row.dataset.id;
  const ticket = tickets.find((item) => item.id === selectedId);
  if (ticket) ticket.status = "確認済み";
  render();
});

[el.searchInput, el.urgencyFilter, el.categoryFilter].forEach((input) => {
  input.addEventListener("input", render);
});

el.saveEditButton.addEventListener("click", () => {
  const ticket = tickets.find((item) => item.id === selectedId);
  if (!ticket) return;
  ticket.urgency = el.urgencyEdit.value;
  ticket.category = el.categoryEdit.value;
  ticket.edited = true;
  ticket.status = "確認済み";
  ticket.reason = "人が分類を修正しました。以後の精度改善では、この修正理由を教師データ候補として扱います。";
  render();
});

el.classifyButton.addEventListener("click", () => {
  tickets = tickets.map((ticket) => {
    const result = classify(`${ticket.subject} ${ticket.body}`);
    return { ...ticket, ...result, edited: false, status: "要確認" };
  });
  selectedId = tickets[0]?.id;
  render();
});

el.resetButton.addEventListener("click", () => {
  tickets = seedTickets.map(toTicket);
  selectedId = tickets[0].id;
  el.searchInput.value = "";
  el.urgencyFilter.value = "all";
  el.categoryFilter.value = "all";
  render();
});

el.csvInput.addEventListener("change", async (event) => {
  const file = event.target.files?.[0];
  if (!file) return;
  const text = await file.text();
  const parsed = parseCsv(text);
  if (parsed.length > 0) {
    tickets = parsed;
    selectedId = tickets[0].id;
    render();
  }
  event.target.value = "";
});

render();
