/**
 * register.js — клиентская проверка формы без бэкенда: формат почты,
 * совпадение паролей и обязательный флажок.
 */

function isValidEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("register-form");
  const successBox = document.getElementById("register-success");

  const emailInput = document.getElementById("reg-email");
  const passwordInput = document.getElementById("reg-password");
  const confirmInput = document.getElementById("confirm-password");
  const termsInput = document.getElementById("terms");

  const emailError = document.getElementById("email-error");
  const passwordError = document.getElementById("password-error");
  const termsError = document.getElementById("terms-error");

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    let valid = true;

    if (!isValidEmail(emailInput.value.trim())) {
      emailError.classList.add("visible");
      valid = false;
    } else {
      emailError.classList.remove("visible");
    }

    if (passwordInput.value.length < 1 || passwordInput.value !== confirmInput.value) {
      passwordError.classList.add("visible");
      valid = false;
    } else {
      passwordError.classList.remove("visible");
    }

    if (!termsInput.checked) {
      termsError.classList.add("visible");
      valid = false;
    } else {
      termsError.classList.remove("visible");
    }

    if (!valid) return;

    successBox.classList.add("visible");
    form.querySelector("button[type=submit]").disabled = true;
    setTimeout(() => {
      window.location.href = "login.html";
    }, 1200);
  });
});
