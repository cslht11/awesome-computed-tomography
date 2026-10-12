/* Keep the query string across a language switch.

   The switch links are baked into the page at build time (absolute hrefs, no
   query), so switching from /zh/?tab=datasets&q=ct to English used to land on
   a bare "/" and drop every filter. The links are static and never rewritten
   afterwards, so appending the current query once at load is enough — and it
   is done here rather than inline because both page.html and index.html need
   it and neither should carry a second copy. */
(function () {
  var q = location.search;
  if (!q) { return; }
  var links = document.querySelectorAll(".lang-switch a[href]");
  for (var i = 0; i < links.length; i++) {
    var href = links[i].getAttribute("href");
    /* Never stack a second "?" onto a URL that already carries one. */
    if (href && href.indexOf("?") === -1) { links[i].setAttribute("href", href + q); }
  }
})();
