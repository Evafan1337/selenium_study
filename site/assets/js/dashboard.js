/**
 * dashboard.js — защищённая страница с перенаправлением неавторизованного
 * пользователя и диалогом подтверждения удаления аккаунта.
 */

document.addEventListener("DOMContentLoaded", () => {
  requireAuth();
  const auth = getAuth();
  if (!auth) return;

  document.getElementById("welcome-msg").textContent = `Welcome back, ${auth.name} (${auth.email})`;

  document.getElementById("delete-account-btn").addEventListener("click", () => {
    const confirmed = window.confirm("Are you sure you want to delete your account? This cannot be undone.");
    if (confirmed) {
      logout();
    }
  });
});
