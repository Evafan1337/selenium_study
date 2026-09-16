/**
 * product.js — читает id из URL, выводит товар и подключает выбор количества,
 * добавление в корзину и переключение вкладок.
 */

function getProductIdFromUrl() {
  const params = new URLSearchParams(window.location.search);
  return Number(params.get("id"));
}

document.addEventListener("DOMContentLoaded", () => {
  const id = getProductIdFromUrl();
  const product = PRODUCTS.find((p) => p.id === id);

  if (!product) {
    document.getElementById("product-detail").classList.add("hidden");
    document.getElementById("product-not-found").classList.remove("hidden");
    return;
  }

  document.getElementById("product-thumb").textContent = product.icon;
  document.getElementById("product-name").textContent = product.name;
  document.getElementById("product-price").textContent = "$" + product.price.toFixed(2);
  document.getElementById("product-description").textContent = product.description;
  document.getElementById("product-specs").innerHTML = product.specs.map((s) => `<li>${s}</li>`).join("");

  document.getElementById("add-to-cart-btn").addEventListener("click", () => {
    const qty = Number(document.getElementById("quantity-select").value);
    addToCart(product.id, qty);
    const msg = document.getElementById("added-msg");
    msg.style.display = "block";
    setTimeout(() => (msg.style.display = "none"), 1500);
  });

  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
      document.querySelectorAll(".tab-panel").forEach((p) => p.classList.remove("active"));
      btn.classList.add("active");
      document.getElementById("panel-" + btn.dataset.tab).classList.add("active");
    });
  });
});
