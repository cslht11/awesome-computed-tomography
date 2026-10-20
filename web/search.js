/* Search core for the CT list — no dependencies, one small file.
 *
 * Shared by the paper filter in app.js and by the global box in index.html, so
 * both behave identically. Written for this project; nothing here is copied
 * from another site (see the note at the bottom of this comment block).
 *
 * What it does
 * ------------
 * 1. tokenise()  — splits text the way this corpus needs. Chinese is not
 *    space-separated, so a run of ideographs is indexed as *both* its single
 *    characters and every adjacent pair: 「稀疏视角」 becomes 稀 疏 视 角 +
 *    稀疏 疏视 视角. That is what lets 「稀疏重建」 find a record titled
 *    「稀疏视角 CT 重建」 even though the user's two words never sit next to
 *    each other in the text.
 * 2. index()     — one weighted token map per record. A token keeps the
 *    *highest* weight it appears with, so a word in the title outranks the same
 *    word buried in a note.
 * 3. score()     — token weights, scaled by how much of the query matched, plus
 *    a bonus for the query appearing verbatim. Results are ranked, and a
 *    partial match still returns something instead of an empty page.
 * 4. terms()/mark()/html() — the same tokenisation drives highlighting, so what
 *    the user sees marked is exactly what was matched.
 *
 * Design notes
 * ------------
 * A library (lunr, FlexSearch, …) would be more code than this corpus needs:
 * ~450 short records fit in memory and are re-filtered per keystroke in well
 * under a millisecond. What actually decides result quality here is the
 * tokeniser and the ranking, and those are the parts a general-purpose library
 * gets wrong for Chinese titles.
 *
 * Provenance: written from scratch for this repository. No third-party source
 * was copied. Ranking ideas (field weighting, coverage, phrase bonus) are
 * standard information-retrieval practice; the implementation and constants are
 * this project's own.
 */
