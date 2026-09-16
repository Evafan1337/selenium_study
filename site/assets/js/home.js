/**
 * home.js — строит сетку популярных товаров и реализует клиентский поиск.
 */

function renderProductCard(product) {
  return `
    <div class="product-card" data-testid="product-card" data-product-id="${product.id}">
      <div class="thumb">${product.icon}</div>
      <strong class="product-name">${product.name}</strong>
      <span class="price" data-testid="product-price">$${product.price.toFixed(2)}</span>
      <a class="btn" href="product.html?id=${product.id}" data-testid="view-product-btn">View details</a>
    </div>
  `;
}

function renderGrid(products) {
  const grid = document.getElementById("featured-grid");
  const noResults = document.getElementById("no-results-msg");
  grid.innerHTML = products.map(renderProductCard).join("");
  noResults.classList.toggle("hidden", products.length > 0);
}

document.addEventListener("DOMContentLoaded", () => {
  renderGrid(PRODUCTS);

  const searchInput = document.getElementById("search-input");
  searchInput.addEventListener("input", () => {
    const term = searchInput.value.trim().toLowerCase();
    const filtered = PRODUCTS.filter((p) => p.name.toLowerCase().includes(term));
    renderGrid(filtered);
  });
});
