const products = [
  {
    id: "lotion",
    name: "ハイドラバランス ローション",
    category: "skincare",
    type: "bottle",
    volume: "150mL",
    description: "みずみずしい感触で角層までうるおいを届ける化粧水。",
    price: 5500,
    badge: "ベストセラー",
  },
  {
    id: "cream",
    name: "ディープグロウ クリーム",
    category: "skincare",
    type: "jar",
    volume: "50g",
    description: "乾燥を防ぎ、なめらかなつや感を保つ保湿クリーム。",
    price: 7700,
    badge: "保湿",
  },
  {
    id: "uv",
    name: "ブライトニング UV エッセンス",
    category: "base",
    type: "tube",
    volume: "SPF50+ PA++++ / 30g",
    description: "白浮きしにくく、日中の肌を軽く守るUV下地。",
    price: 3300,
    badge: "UV",
  },
  {
    id: "serum",
    name: "リペア セラム",
    category: "skincare",
    type: "bottle",
    volume: "30mL",
    description: "洗顔後の肌になじむ、軽い使い心地の美容液。",
    price: 8800,
    badge: "集中ケア",
  },
  {
    id: "cushion",
    name: "グロウ クッション ファンデーション",
    category: "base",
    type: "cushion",
    volume: "SPF40 PA+++ / 全3色",
    description: "薄膜で自然なつやを仕込むベースメイク。",
    price: 6600,
    badge: "メイク",
  },
  {
    id: "gift",
    name: "スターター ギフト セット",
    category: "gift",
    type: "jar",
    volume: "ローション / クリーム / UV",
    description: "朝の基本ケアを試せるギフト向けセット。",
    price: 13200,
    badge: "ギフト",
  },
];

const state = {
  filter: "all",
  cart: [],
  customer: null,
};

const grid = document.querySelector("#productGrid");
const cartDrawer = document.querySelector("#cartDrawer");
const cartCount = document.querySelector("#cartCount");
const cartItems = document.querySelector("#cartItems");
const cartEmpty = document.querySelector("#cartEmpty");
const subtotalEl = document.querySelector("#subtotal");
const shippingEl = document.querySelector("#shipping");
const totalEl = document.querySelector("#total");
const shippingHint = document.querySelector("#shippingHint");
const checkoutForm = document.querySelector("#checkoutForm");
const formError = document.querySelector("#formError");
const reviewDialog = document.querySelector("#reviewDialog");
const completeDialog = document.querySelector("#completeDialog");
const reviewContent = document.querySelector("#reviewContent");
const completeMessage = document.querySelector("#completeMessage");

const yen = new Intl.NumberFormat("ja-JP", {
  style: "currency",
  currency: "JPY",
  maximumFractionDigits: 0,
});

function formatYen(value) {
  return yen.format(value);
}

function getCartProduct(item) {
  return products.find((product) => product.id === item.id);
}

function getSubtotal() {
  return state.cart.reduce((sum, item) => {
    const product = getCartProduct(item);
    return sum + product.price * item.qty;
  }, 0);
}

function getShipping(subtotal) {
  if (subtotal === 0 || subtotal >= 3500) return 0;
  return 550;
}

function renderProducts() {
  const visibleProducts = products.filter((product) => state.filter === "all" || product.category === state.filter);
  grid.innerHTML = visibleProducts
    .map(
      (product) => `
        <article class="product-card">
          <div class="product-media">
            <div class="product-visual ${product.type}"><span>${product.name.split(" ")[0]}</span></div>
          </div>
          <div class="product-info">
            <span class="badge">${product.badge}</span>
            <h3>${product.name}</h3>
            <p>${product.volume}</p>
            <p>${product.description}</p>
            <div class="product-bottom">
              <span class="price">${formatYen(product.price)}</span>
              <button class="add-button" type="button" data-add="${product.id}">追加</button>
            </div>
          </div>
        </article>
      `,
    )
    .join("");
}

function renderCart() {
  const subtotal = getSubtotal();
  const shipping = getShipping(subtotal);
  const total = subtotal + shipping;
  const quantity = state.cart.reduce((sum, item) => sum + item.qty, 0);

  cartCount.textContent = quantity;
  subtotalEl.textContent = formatYen(subtotal);
  shippingEl.textContent = shipping === 0 ? "無料" : formatYen(shipping);
  totalEl.textContent = formatYen(total);
  shippingHint.textContent =
    subtotal >= 3500 ? "送料無料の条件を満たしています" : `あと${formatYen(3500 - subtotal)}で送料無料`;

  cartEmpty.classList.toggle("show", state.cart.length === 0);
  cartItems.innerHTML = state.cart
    .map((item) => {
      const product = getCartProduct(item);
      return `
        <article class="cart-item">
          <div class="cart-thumb">${product.badge}</div>
          <div>
            <div class="cart-row">
              <div>
                <h3>${product.name}</h3>
                <span>${formatYen(product.price)} / ${product.volume}</span>
              </div>
              <strong>${formatYen(product.price * item.qty)}</strong>
            </div>
            <div class="cart-row">
              <div class="qty" aria-label="${product.name}の数量">
                <button type="button" data-dec="${product.id}" aria-label="数量を減らす">−</button>
                <span>${item.qty}</span>
                <button type="button" data-inc="${product.id}" aria-label="数量を増やす">＋</button>
              </div>
              <button class="remove" type="button" data-remove="${product.id}">削除</button>
            </div>
          </div>
        </article>
      `;
    })
    .join("");
}

