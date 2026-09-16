/**
 * cart.js — строит корзину из localStorage, пересчитывает итоговую сумму
 * при изменении количества и удаляет строки.
 */

function renderCart() {
  const cart = getCart();
  const emptyMsg = document.getElementById("empty-cart-msg");
  const table = document.getElementById("cart-table");
  const summary = document.getElementById("cart-summary");

  if (cart.length === 0) {
    emptyMsg.classList.remove("hidden");
    table.classList.add("hidden");
    summary.classList.add("hidden");
    return;
  }

  emptyMsg.classList.add("hidden");
  table.classList.remove("hidden");
  summary.classList.remove("hidden");

  const body = document.getElementById("cart-body");
  let total = 0;

  body.innerHTML = cart.map((item) => {
    const product = PRODUCTS.find((p) => p.id === item.id);
    const subtotal = product.price * item.qty;
    total += subtotal;
    return `
      <tr data-testid="cart-row" data-product-id="${product.id}">
        <td>${product.name}</td>
        <td>$${product.price.toFixed(2)}</td>
        <td>
          <input type="number" min="1" class="qty-input" value="${item.qty}"
                 data-testid="cart-qty-input" data-product-id="${product.id}">
        </td>
        <td data-testid="cart-row-subtotal">$${subtotal.toFixed(2)}</td>
        <td><button class="btn-danger" data-testid="cart-remove-btn" data-product-id="${product.id}">Remove</button></td>
      </tr>
    `;
  }).join("");

  document.getElementById("cart-total").textContent = "$" + total.toFixed(2);

  body.querySelectorAll("[data-testid=cart-qty-input]").forEach((input) => {
    input.addEventListener("change", () => {
      updateCartQty(Number(input.dataset.productId), Number(input.value));
      renderCart();
    });
  });

  body.querySelectorAll("[data-testid=cart-remove-btn]").forEach((btn) => {
    btn.addEventListener("click", () => {
      removeFromCart(Number(btn.dataset.productId));
      renderCart();
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  renderCart();
  document.getElementById("checkout-btn").addEventListener("click", () => {
    window.location.href = "checkout.html";
  });
});
