// Mobile navigation toggle. No tracking, no external requests.
(function () {
  var btn = document.querySelector(".navtoggle");
  var nav = document.getElementById("nav");
  if (!btn || !nav) return;
  function set(open) {
    nav.classList.toggle("open", open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    btn.textContent = open ? "Close" : "Menu";
  }
  btn.addEventListener("click", function () {
    set(!nav.classList.contains("open"));
  });
  nav.addEventListener("click", function (e) {
    if (e.target.closest("a")) set(false);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && nav.classList.contains("open")) { set(false); btn.focus(); }
  });
})();

// Background videos: play only while visible, never for visitors who ask for
// reduced motion, and always with a pause button.
(function () {
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  Array.prototype.forEach.call(document.querySelectorAll("video.bg"), function (video) {
    var btn = video.parentNode.querySelector(".vtoggle");
    var stopped = reduce;   // the visitor's choice wins over scrolling
    var visible = false;
    function sync() {
      if (visible && !stopped) { var p = video.play(); if (p && p.catch) p.catch(function () {}); }
      else video.pause();
      if (btn) {
        btn.textContent = stopped ? "Play video" : "Pause video";
        btn.setAttribute("aria-pressed", stopped ? "true" : "false");
      }
    }
    if (reduce) video.removeAttribute("autoplay");
    if (btn) btn.addEventListener("click", function () { stopped = !stopped; sync(); });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        visible = entries[0].isIntersecting; sync();
      }, { rootMargin: "200px" }).observe(video);
    } else { visible = true; sync(); }
  });
})();
