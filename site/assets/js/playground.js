/**
 * playground.js — подключает виджеты полигона. Каждый блок независим;
 * примеры Selenium находятся в standalone_examples и tests/test_playground.py.
 */

document.addEventListener("DOMContentLoaded", () => {
  // 1. Диалоги JavaScript.
  document.getElementById("alert-btn").addEventListener("click", () => {
    alert("This is a plain alert.");
    document.getElementById("dialog-result").textContent = "alert() was dismissed";
  });
  document.getElementById("confirm-btn").addEventListener("click", () => {
    const ok = confirm("Do you confirm this action?");
    document.getElementById("dialog-result").textContent = ok ? "confirm() accepted" : "confirm() dismissed";
  });
  document.getElementById("prompt-btn").addEventListener("click", () => {
    const value = prompt("What is your name?");
    document.getElementById("dialog-result").textContent = value ? `prompt() returned: ${value}` : "prompt() dismissed";
  });

  // 3. Нативное перетаскивание HTML5.
  const draggable = document.getElementById("draggable");
  const dropzone = document.getElementById("dropzone");
  draggable.addEventListener("dragstart", (e) => {
    e.dataTransfer.setData("text/plain", "dragged");
  });
  dropzone.addEventListener("dragover", (e) => e.preventDefault());
  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.textContent = "Dropped!";
    dropzone.dataset.testid = "dropzone";
  });

  // 4. Динамическая загрузка.
  document.getElementById("load-btn").addEventListener("click", () => {
    document.getElementById("loaded-content").classList.add("hidden");
    document.getElementById("loading-spinner").classList.remove("hidden");
    setTimeout(() => {
      document.getElementById("loading-spinner").classList.add("hidden");
      document.getElementById("loaded-content").classList.remove("hidden");
    }, 2000);
  });

  // 7. Загрузка файла.
  document.getElementById("file-input").addEventListener("change", (e) => {
    const file = e.target.files[0];
    document.getElementById("file-name").textContent = file ? `Selected: ${file.name}` : "";
  });

  // 8. Множественный выбор.
  document.getElementById("multi-select").addEventListener("change", (e) => {
    const selected = Array.from(e.target.selectedOptions).map((o) => o.text);
    document.getElementById("multi-select-result").textContent = "Selected: " + selected.join(", ");
  });

  // 9. Сортируемая таблица: клик по заголовку сортирует столбец.
  function sortTableBy(colIndex, numeric) {
    const tbody = document.getElementById("sortable-table-body");
    const rows = Array.from(tbody.querySelectorAll("tr"));
    rows.sort((a, b) => {
      const aVal = a.children[colIndex].textContent;
      const bVal = b.children[colIndex].textContent;
      return numeric ? Number(aVal) - Number(bVal) : aVal.localeCompare(bVal);
    });
    rows.forEach((r) => tbody.appendChild(r));
  }
  document.querySelector("[data-testid=sort-by-name]").addEventListener("click", () => sortTableBy(0, false));
  document.querySelector("[data-testid=sort-by-age]").addEventListener("click", () => sortTableBy(1, true));

  // 10. Ползунок диапазона.
  const slider = document.getElementById("volume-slider");
  slider.addEventListener("input", () => {
    document.getElementById("volume-value").textContent = slider.value;
  });

  // 11. Включение и отключение элемента.
  document.getElementById("enable-checkbox").addEventListener("change", (e) => {
    document.getElementById("toggle-target-btn").disabled = !e.target.checked;
  });
});
