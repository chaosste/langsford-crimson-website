(function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.textContent = open ? "Close" : "Menu";
    });
  }

  document.querySelectorAll(".retro-accordion__trigger").forEach(function (button) {
    button.addEventListener("click", function () {
      var item = button.closest(".retro-accordion__item");
      if (!item) return;
      var isOpen = item.classList.toggle("is-open");
      button.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
  });
})();
