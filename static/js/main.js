const sidebar = document.getElementById("sidebar");
const toggleBtn = document.getElementById("toggle-btn");
const main = document.querySelector("main");
const toggleIcon = document.getElementById("toggle-icon");

toggleBtn.addEventListener("click", function() {
  sidebar.classList.toggle("collapsed");
  main.classList.toggle("collapsed");

  if (sidebar.classList.contains("collapsed")) {
    toggleIcon.setAttribute("data-lucide", "chevrons-right");
  } else {
    toggleIcon.setAttribute("data-lucide", "chevrons-left");
  }

  lucide.createIcons();
});