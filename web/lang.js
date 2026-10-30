/* Keep the page state across a language switch.

   The switch links are baked into the page at build time (absolute hrefs, no
   query), pointing at the same page in the other language. The state that
   must survive the switch lives in the address bar: the homepage's tab and
   filters (?tab=datasets&topic=...), which app.js rewrites with
   history.replaceState as the reader clicks, and #anchors on the sub-pages.

   An earlier version appended the query once, at load. Any tab or filter
   chosen after that was lost, so switching language from a tab the reader
   had clicked landed on the Papers tab. The href is therefore rebuilt from
   the current address at the moment it is used: on click, middle-click,
   right-click (copy link) and keyboard focus. Both page.html and index.html
   load this file, so neither carries a copy of it. */
(function () {
  var links = document.querySelectorAll(".lang-switch a[href]");
  function sync(a) {
    var base = a.getAttribute("data-base");
    if (!base) {
      base = a.getAttribute("href").split(/[?#]/)[0];
      a.setAttribute("data-base", base);
    }
    a.setAttribute("href", base + location.search + location.hash);
  }
  for (var i = 0; i < links.length; i++) {
    sync(links[i]);
    ["click", "auxclick", "contextmenu", "focus", "mouseenter", "touchstart"].forEach(function (ev) {
      links[i].addEventListener(ev, function () { sync(this); }, { passive: true });
    });
  }
})();
