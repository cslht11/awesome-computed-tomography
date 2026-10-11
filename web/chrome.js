/* Header behaviour for the static pages (About, Contact, Privacy):
   the colour-theme toggle and the phone drawer. The main page does the same in app.js. */
(function () {
  var root = document.documentElement;
  var theme = document.getElementById("theme");
  if (theme) theme.addEventListener("click", function () {
    var cur = root.getAttribute("data-theme");
    if (!cur) cur = matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    var next = cur === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem("ct-theme", next); } catch (e) {}
  });
  var menu = document.getElementById("menu"), scrim = document.getElementById("scrim");
  function set(open) {
    document.body.classList.toggle("drawer-open", open);
    if (menu) menu.setAttribute("aria-expanded", String(open));
    if (scrim) scrim.hidden = !open;
  }
  if (menu) menu.addEventListener("click", function () { set(!document.body.classList.contains("drawer-open")); });
  if (scrim) scrim.addEventListener("click", function () { set(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") set(false); });
})();
