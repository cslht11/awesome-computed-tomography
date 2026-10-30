/* Phone drawer and the "/" search shortcut for the standalone pages.
   The colour theme is NOT handled here: page.html wires it in an inline head
   script, and a second listener would toggle the theme twice per click. */
(function () {
  var menu = document.getElementById("menu"), scrim = document.getElementById("scrim");
  function set(open) {
    document.body.classList.toggle("drawer-open", open);
    if (menu) menu.setAttribute("aria-expanded", String(open));
    if (scrim) scrim.hidden = !open;
  }
  if (menu) menu.addEventListener("click", function () { set(!document.body.classList.contains("drawer-open")); });
  if (scrim) scrim.addEventListener("click", function () { set(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") set(false); });
  /* "/" jumps to the search box, as on the homepage. */
  var gq = document.getElementById("gq");
  document.addEventListener("keydown", function (e) {
    var t = e.target && e.target.tagName;
    if (gq && e.key === "/" && t !== "INPUT" && t !== "TEXTAREA" && !e.metaKey && !e.ctrlKey) {
      e.preventDefault(); gq.focus();
    }
  });
})();
