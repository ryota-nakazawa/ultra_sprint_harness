const STORAGE_KEY = "project-pulse-v1";
const $ = (selector) => document.querySelector(selector);
const today = new Date();
const iso = (date) => date.toISOString().slice(0, 10);
const daysFromNow = (offset) => iso(new Date(today.getFullYear(), today.getMonth(), today.getDate() + offset));

const seed = () => ({
  tasks: [
    { id: "t1", name: "要件定義書のレビュー", assignee: "佐藤", due: daysFromNow(-1), status: "進行中", progress: 65 },
    { id: "t2", name: "設計レビューを実施", assignee: "田中", due: daysFromNow(1), status: "未着手", progress: 0 },
    { id: "t3", name: "テスト計画を作成", assignee: "鈴木", due: daysFromNow(4), status: "進行中", progress: 40 },
    { id: "t4", name: "移行リハーサルの準備", assignee: "高橋", due: daysFromNow(8), status: "完了", progress: 100 }
  ],
  risks: [
    { id: "r1", title: "外部システム連携の遅延", level: "高", assignee: "佐藤", status: "対応中", detail: "接続先の開発完了日が未確定。週次で進捗を確認する。" },
    { id: "r2", title: "テスト期間の不足", level: "高", assignee: "鈴木", status: "未対応", detail: "結合テストの開始が遅れる可能性がある。計画を見直す。" },
    { id: "r3", title: "追加要望によるスコープ拡大", level: "中", assignee: "田中", status: "監視中", detail: "要望の優先順位を隔週レビューで確認する。" }
  ]
});
let state = load();
let modalType = "task";

function load() { try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || seed(); } catch { return seed(); } }
function save() { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }
function isOverdue(task) { return task.status !== "完了" && task.due < iso(today); }
function initials(name) { return (name || "?").slice(0, 2); }
function statusClass(status) { return ({ "完了": "done", "進行中": "progress", "未着手": "todo" }[status] || "todo"); }
function levelClass(level) { return ({ "高": "high", "中": "medium", "低": "low" }[level] || "low"); }

