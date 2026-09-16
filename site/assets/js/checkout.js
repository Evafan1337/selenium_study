/**
 * checkout.js — мастер из трёх шагов: доставка, оплата и проверка.
 * Секции переключаются через .step-panel, поля карты показываются условно,
 * а перед созданием заказа открывается window.confirm().
 */

function showStep(stepNumber) {
  document.querySelectorAll(".step-panel").forEach((el) => el.classList.remove("active"));
  document.getElementById("step-" + stepNumber).classList.add("active");

  [1, 2, 3].forEach((n) => {
    const indicator = document.getElementById("step-indicator-" + n);
    indicator.classList.remove("active", "done");
    if (n === stepNumber) indicator.classList.add("active");
    if (n < stepNumber) indicator.classList.add("done");
  });
}

function cartTotal() {
  const cart = getCart();
  return cart.reduce((sum, item) => {
    const product = PRODUCTS.find((p) => p.id === item.id);
    return sum + product.price * item.qty;
  }, 0);
}

function selectedPaymentLabel() {
  const selected = document.querySelector('input[name="payment"]:checked').value;
  return { card: "Credit card", paypal: "PayPal", cash: "Cash on delivery" }[selected];
}

document.addEventListener("DOMContentLoaded", () => {
  const cartEmpty = getCart().length === 0;
  document.getElementById("cart-empty-warning").classList.toggle("visible", cartEmpty);
  document.getElementById("checkout-flow").classList.toggle("hidden", cartEmpty);
  if (cartEmpty) return;

  document.getElementById("to-step-2").addEventListener("click", () => showStep(2));
  document.getElementById("to-step-1").addEventListener("click", () => showStep(1));
  document.getElementById("to-step-2-back").addEventListener("click", () => showStep(2));

  document.querySelectorAll('input[name="payment"]').forEach((radio) => {
    radio.addEventListener("change", () => {
      const cardFields = document.getElementById("card-fields");
      cardFields.classList.toggle("hidden", radio.value !== "card" || !radio.checked);
    });
  });

  document.getElementById("to-step-3").addEventListener("click", () => {
    document.getElementById("review-name").textContent = document.getElementById("full-name").value || "(not provided)";
    document.getElementById("review-address").textContent =
      [document.getElementById("address").value, document.getElementById("city").value, document.getElementById("zip").value]
        .filter(Boolean).join(", ") || "(not provided)";
    document.getElementById("review-payment").textContent = selectedPaymentLabel();
    document.getElementById("review-total").textContent = "$" + cartTotal().toFixed(2);
    showStep(3);
  });

  document.getElementById("place-order-btn").addEventListener("click", () => {
    const confirmed = window.confirm("Place this order now?");
    if (!confirmed) return;

    const orderNumber = "SE-" + Math.floor(100000 + Math.random() * 900000);
    document.getElementById("order-number").textContent = orderNumber;
    clearCart();

    document.querySelectorAll(".step-panel").forEach((el) => el.classList.remove("active"));
    document.getElementById("step-confirmation").classList.add("active");
    document.querySelectorAll(".step").forEach((el) => el.classList.add("done"));
  });
});
