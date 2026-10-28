(function () {
  var WHATSAPP = "5551980515585";

  // Ano no rodapé
  var year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();

  // Sombra no cabeçalho ao rolar
  var header = document.getElementById("header");
  function onScroll() {
    header.classList.toggle("is-scrolled", window.scrollY > 10);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Menu mobile
  var toggle = document.getElementById("navToggle");
  var nav = document.getElementById("nav");
  function setMenu(open) {
    nav.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Fechar menu" : "Abrir menu");
  }
  toggle.addEventListener("click", function () {
    setMenu(!nav.classList.contains("is-open"));
  });
  nav.addEventListener("click", function (e) {
    if (e.target.closest("a")) setMenu(false);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") setMenu(false);
  });

  // Animação de entrada dos blocos
  var targets = document.querySelectorAll(
    ".section__head, .service, .steps li, .segment, .benefit, .cities li, .faq details, .feature, .detail, .post-card, .plan, .city, .info-card"
  );
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    targets.forEach(function (el) {
      el.classList.add("reveal");
      io.observe(el);
    });
  }

  // Formulário -> WhatsApp com mensagem pronta
  var form = document.getElementById("contactForm");
  var error = document.getElementById("formError");
  if (form) form.addEventListener("submit", function (e) {
    e.preventDefault();
    var data = new FormData(form);
    var required = ["nome", "cidade", "servico"];
    var valid = true;

    required.forEach(function (name) {
      var field = form.elements[name];
      var empty = !String(data.get(name) || "").trim();
      field.classList.toggle("is-invalid", empty);
      if (empty) valid = false;
    });
    error.hidden = valid;
    if (!valid) return;

    var lines = [
      "Olá! Vim pelo site e gostaria de um orçamento.",
      "",
      "*Nome:* " + data.get("nome"),
    ];
    if (data.get("empresa")) lines.push("*Empresa:* " + data.get("empresa"));
    lines.push("*Cidade:* " + data.get("cidade"));
    lines.push("*Serviço:* " + data.get("servico"));
    if (data.get("equipamentos")) lines.push("*Equipamentos:* " + data.get("equipamentos"));
    if (data.get("mensagem")) lines.push("*Mensagem:* " + data.get("mensagem"));

    var url = "https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent(lines.join("\n"));
    window.open(url, "_blank", "noopener");
  });
})();