function renderSummary() {
  const overdue = state.tasks.filter(isOverdue).length;
  const highRisks = state.risks.filter(r => r.level === "高" && r.status !== "解決済み").length;
  const active = state.tasks.filter(t => t.status !== "完了").length;
  const average = state.tasks.length ? Math.round(state.tasks.reduce((sum, t) => sum + Number(t.progress), 0) / state.tasks.length) : 0;
  $("#summaryGrid").innerHTML = [
    ["総タスク", state.tasks.length, `進行中 ${active} 件`, ""], ["平均進捗", `${average}%`, "チーム全体の進捗", ""], ["期限超過", overdue, overdue ? "対応が必要です" : "超過はありません", overdue ? "risk" : ""], ["未解決の高リスク", highRisks, highRisks ? "優先確認が必要です" : "高リスクはありません", highRisks ? "risk" : ""]
  ].map(([label, value, note, cls]) => `<article class="summary ${cls}"><span class="label">${label}</span><strong class="value">${value}</strong><span class="note">${note}</span></article>`).join("");
}
function renderDashboard() {
  const priorities = [...state.tasks].filter(isOverdue).concat(state.tasks.filter(t => !isOverdue(t) && t.status === "進行中")).slice(0, 4);
  $("#priorityTasks").innerHTML = priorities.length ? priorities.map(t => `<article class="priority-row ${isOverdue(t) ? "overdue" : ""}"><span class="dot"></span><div class="row-main"><strong>${escapeHtml(t.name)}</strong><span>${escapeHtml(t.assignee)} · 期限 ${t.due}</span></div><span class="badge ${isOverdue(t) ? "overdue" : statusClass(t.status)}">${isOverdue(t) ? "期限超過" : t.status}</span></article>`).join("") : empty("優先確認が必要なタスクはありません。");
  const risks = state.risks.filter(r => r.level === "高" && r.status !== "解決済み");
  $("#priorityRisks").innerHTML = risks.length ? risks.map(r => `<article class="risk-item"><div class="risk-top"><strong>${escapeHtml(r.title)}</strong><span class="badge high">高リスク</span></div><p>${escapeHtml(r.detail)}</p><div class="risk-meta">担当 ${escapeHtml(r.assignee)} · ${escapeHtml(r.status)}</div></article>`).join("") : empty("未解決の高リスクはありません。");
  $("#dashboardTasks").innerHTML = taskTable(state.tasks.slice(0, 5), false);
}
function taskTable(tasks, editable = true) {
  return `<table class="data-table"><thead><tr><th>タスク</th><th>担当</th><th>期限</th><th>状態</th><th>進捗</th>${editable ? "<th></th>" : ""}</tr></thead><tbody>${tasks.map(t => `<tr><td><span class="task-name">${escapeHtml(t.name)}</span></td><td><span class="assignee">${initials(t.assignee)}</span> ${escapeHtml(t.assignee)}</td><td>${t.due}${isOverdue(t) ? " <span class=\"badge overdue\">超過</span>" : ""}</td><td><span class="badge ${statusClass(t.status)}">${t.status}</span></td><td><span class="progress-track"><span class="progress-bar" style="width:${t.progress}%"></span></span><span class="progress-number">${t.progress}%</span></td>${editable ? `<td><button class="edit-button" data-edit-task="${t.id}">編集</button></td>` : ""}</tr>`).join("")}</tbody></table>`;
}
function renderTasks() { $("#taskTable").innerHTML = state.tasks.length ? taskTable(state.tasks) : empty("タスクはまだありません。右上から追加できます。"); }
function renderRisks() {
  $("#riskTable").innerHTML = state.risks.length ? state.risks.map(r => `<article class="risk-card ${levelClass(r.level)}"><span class="risk-stripe"></span><div><div class="risk-top"><h3>${escapeHtml(r.title)}</h3><span class="badge ${levelClass(r.level)}">${r.level}リスク</span></div><p>${escapeHtml(r.detail)}</p><div class="risk-details"><span>担当: ${escapeHtml(r.assignee)}</span><span>対応: ${escapeHtml(r.status)}</span></div></div><button class="edit-button" data-edit-risk="${r.id}">編集</button></article>`).join("") : empty("リスクはまだありません。右上から追加できます。");
}
function empty(text) { return `<p class="empty-state">${text}</p>`; }
function escapeHtml(text) { return String(text).replace(/[&<>'"]/g, c => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", "'":"&#39;", '"':"&quot;" }[c])); }
function renderAll() { renderSummary(); renderDashboard(); renderTasks(); renderRisks(); bindEditButtons(); }

function openModal(type, item = null) {
  modalType = type; const isTask = type === "task";
  $("#modalEyebrow").textContent = isTask ? "TASK ENTRY" : "RISK ENTRY";
  $("#modalTitle").textContent = item ? (isTask ? "タスクを編集" : "リスクを編集") : (isTask ? "タスクを追加" : "リスクを追加");
  const data = item || {};
  $("#formFields").innerHTML = isTask ? `
    <input type="hidden" name="id" value="${data.id || ""}"><div class="field"><label for="entryName">タスク名 *</label><input id="entryName" name="name" value="${escapeHtml(data.name || "")}" placeholder="例：設計レビューを実施"></div><div class="field"><label for="entryAssignee">担当者</label><input id="entryAssignee" name="assignee" value="${escapeHtml(data.assignee || "")}" placeholder="例：佐藤"></div><div class="field"><label for="entryDue">期限</label><input id="entryDue" name="due" type="date" value="${data.due || daysFromNow(7)}"></div><div class="field"><label for="entryStatus">状態</label><select id="entryStatus" name="status">${["未着手","進行中","完了"].map(v => `<option ${data.status === v ? "selected" : ""}>${v}</option>`).join("")}</select></div><div class="field"><label for="entryProgress">進捗 (%)</label><input id="entryProgress" name="progress" type="number" min="0" max="100" value="${data.progress ?? 0}"></div>` : `
    <input type="hidden" name="id" value="${data.id || ""}"><div class="field"><label for="entryTitle">リスク内容 *</label><input id="entryTitle" name="title" value="${escapeHtml(data.title || "")}" placeholder="例：外部連携の遅延"></div><div class="field"><label for="entryLevel">重要度</label><select id="entryLevel" name="level">${["高","中","低"].map(v => `<option ${data.level === v ? "selected" : ""}>${v}</option>`).join("")}</select></div><div class="field"><label for="entryAssignee">担当者</label><input id="entryAssignee" name="assignee" value="${escapeHtml(data.assignee || "")}" placeholder="例：佐藤"></div><div class="field"><label for="entryRiskStatus">対応状況</label><select id="entryRiskStatus" name="status">${["未対応","対応中","監視中","解決済み"].map(v => `<option ${data.status === v ? "selected" : ""}>${v}</option>`).join("")}</select></div><div class="field"><label for="entryDetail">対応メモ</label><textarea id="entryDetail" name="detail" placeholder="影響や対応方針を記録">${escapeHtml(data.detail || "")}</textarea></div>`;
  $("#formError").textContent = ""; $("#entryModal").showModal();
}
function bindEditButtons() { document.querySelectorAll("[data-edit-task]").forEach(b => b.onclick = () => openModal("task", state.tasks.find(t => t.id === b.dataset.editTask))); document.querySelectorAll("[data-edit-risk]").forEach(b => b.onclick = () => openModal("risk", state.risks.find(r => r.id === b.dataset.editRisk))); }
function showToast(message) { const toast = $("#toast"); toast.textContent = message; toast.classList.add("show"); setTimeout(() => toast.classList.remove("show"), 2400); }
function setView(view) { document.querySelectorAll(".view").forEach(v => v.classList.toggle("active", v.id === `${view}View`)); document.querySelectorAll("[data-view-link]").forEach(b => b.classList.toggle("active", b.dataset.viewLink === view)); const names = { dashboard:["プロジェクトの状態","ダッシュボード"], tasks:["タスクを一覧・更新","タスク"], risks:["優先度と対応状況","リスク"] }; $("#viewEyebrow").textContent = names[view][0]; $("#viewTitle").textContent = names[view][1]; window.scrollTo({ top:0, behavior:"smooth" }); }

document.querySelectorAll("[data-view-link]").forEach(b => b.addEventListener("click", () => setView(b.dataset.viewLink)));
document.querySelectorAll("[data-open-modal]").forEach(b => b.addEventListener("click", () => openModal(b.dataset.openModal)));
$("#quickAdd").addEventListener("click", () => openModal($("#tasksView").classList.contains("active") ? "task" : $("#risksView").classList.contains("active") ? "risk" : "task"));
$("#entryForm").addEventListener("submit", event => { event.preventDefault(); const values = Object.fromEntries(new FormData(event.currentTarget)); const required = modalType === "task" ? values.name?.trim() : values.title?.trim(); if (!required) { $("#formError").textContent = modalType === "task" ? "タスク名を入力してください。" : "リスク内容を入力してください。"; return; } const collection = modalType === "task" ? state.tasks : state.risks; const item = modalType === "task" ? { id: values.id || `t${Date.now()}`, name: values.name.trim(), assignee: values.assignee.trim() || "未設定", due: values.due || daysFromNow(7), status: values.status, progress: Math.max(0, Math.min(100, Number(values.progress) || 0)) } : { id: values.id || `r${Date.now()}`, title: values.title.trim(), level: values.level, assignee: values.assignee.trim() || "未設定", status: values.status, detail: values.detail.trim() || "対応方針は未記入です。" }; const index = collection.findIndex(v => v.id === item.id); if (index >= 0) collection[index] = item; else collection.unshift(item); save(); renderAll(); $("#entryModal").close(); showToast(index >= 0 ? "更新を保存しました。" : "登録しました。"); });
$("#resetData").addEventListener("click", () => { state = seed(); save(); renderAll(); showToast("サンプルデータに戻しました。"); });
$("#projectFilter").addEventListener("change", () => showToast("PoCでは表示対象を切り替えた想定で維持します。"));
renderAll();
