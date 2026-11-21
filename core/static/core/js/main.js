(function () {
  "use strict";
  var root = document.documentElement;

  /* ---------- Thème clair / sombre (sombre par défaut) ---------- */
  var themeBtn = document.getElementById("theme-toggle");
  var meta = document.querySelector('meta[name="theme-color"]');
  function applyTheme(t) {
    root.setAttribute("data-theme", t);
    if (meta) meta.setAttribute("content", t === "dark" ? "#0c0a18" : "#fbf9ff");
    try { localStorage.setItem("theme", t); } catch (e) {}
  }
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      applyTheme(root.getAttribute("data-theme") === "dark" ? "light" : "dark");
    });
  }

  /* ---------- Menu mobile ---------- */
  var burger = document.getElementById("burger");
  var menu = document.getElementById("menu");
  function closeMenu() {
    menu.classList.remove("open");
    burger.setAttribute("aria-expanded", "false");
  }
  if (burger && menu) {
    burger.addEventListener("click", function () {
      var open = menu.classList.toggle("open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    });
    menu.addEventListener("click", function (e) { if (e.target.tagName === "A") closeMenu(); });
  }

  /* ---------- Lien actif selon la section visible ---------- */
  var links = document.querySelectorAll(".nav-links a");
  var sections = Array.prototype.map.call(links, function (a) {
    return document.querySelector(a.getAttribute("href"));
  });
  if ("IntersectionObserver" in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) {
          a.classList.toggle("active", a.getAttribute("href") === "#" + en.target.id);
        });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    sections.forEach(function (s) { if (s) spy.observe(s); });
  }

  /* ---------- Onglets de compétences + barres animées ---------- */
  var tabs = document.querySelectorAll(".tab");
  var panels = document.querySelectorAll(".skill-panel");
  var skillSection = document.getElementById("competences");
  var skillsSeen = false;

  function markInView() {
    panels.forEach(function (p) { if (p.classList.contains("is-active")) p.classList.add("in-view"); });
  }
  tabs.forEach(function (tab) {
    tab.addEventListener("click", function () {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.classList.toggle("is-active", on);
        t.setAttribute("aria-selected", on ? "true" : "false");
      });
      panels.forEach(function (p) {
        var on = p.getAttribute("data-panel") === tab.getAttribute("data-tab");
        p.classList.toggle("is-active", on);
        p.classList.remove("in-view");
      });
      if (skillsSeen) requestAnimationFrame(function () { requestAnimationFrame(markInView); });
    });
  });
  if (skillSection && "IntersectionObserver" in window) {
    var barObs = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) { skillsSeen = true; markInView(); barObs.disconnect(); }
    }, { threshold: 0.25 });
    barObs.observe(skillSection);
  } else { skillsSeen = true; markInView(); }

  /* ---------- Filtre des projets ---------- */
  var filterBtns = document.querySelectorAll(".chip-btn");
  var cards = document.querySelectorAll(".project");
  filterBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var f = btn.getAttribute("data-filter");
      filterBtns.forEach(function (b) { b.classList.toggle("is-active", b === btn); });
      cards.forEach(function (c) {
        c.hidden = !(f === "all" || c.getAttribute("data-cat") === f);
      });
    });
  });

  /* ---------- Formulaire de contact (AJAX) ---------- */
  var form = document.getElementById("contact-form");
  if (form) {
    var status = document.getElementById("form-status");
    var submit = document.getElementById("f-submit");

    function clearErrors() {
      form.querySelectorAll(".err").forEach(function (e) { e.textContent = ""; });
      form.querySelectorAll(".field").forEach(function (f) { f.classList.remove("has-error"); });
      status.textContent = ""; status.className = "form-status";
    }
    function showErrors(errors) {
      Object.keys(errors).forEach(function (k) {
        var el = form.querySelector('[data-err="' + k + '"]');
        if (el) { el.textContent = errors[k]; el.closest(".field").classList.add("has-error"); }
      });
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      clearErrors();

      var local = {};
      if (!form.name.value.trim()) local.name = "Indique ton nom.";
      if (!/^\S+@\S+\.\S+$/.test(form.email.value.trim())) local.email = "Indique une adresse e-mail valide.";
      if (form.body.value.trim().length < 10) local.body = "Écris un message d'au moins 10 caractères.";
      if (Object.keys(local).length) { showErrors(local); return; }

      submit.disabled = true;
      submit.textContent = "Envoi en cours…";

      fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: { "X-Requested-With": "XMLHttpRequest" },
        credentials: "same-origin"
      })
        .then(function (r) { return r.json().then(function (data) { return { ok: r.ok, data: data }; }); })
        .then(function (res) {
          if (res.ok && res.data.ok) {
            form.reset();
            status.textContent = res.data.message;
            status.className = "form-status ok";
          } else {
            showErrors(res.data.errors || {});
            status.textContent = "Le message n'a pas été envoyé. Vérifie les champs en rouge.";
            status.className = "form-status bad";
          }
        })
        .catch(function () {
          status.textContent = "Connexion impossible. Réessaie ou écris-moi directement par e-mail.";
          status.className = "form-status bad";
        })
        .finally(function () {
          submit.disabled = false;
          submit.textContent = "Envoyer le message";
        });
    });
  }
})();
