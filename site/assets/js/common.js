/**
 * common.js — общие функции хранилища и состояния шапки.
 * Подключён на всех страницах; магазин работает без бэкенда через localStorage.
 */

const STORAGE_KEYS = {
  CART: "shopeasy_cart",       // Массив объектов {id, qty}.
  AUTH: "shopeasy_auth",       // Объект {email, name} либо null.
  ORDERS: "shopeasy_orders",   // Массив заказов.
};

const PRODUCTS = [
  { id: 1, name: "Aurora Wireless Headphones", price: 79.99, category: "audio", icon: "🎧",
    description: "Over-ear wireless headphones with active noise cancellation and 30h battery life.",
    specs: ["Bluetooth 5.3", "30h battery", "Active Noise Cancelling", "250g"] },
  { id: 2, name: "Nimbus Mechanical Keyboard", price: 129.0, category: "accessories", icon: "⌨️",
    description: "Hot-swappable mechanical keyboard with per-key RGB lighting.",
    specs: ["Hot-swap switches", "RGB backlight", "USB-C", "TKL layout"] },
  { id: 3, name: "Zenith 4K Monitor", price: 349.5, category: "displays", icon: "🖥️",
    description: "27-inch 4K IPS monitor with 99% sRGB coverage, ideal for design work.",
    specs: ["27\" IPS panel", "3840x2160", "99% sRGB", "HDMI + DisplayPort"] },
  { id: 4, name: "Pulse Fitness Tracker", price: 59.0, category: "wearables", icon: "⌚",
    description: "Lightweight fitness band with heart-rate and sleep tracking.",
    specs: ["7-day battery", "Heart rate sensor", "Water resistant", "Sleep tracking"] },
  { id: 5, name: "Orbit Portable SSD 1TB", price: 89.99, category: "storage", icon: "💾",
    description: "Compact 1TB external SSD with USB-C, read speeds up to 1050MB/s.",
    specs: ["1TB capacity", "USB-C 3.2", "1050MB/s read", "Shock resistant"] },
  { id: 6, name: "Comet Wireless Mouse", price: 34.5, category: "accessories", icon: "🖱️",
    description: "Ergonomic wireless mouse with silent clicks and adjustable DPI.",
    specs: ["Silent click", "800-3200 DPI", "Bluetooth + USB dongle", "Rechargeable"] },
];

function getCart() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEYS.CART)) || [];
  } catch (e) {
    return [];
  }
}

function saveCart(cart) {
  localStorage.setItem(STORAGE_KEYS.CART, JSON.stringify(cart));
  updateCartBadge();
}

function addToCart(productId, qty) {
  qty = qty || 1;
  const cart = getCart();
  const existing = cart.find((i) => i.id === productId);
  if (existing) {
    existing.qty += qty;
  } else {
    cart.push({ id: productId, qty: qty });
  }
  saveCart(cart);
}

function removeFromCart(productId) {
  const cart = getCart().filter((i) => i.id !== productId);
  saveCart(cart);
}

function updateCartQty(productId, qty) {
  const cart = getCart();
  const item = cart.find((i) => i.id === productId);
  if (item) item.qty = Math.max(1, qty);
  saveCart(cart);
}

function clearCart() {
  saveCart([]);
}

function cartCount() {
  return getCart().reduce((sum, i) => sum + i.qty, 0);
}

function getAuth() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEYS.AUTH));
  } catch (e) {
    return null;
  }
}

function setAuth(user) {
  localStorage.setItem(STORAGE_KEYS.AUTH, JSON.stringify(user));
}

function logout() {
  localStorage.removeItem(STORAGE_KEYS.AUTH);
  window.location.href = "login.html";
}

function requireAuth() {
  if (!getAuth()) {
    window.location.href = "login.html";
  }
}

function updateCartBadge() {
  const badge = document.getElementById("cart-count");
  if (badge) badge.textContent = String(cartCount());
}

function initNav() {
  updateCartBadge();
  const auth = getAuth();
  const authLink = document.getElementById("auth-link");
  if (!authLink) return;
  if (auth) {
    authLink.textContent = "Logout (" + auth.name + ")";
    authLink.setAttribute("href", "#");
    authLink.id = "logout-link";
    authLink.addEventListener("click", (e) => {
      e.preventDefault();
      logout();
    });
  } else {
    authLink.textContent = "Login";
    authLink.setAttribute("href", "login.html");
  }
}

document.addEventListener("DOMContentLoaded", initNav);
