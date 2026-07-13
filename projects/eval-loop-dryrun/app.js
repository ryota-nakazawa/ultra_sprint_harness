const countEl = document.getElementById("count");
const incrementButton = document.getElementById("increment");
const resetButton = document.getElementById("reset");
const statusEl = document.getElementById("status");

let count = 0;

function render(message) {
  countEl.textContent = String(count);
  statusEl.textContent = message;
}

incrementButton.addEventListener("click", () => {
  count += 1;
  render(`Incremented to ${count}`);
});

resetButton.addEventListener("click", () => {
  count = 0;
  render("Reset to 0");
});
