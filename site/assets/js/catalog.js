/**
 * catalog.js — клиентская фильтрация по категории и цене, а также сортировка.
 */

function renderCatalogCard(product) {
  return `
    <div class="product-card" data-testid="product-card" data-product-id="${product.id}" data-category="${product.category}">
      <div class="thumb">${product.icon}</div>
      <strong class="product-name">${product.name}</strong>
      <span class="price" data-testid="product-price">$${product.price.toFixed(2)}</span>
      <a class="btn" href="product.html?id=${product.id}" data-testid="view-product-btn">View details</a>
    </div>
  `;
}

function applyFilters() {
  const category = document.getElementById("category-filter").value;
  const maxPrice = Number(document.getElementById("max-price").value);
  const sort = document.getElementById("sort-select").value;

  let items = PRODUCTS.filter((p) => (category === "all" || p.category === category) && p.price <= maxPrice);

  if (sort === "price-asc") items = items.sort((a, b) => a.price - b.price);
  if (sort === "price-desc") items = items.sort((a, b) => b.price - a.price);
  if (sort === "name-asc") items = items.sort((a, b) => a.name.localeCompare(b.name));

  document.getElementById("catalog-grid").innerHTML = items.map(renderCatalogCard).join("");
  document.getElementById("result-count").textContent = String(items.length);
}

document.addEventListener("DOMContentLoaded", () => {
  applyFilters();

  document.getElementById("category-filter").addEventListener("change", applyFilters);
  document.getElementById("sort-select").addEventListener("change", applyFilters);

  const priceRange = document.getElementById("max-price");
  priceRange.addEventListener("input", () => {
    document.getElementById("max-price-value").textContent = priceRange.value;
    applyFilters();
  });
});