(function (root) {
  "use strict";

  /* CJK ranges: Extension A, the main block, and the compatibility block.
     Anything outside these is treated as "latin" (letters, digits). */
  var HAN = "\\u3400-\\u4dbf\\u4e00-\\u9fff\\uf900-\\ufaff";
  var RUN = new RegExp("[a-z0-9]+|[" + HAN + "]+", "g");
  var HAN_CHAR = new RegExp("[" + HAN + "]");
  var NON_WORD = new RegExp("[^a-z0-9" + HAN + "]", "g");

  /* One-letter latin tokens are noise ("K", "X", "A"); CJK is never dropped to
     a single-symbol rule, because one ideograph is a real word. */
  var MIN_LATIN = 2;

  /* Field weights. Only the ordering matters: title > abbreviation > metadata
     (venue, year, topic) > everything else. */
  var W = { title: 5, abbr: 4, meta: 2, body: 1 };

  /* Normalise: lower-case, unwrap inline TeX ("$K$-NeAS" → "k-neas"),
     strip zero-width characters, collapse whitespace. */
  function fold(s) {
    return String(s == null ? "" : s)
      .toLowerCase()
      .replace(/\$([^$]*)\$/g, "$1")
      .replace(/[\u200b-\u200d\ufeff]/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  }

  /* "latin words of >= 2 chars" + "CJK unigrams and bigrams". */
  function tokenize(text) {
    var s = fold(text);
    var out = [];
    var m;
    RUN.lastIndex = 0;
    while ((m = RUN.exec(s)) !== null) {
      var run = m[0];
      if (HAN_CHAR.test(run)) {
        for (var i = 0; i < run.length; i++) {
          out.push(run.charAt(i));
          if (i + 1 < run.length) out.push(run.substr(i, 2));
        }
      } else if (run.length >= MIN_LATIN) {
        out.push(run);
      }
    }
    return out;
  }

  /* Deduplicated token list + the folded query, in one object. */
  function parse(text) {
    var folded = fold(text);
    var raw = tokenize(text);
    var seen = Object.create(null);
    var tokens = [];
    for (var i = 0; i < raw.length; i++) {
      if (!seen[raw[i]]) { seen[raw[i]] = 1; tokens.push(raw[i]); }
    }
    return { text: String(text == null ? "" : text).trim(), folded: folded, tokens: tokens };
  }

  /* Build the per-record index.
     `rec` is { title, abbr, meta, body } — any of them may be missing. */
  function index(rec) {
    var map = Object.create(null);
    function add(text, weight) {
      var toks = tokenize(text);
      for (var i = 0; i < toks.length; i++) {
        var t = toks[i];
        if (!map[t] || map[t] < weight) { map[t] = weight; }
      }
    }
    add(rec.title, W.title);
    add(rec.abbr, W.abbr);
    add(rec.meta, W.meta);
    add(rec.body, W.body);
    return {
      map: map,
      /* Kept for the verbatim-phrase bonus. */
      title: fold(rec.title),
      bodyF: fold((rec.meta || "") + " " + (rec.body || ""))
    };
  }

  /* Score one indexed record. 0 means "no match".
     `sets` (optional) maps each query token to the index keys it should try —
     see matchSets(). Without it, only exact token hits count. */
  function score(doc, q, sets) {
    var toks = q.tokens;
    if (!toks.length) { return 0; }
    var sum = 0;
    var hit = 0;
    for (var i = 0; i < toks.length; i++) {
      var w = weightFor(doc, toks[i], sets ? sets[i] : null);
      if (w) { sum += w; hit++; }
    }
    if (!hit) { return 0; }
    /* Coverage factor: a record matching every term beats one that matches a
       single high-weight term. The floor keeps a lone strong hit useful. */
    var coverage = hit / toks.length;
    var s = sum * (0.35 + 0.65 * coverage);
    /* Verbatim bonus: the query typed as one string is the strongest signal a
       substring search can give, so it is worth more than token overlap. */
    if (q.folded.length >= 2) {
      if (doc.title.indexOf(q.folded) >= 0) { s += 10; }
      else if (doc.bodyF.indexOf(q.folded) >= 0) { s += 3; }
    }
    return s;
  }

  /* Best weight this document gives a query token.
     Exact key first. If there is no exact key, fall back to index keys that
     merely *contain* the token, at a discount — that is what keeps "mamba"
     finding "DenoMamba" and "splat" finding "splatting", which pure token
     equality would lose. */
  function weightFor(doc, token, variants) {
    var exact = doc.map[token];
    if (exact) { return exact; }
    if (!variants) { return 0; }
    var best = 0;
    for (var i = 0; i < variants.length; i++) {
      var w = doc.map[variants[i]];
      if (w > best) { best = w; }
    }
    /* A partial hit is real but weaker than a whole-token hit. */
    return best ? Math.max(1, best * 0.75) : 0;
  }

  /* For every query token, the index keys worth trying. Latin tokens get a
     substring fallback capped at MAX_VARIANTS so one broad token cannot make a
     query scan the whole vocabulary; CJK uni/bigrams are already the smallest
     useful units, so they are matched exactly. */
  var MAX_VARIANTS = 48;

  function matchSets(q, vocab) {
    var out = [];
    for (var i = 0; i < q.tokens.length; i++) {
      var t = q.tokens[i];
      if (vocab[t]) { out.push(null); continue; }
      if (HAN_CHAR.test(t)) { out.push(null); continue; }
      var found = [];
      for (var k in vocab) {
        if (k.length > t.length && k.indexOf(t) >= 0) {
          found.push(k);
          if (found.length >= MAX_VARIANTS) { break; }
        }
      }
      out.push(found.length ? found : null);
    }
    return out;
  }

  /* Filter + rank a built index against raw query text.
     Keeps only score > 0, so a query never comes back empty just because one
     word missed (the previous strict-AND search did exactly that).
     The sort is stable, so equal scores keep the caller's own order — for the
     paper list that is the user's chosen sort, for the dropdown it is newest
     first. */
  function search(index, text) {
    var q = parse(text);
    if (!q.tokens.length) { return []; }
    var sets = matchSets(q, index.vocab);
    var out = [];
    for (var i = 0; i < index.entries.length; i++) {
      var s = score(index.entries[i].doc, q, sets);
      if (s > 0) { out.push({ item: index.entries[i].item, s: s }); }
    }
    out.sort(function (a, b) { return b.s - a.s; });
    return out;
  }

  /* Strings worth marking in the results: the query's own phrases plus its
     tokens, longest first so a longer phrase wins over its own sub-grams. */
  function terms(text) {
    var q = parse(text);
    var set = Object.create(null);
    var phrases = q.folded.split(" ");
    for (var i = 0; i < phrases.length; i++) {
      var p = phrases[i].replace(NON_WORD, "");
      if (p.length >= 2) { set[p] = 1; }
    }
    for (var j = 0; j < q.tokens.length; j++) {
      if (q.tokens[j].length >= 2) { set[q.tokens[j]] = 1; }
    }
    var out = [];
    for (var k in set) { out.push(k); }
    out.sort(function (a, b) { return b.length - a.length; });
    return out;
  }

  /* Character ranges to mark, merged so overlapping terms produce one <mark>.
     Matching is done on the folded string, which has the same length as the
     original for every transformation fold() applies except the TeX unwrap —
     so this is only safe on text that has no "$" (titles are pre-stripped). */
  function rangesFor(text, list) {
    var s = String(text == null ? "" : text);
    if (!s || !list.length) { return []; }
    var lower = s.toLowerCase();
    var flags = new Array(s.length);
    var i, j, from, at, term;
    for (i = 0; i < list.length; i++) {
      term = list[i];
      from = 0;
      while ((at = lower.indexOf(term, from)) !== -1) {
        for (j = at; j < at + term.length; j++) { flags[j] = true; }
        from = at + term.length;
      }
    }
    var out = [];
    i = 0;
    while (i < s.length) {
      if (!flags[i]) { i++; continue; }
      j = i;
      while (j < s.length && flags[j]) { j++; }
      out.push([i, j]);
      i = j;
    }
    return out;
  }

  /* Ranges as <mark> elements appended to `parent` (DOM path, used by app.js).
     textContent is used throughout, so nothing can escape as markup. */
  function markInto(parent, text, list) {
    var s = String(text == null ? "" : text);
    var marks = rangesFor(s, list);
    if (!marks.length) { parent.appendChild(document.createTextNode(s)); return parent; }
    var pos = 0;
    for (var i = 0; i < marks.length; i++) {
      if (marks[i][0] > pos) {
        parent.appendChild(document.createTextNode(s.slice(pos, marks[i][0])));
      }
      var el = document.createElement("mark");
      el.textContent = s.slice(marks[i][0], marks[i][1]);
      parent.appendChild(el);
      pos = marks[i][1];
    }
    if (pos < s.length) { parent.appendChild(document.createTextNode(s.slice(pos))); }
    return parent;
  }

  /* Same thing as an HTML string (used by the dropdown, which builds markup).
     Each slice is escaped whole and only the matched slice is wrapped, so a
     character in the text can never break out of its own element. */
  function markHtml(text, list, esc) {
    var s = String(text == null ? "" : text);
    var marks = rangesFor(s, list);
    if (!marks.length) { return esc(s); }
    var out = "";
    var pos = 0;
    for (var i = 0; i < marks.length; i++) {
      out += esc(s.slice(pos, marks[i][0])) + "<mark>" + esc(s.slice(marks[i][0], marks[i][1])) + "</mark>";
      pos = marks[i][1];
    }
    return out + esc(s.slice(pos));
  }

  /* Build the index both callers rank against.
     Returns { entries, vocab }: the per-record wrappers, plus the set of every
     token seen anywhere — the vocabulary is what makes the substring fallback
     cheap, since a query token is matched against it instead of against every
     record in turn. */
  function build(items, toRecord) {
    var entries = [];
    var vocab = Object.create(null);
    for (var i = 0; i < items.length; i++) {
      var doc = index(toRecord(items[i]));
      for (var k in doc.map) { vocab[k] = 1; }
      entries.push({ doc: doc, item: items[i] });
    }
    return { entries: entries, vocab: vocab };
  }

  /* ---------------------------------------------------------------- records
     Payload row -> weighted fields, one mapper per section. This lives here
     rather than in app.js so that the Node test exercises the exact mapping the
     site runs, and so the paper filter and the global dropdown cannot drift. */

  function hostOf(url) {
    return String(url || "").replace(/^[a-z]+:\/\//i, "").split("/")[0];
  }

  /* An arXiv id is worth searching for in its own right — 151 of the papers
     link to one — but only as the bare id. Indexing the whole URL would let
     every other number in it (a record id, a version) match too, which is how
     typing one id used to land on an unrelated record. It goes in `meta`, not
     `body`: an identifier is metadata, and the higher weight is what makes a
     real id clear the "open the top hit" threshold while a partial one does
     not. */
  function arxivIds() {
    var out = [];
    for (var i = 0; i < arguments.length; i++) {
      var m = /arxiv\.org\/(?:abs|pdf)\/([0-9]{4}\.[0-9]{4,5})/.exec(String(arguments[i] || ""));
      if (m) { out.push(m[1]); }
    }
    return out.join(" ");
  }

  /* A title is both displayed and indexed, so drop inline TeX delimiters once,
     here: "$K$-NeAS" shows as "K-NeAS". Tokenising is unaffected (fold does the
     same unwrap), but highlighting needs the displayed string to be the one the
     ranges are computed against. */
  function plain(s) {
    return String(s == null ? "" : s).replace(/\$([^$]*)\$/g, "$1");
  }

  function mappers(topicName) {
    topicName = topicName || {};
    function join(list) {
      return list.filter(Boolean).join(" ");
    }

    function paper(p) {
      var links = p.links || {};
      var topics = (p.topics || []).map(function (id) {
        return topicName[id] || id;
      }).join(" ");
      return {
        title: plain(p.title),
        abbr: p.abbr,
        meta: join([p.venue, p.year, topics, p.preprint ? "preprint" : "",
                    arxivIds(links.paper, links.project, links.code)]),
        /* Everything below the fields above still has to be findable: the
           landmark note, and the link host so "github" or "arxiv" narrows.
           These used to arrive pre-joined as a `_q` blob from the exporter;
           building it here instead keeps one source of truth and drops ~68k
           characters of duplicated payload (payload schema 2). */
        body: join([p.note, hostOf(links.paper || links.project || links.code)])
      };
    }

    function toolkit(r) {
      return {
        title: plain(r.name),
        meta: join([r.language, r.license, (r.tags || []).join(" "), arxivIds(r.url)]),
        /* Host only, not the whole URL: the URL's own digits (an arXiv id, a
           Zenodo record number) would otherwise become searchable tokens and
           an id typed into the box would match an unrelated record. */
        body: join([r.note, hostOf(r.url)])
      };
    }

    function dataset(r) {
      return {
        title: plain(r.name),
        meta: join([r.modality, (r.tasks || []).join(" "), r.license, arxivIds(r.url)]),
        /* Host only, not the whole URL: the URL's own digits (an arXiv id, a
           Zenodo record number) would otherwise become searchable tokens and
           an id typed into the box would match an unrelated record. */
        body: join([r.note, hostOf(r.url)])
      };
    }

    function benchmark(r) {
      return {
        title: plain(r.name),
        meta: join([r.year, (r.tasks || []).join(" "), arxivIds(r.url)]),
        /* Host only, not the whole URL: the URL's own digits (an arXiv id, a
           Zenodo record number) would otherwise become searchable tokens and
           an id typed into the box would match an unrelated record. */
        body: join([r.note, hostOf(r.url)])
      };
    }

    function learning(r) {
      return {
        title: plain(r.name),
        meta: join([r.type, arxivIds(r.url)]),
        /* Host only, not the whole URL: the URL's own digits (an arXiv id, a
           Zenodo record number) would otherwise become searchable tokens and
           an id typed into the box would match an unrelated record. */
        body: join([r.note, hostOf(r.url)])
      };
    }

    /* A research team: names and people in the title field, affiliations and
       focus areas as metadata, the intro as the body. */
    function team(r) {
      var focus = ((r.focus || []).map(function (id) {
        return topicName[id] || id;
      })).join(" ");
      return {
        title: join([r.name, r.name_zh]),
        meta: join([r.institution, r.city, r.country, (r.pi || []).join(" "), focus, r.status]),
        body: join([r.intro, r.software, hostOf(r.homepage)])
      };
    }

    return {
      papers: paper, toolkits: toolkit, datasets: dataset,
      benchmarks: benchmark, learning: learning, teams: team
    };
  }

  root.CTSearch = {
    fold: fold,
    tokenize: tokenize,
    parse: parse,
    index: index,
    score: score,
    matchSets: matchSets,
    search: search,
    terms: terms,
    ranges: rangesFor,
    markInto: markInto,
    markHtml: markHtml,
    build: build,
    mappers: mappers,
    plain: plain,
    weights: W
  };
})(typeof window !== "undefined" ? window : this);
