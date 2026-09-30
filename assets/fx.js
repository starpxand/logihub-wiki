/* ЛогиХаб FX: счётчики, появление при прокрутке, 3D-наклон карточек, прожектор, прогресс чтения */
(function () {
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var still = /[?&]lh-static/.test(window.location.search);

  function counters(root) {
    root.querySelectorAll("[data-count]").forEach(function (el) {
      if (el.dataset.lhDone) return;
      el.dataset.lhDone = "1";
      var raw = el.dataset.count;
      var target = parseFloat(raw.replace(",", "."));
      var dec = (raw.split(/[.,]/)[1] || "").length;
      if (reduce || still || isNaN(target)) return;
      var t0 = null, dur = 1800;
      function step(t) {
        if (t0 === null) t0 = t;
        var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
        el.textContent = (target * e).toFixed(dec).replace(".", ",");
        if (p < 1) requestAnimationFrame(step);
      }
      el.textContent = (0).toFixed(dec).replace(".", ",");
      requestAnimationFrame(step);
      setTimeout(function () { el.textContent = raw; }, dur + 150);
    });
  }

  var io = null;
  function reveal() {
    if (reduce || still || !("IntersectionObserver" in window)) return;
    if (io) io.disconnect();
    io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("lh-in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    var sel = [
      ".md-content .md-typeset > h2", ".md-content .md-typeset > .md-typeset__scrollwrap",
      ".md-content .md-typeset .grid.cards > ul > li", ".md-content .md-typeset > .admonition",
      ".md-content .md-typeset > .mermaid", ".md-content .md-typeset > .tabbed-set",
      ".md-content .md-typeset > p > img", ".md-content .md-typeset > blockquote"
    ].join(",");
    document.querySelectorAll(sel).forEach(function (el, i) {
      el.classList.add("lh-reveal");
      el.style.transitionDelay = (i % 6) * 60 + "ms";
      io.observe(el);
    });
  }

  function tilt() {
    if (reduce) return;
    document.querySelectorAll(".md-typeset .grid.cards > ul > li").forEach(function (card) {
      if (card.dataset.lhTilt) return;
      card.dataset.lhTilt = "1";
      card.addEventListener("mousemove", function (e) {
        var r = card.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        card.style.setProperty("--ry", ((x - 0.5) * 10).toFixed(2) + "deg");
        card.style.setProperty("--rx", ((0.5 - y) * 10).toFixed(2) + "deg");
        card.style.setProperty("--mx", (x * 100).toFixed(1) + "%");
        card.style.setProperty("--my", (y * 100).toFixed(1) + "%");
      });
      card.addEventListener("mouseleave", function () {
        card.style.setProperty("--rx", "0deg");
        card.style.setProperty("--ry", "0deg");
      });
    });
  }

  function spotlight() {
    var hero = document.querySelector("[data-lh-spotlight]");
    if (!hero || hero.dataset.lhSpot || reduce) return;
    hero.dataset.lhSpot = "1";
    hero.addEventListener("mousemove", function (e) {
      var r = hero.getBoundingClientRect();
      hero.style.setProperty("--sx", ((e.clientX - r.left) / r.width * 100).toFixed(1) + "%");
      hero.style.setProperty("--sy", ((e.clientY - r.top) / r.height * 100).toFixed(1) + "%");
    });
  }

  function progress() {
    var bar = document.getElementById("lh-progress");
    if (!bar) {
      bar = document.createElement("div");
      bar.id = "lh-progress";
      document.body.appendChild(bar);
      window.addEventListener("scroll", update, { passive: true });
      window.addEventListener("resize", update);
    }
    function update() {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.transform = "scaleX(" + (h > 0 ? window.scrollY / h : 0) + ")";
    }
    update();
  }

  function init() { counters(document); reveal(); tilt(); spotlight(); progress(); }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(init);
  } else if (document.readyState !== "loading") {
    init();
  } else {
    document.addEventListener("DOMContentLoaded", init);
  }
})();
