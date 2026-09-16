/**
 * login.js — учебная авторизация с одной заданной учётной записью.
 * При успехе сохраняет данные и открывает личный кабинет.
 */

const VALID_EMAIL = "test@example.com";
const VALID_PASSWORD = "Password123";

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("login-form");
  const errorBox = document.getElementById("login-error");

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    if (email === VALID_EMAIL && password === VALID_PASSWORD) {
      errorBox.classList.remove("visible");
      setAuth({ email: email, name: "Test User" });
      window.location.href = "dashboard.html";
    } else {
      errorBox.classList.add("visible");
    }
  });
});