function addToCart(productId) {
  const existing = state.cart.find((item) => item.id === productId);
  if (existing) {
    existing.qty += 1;
  } else {
    state.cart.push({ id: productId, qty: 1 });
  }
  renderCart();
  openCart();
}

function changeQuantity(productId, delta) {
  const item = state.cart.find((cartItem) => cartItem.id === productId);
  if (!item) return;
  item.qty += delta;
  if (item.qty <= 0) {
    state.cart = state.cart.filter((cartItem) => cartItem.id !== productId);
  }
  renderCart();
}

function removeItem(productId) {
  state.cart = state.cart.filter((item) => item.id !== productId);
  renderCart();
}

function openCart() {
  cartDrawer.classList.add("open");
  cartDrawer.setAttribute("aria-hidden", "false");
}

function closeCart() {
  cartDrawer.classList.remove("open");
  cartDrawer.setAttribute("aria-hidden", "true");
}

function validateCheckout(formData) {
  if (state.cart.length === 0) return "商品をカートに追加してください。";
  if (!formData.get("name").trim()) return "お名前を入力してください。";
  if (!formData.get("email").trim() || !formData.get("email").includes("@")) return "有効なメールアドレスを入力してください。";
  if (!formData.get("address").trim()) return "配送先住所を入力してください。";
  if (!formData.get("payment")) return "支払方法を選択してください。";
  return "";
}

function buildReview() {
  const subtotal = getSubtotal();
  const shipping = getShipping(subtotal);
  const total = subtotal + shipping;
  const lines = state.cart
    .map((item) => {
      const product = getCartProduct(item);
      return `<div class="review-line"><span>${product.name} × ${item.qty}</span><strong>${formatYen(product.price * item.qty)}</strong></div>`;
    })
    .join("");

  reviewContent.innerHTML = `
    ${lines}
    <div class="review-line"><span>配送先</span><strong>${state.customer.name} / ${state.customer.address}</strong></div>
    <div class="review-line"><span>支払方法</span><strong>${state.customer.payment}</strong></div>
    <div class="review-line"><span>送料</span><strong>${shipping === 0 ? "無料" : formatYen(shipping)}</strong></div>
    <div class="review-total"><span>合計（税込）</span><strong>${formatYen(total)}</strong></div>
    <p class="demo-note">これはデモ注文です。実際の請求・配送・在庫確保は行われません。</p>
  `;
}

document.addEventListener("click", (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;

  const addId = target.dataset.add;
  const incId = target.dataset.inc;
  const decId = target.dataset.dec;
  const removeId = target.dataset.remove;

  if (addId) addToCart(addId);
  if (incId) changeQuantity(incId, 1);
  if (decId) changeQuantity(decId, -1);
  if (removeId) removeItem(removeId);
});

document.querySelectorAll(".filter").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".filter").forEach((filterButton) => filterButton.classList.remove("active"));
    button.classList.add("active");
    state.filter = button.dataset.filter;
    renderProducts();
  });
});

document.querySelector("#openCart").addEventListener("click", openCart);
document.querySelector("#closeCart").addEventListener("click", closeCart);
document.querySelector("#backToProducts").addEventListener("click", closeCart);
document.querySelector("#quickAdd").addEventListener("click", () => {
  addToCart("lotion");
  addToCart("cream");
  addToCart("uv");
});

checkoutForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const formData = new FormData(checkoutForm);
  const error = validateCheckout(formData);
  formError.textContent = error;
  if (error) return;

  state.customer = {
    name: formData.get("name").trim(),
    email: formData.get("email").trim(),
    address: formData.get("address").trim(),
    payment: formData.get("payment"),
  };
  buildReview();
  reviewDialog.showModal();
});

document.querySelector("#placeOrder").addEventListener("click", () => {
  const total = getSubtotal() + getShipping(getSubtotal());
  const orderId = `LS-${new Date().getFullYear()}-${Math.floor(100000 + Math.random() * 900000)}`;
  completeMessage.textContent = `注文番号 ${orderId} / 合計 ${formatYen(total)}。確認メールの送信は行わないデモ表示です。`;
  reviewDialog.close();
  closeCart();
  completeDialog.showModal();
  state.cart = [];
  renderCart();
  checkoutForm.reset();
});

renderProducts();
renderCart();
