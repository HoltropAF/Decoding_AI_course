  /* Owns Dictionary UI and transient state. Storage and dashboard navigation are supplied by the caller. */
  function createDictionary(deps) {
    var { entries: D, figures, termSlug, el, esc, inlineMd, makeFigure, whereLinks, loadView, saveView, replaceSelection } = deps;
    var dictState = { q: "", cat: "", sel: null }, dictView;
    function plain(text) { return text.replace(/[`*]/g, ""); }
    function highlight(text, q) {
      var safe = esc(plain(text));
      if (!q) return safe;
      var qq = esc(q), i = safe.toLowerCase().indexOf(qq.toLowerCase());
      if (i < 0) return safe;
      return safe.slice(0, i) + "<mark>" + safe.slice(i, i + qq.length) + "</mark>" + safe.slice(i + qq.length);
    }

    function renderDict(main, focusTerm) {
      if (focusTerm) { dictState.q = ""; dictState.cat = ""; dictState.sel = focusTerm; }
      var cats = [];
      D.forEach(function (e) { if (cats.indexOf(e.cat) < 0) cats.push(e.cat); });
      var bySlug = Object.create(null);
      D.forEach(function (e) { bySlug[termSlug(e.term)] = e; });
      if (dictState.sel && !bySlug[dictState.sel]) dictState.sel = null;

      var browser = main.ownerDocument.defaultView;
      var page = el("div", { class: "page dict-page" });
      page.appendChild(el("div", { class: "modtop" }, [
        el("span", { class: "label", text: "Dictionary \u00b7 " + D.length + " words" }),
        el("h2", { text: "Dictionary" }),
        el("p", { text: "Every word used in the course, explained in plain language: a short definition, a longer explanation, an example from our own kind of work, related words, and links to where the course explains it. Search, or pick a word from the list." })
      ]));

      /* ---- toolbar: search, topic, view ---- */
      var input = el("input", { class: "dict-search", type: "search", id: "dict-search", placeholder: "Search a word, e.g. token, prompt, padj, Docker\u2026", "aria-label": "Search the dictionary", autocomplete: "off" });
      input.value = dictState.q;
      function opt(v, label, cur) { return el("option", { value: v, text: label, selected: v === cur ? "selected" : null }); }
      var catSel = el("select", { "aria-label": "Topic" }, [opt("", "All topics", dictState.cat)].concat(cats.map(function (c) { return opt(c, c, dictState.cat); })));

      if (!dictView) dictView = loadView();
      var view = focusTerm ? { mode: "lookup", cols: dictView.cols } : dictView;
      var modeSel = el("select", { "aria-label": "Dictionary view" }, [opt("lookup", "Look up one word", view.mode), opt("cards", "Browse as cards", view.mode), opt("list", "Browse as list", view.mode)]);
      var colSel = el("select", { "aria-label": "Number of columns" }, [opt("auto", "Fit to screen", view.cols), opt("1", "1 column", view.cols), opt("2", "2 columns", view.cols), opt("3", "3 columns", view.cols), opt("4", "4 columns", view.cols)]);
      var colWrap = el("label", { class: "viewopt" }, [el("span", { text: "Columns" }), colSel]);
      var count = el("span", { class: "dict-count", role: "status", "aria-live": "polite" });
      page.appendChild(el("div", { class: "dict-toolbar" }, [
        input,
        el("label", { class: "viewopt topicopt" }, [el("span", { text: "Topic" }), catSel]),
        el("label", { class: "viewopt viewonly" }, [el("span", { text: "View" }), modeSel]),
        colWrap
      ]));

      /* ---- areas ---- */
      var lookup = el("div", { class: "dlook" });
      var listPane = el("div", { class: "dlook-list", role: "navigation", "aria-label": "Words" });
      var detail = el("article", { class: "dlook-detail", "aria-live": "polite" });
      var topicChips = el("div", { class: "dl-topics", role: "group", "aria-label": "Filter by topic" });
      function drawTopics() {
        topicChips.textContent = "";
        [""].concat(cats).forEach(function (c) {
          var b = el("button", { type: "button", "aria-pressed": dictState.cat === c ? "true" : "false", text: c ? ({ "AI concepts and techniques": "AI concepts", "Lab and data terms": "Lab and data", "Computer and tool terms": "Computers and tools" }[c] || c) : "All" });
          b.addEventListener("click", function () { dictState.cat = c; catSel.value = c; drawTopics(); update(); });
          topicChips.appendChild(b);
        });
      }
      drawTopics();
      lookup.appendChild(el("div", { class: "dlook-side" }, [el("div", { class: "dl-head" }, [count, topicChips]), listPane]));
      lookup.appendChild(detail);
      var browse = el("div", { class: "dict-list" });
      page.appendChild(lookup);
      page.appendChild(browse);
      main.appendChild(page);

      var hits = [];
      function filtered() {
        var q = dictState.q.trim().toLowerCase();
        var inTerm = function (e) { return plain(e.term).toLowerCase().indexOf(q) >= 0; };
        var out = D.filter(function (e) {
          if (dictState.cat && e.cat !== dictState.cat) return false;
          if (!q) return true;
          return inTerm(e) || plain(e.def).toLowerCase().indexOf(q) >= 0 || plain(e.ex || "").toLowerCase().indexOf(q) >= 0 || plain(e.more || "").toLowerCase().indexOf(q) >= 0;
        });
        if (q) {
          var rank = function (e) {
            var t = plain(e.term).toLowerCase();
            if (t === q || t.split(/[\s/()]+/).indexOf(q) >= 0) return 0;
            if (t.indexOf(q) === 0) return 1;
            return inTerm(e) ? 2 : 3;
          };
          out.sort(function (x, y) { return rank(x) - rank(y); });
        }
        return out;
      }

      /* ---- the detail of one word ---- */
      function showDetail() {
        detail.textContent = "";
        lookup.classList.toggle("has-sel", !!dictState.sel);
        var e = dictState.sel && bySlug[dictState.sel];
        if (!e) {
          var starters = ["Artificial intelligence (AI)", "Large language model (LLM)", "Token", "Prompt", "Context window", "Hallucination / fabrication", "Temperature", "Agent"];
          detail.appendChild(el("div", { class: "dd-empty" }, [
            el("span", { class: "label", text: "Where to start" }),
            el("h3", { text: "Pick a word to see what it means" }),
            el("p", { text: "New to all of this? These eight words explain most of what you'll read in the course:" }),
            el("div", { class: "dd-chips" }, starters.filter(function (t) { return bySlug[termSlug(t)]; }).map(function (t) {
              var b = el("button", { type: "button", text: plain(t) });
              b.addEventListener("click", function () { select(termSlug(t)); });
              return b;
            }))
          ]));
          return;
        }
        var idx = hits.indexOf(e);
        var back = el("button", { type: "button", class: "dd-back", text: "\u2190 All words" });
        back.addEventListener("click", function () { select(null); });
        var where = whereLinks(e.where);
        detail.appendChild(back);
        detail.appendChild(el("div", { class: "dd-cat" }, [el("span", { text: e.cat })]));
        detail.appendChild(el("h3", { class: "dd-term", tabindex: "-1", html: esc(plain(e.term)) }));
        detail.appendChild(el("section", { class: "dd-block" }, [el("h4", { text: "In short" }), el("p", { class: "dd-def", html: inlineMd(e.def) })]));
        if (e.more) detail.appendChild(el("section", { class: "dd-block" }, [el("h4", { text: "Explained" }), el("p", { class: "dd-more", html: inlineMd(e.more) })]));
        if (e.fig && figures[e.fig]) {
          var src = figures[e.fig];
          detail.appendChild(el("figure", { class: "dd-fig" }, [makeFigure(src, e.figcap || plain(e.term)), e.figcap ? el("figcaption", { text: e.figcap }) : null]));
        }
        if (e.ex) detail.appendChild(el("section", { class: "dd-block dd-ex" }, [el("h4", { text: "Example" }), el("p", { html: inlineMd(e.ex) })]));
        if ((e.see || []).length) detail.appendChild(el("section", { class: "dd-block" }, [el("h4", { text: "Related words" }),
          el("div", { class: "dd-chips" }, e.see.map(function (t) {
            var b = el("button", { type: "button", text: plain(t), title: (bySlug[termSlug(t)] || {}).def ? plain(bySlug[termSlug(t)].def) : "" });
            b.addEventListener("click", function () { select(termSlug(t)); });
            return b;
          }))]));
        if ((e.links || []).length) detail.appendChild(el("section", { class: "dd-block" }, [el("h4", { text: "Read more in the course" }),
          el("ul", { class: "dd-links" }, e.links.map(function (l) {
            var parts = l.label.split(" · ");
            return el("li", null, [el("a", { href: l.href }, [el("span", { class: "dd-lk-where", text: parts.slice(0, 2).join(" · ") }), el("span", { class: "dd-lk-title", text: parts.slice(2).join(" · ") })])]);
          }))]));
        else if (where.length) detail.appendChild(el("section", { class: "dd-block" }, [el("h4", { text: "Where it comes up" }), el("div", { class: "dd-where" }, where)]));
        var prev = el("button", { type: "button", class: "btn", text: "\u2039 " + (idx > 0 ? plain(hits[idx - 1].term) : "") });
        var next = el("button", { type: "button", class: "btn", text: (idx >= 0 && idx < hits.length - 1 ? plain(hits[idx + 1].term) : "") + " \u203a" });
        prev.disabled = idx <= 0; next.disabled = idx < 0 || idx >= hits.length - 1;
        prev.addEventListener("click", function () { if (idx > 0) select(termSlug(hits[idx - 1].term)); });
        next.addEventListener("click", function () { if (idx < hits.length - 1) select(termSlug(hits[idx + 1].term)); });
        detail.appendChild(el("div", { class: "dd-nav" }, [prev, next]));
      }

      function select(slug) {
        var previous = dictState.sel;
        dictState.sel = slug;
        replaceSelection(slug);
        listPane.querySelectorAll("button.dl-item").forEach(function (b) {
          var on = b.getAttribute("data-slug") === slug;
          b.classList.toggle("on", on);
          if (on) b.setAttribute("aria-current", "true"); else b.removeAttribute("aria-current");
          if (on) b.scrollIntoView({ block: "nearest" });
        });
        showDetail();
        if (slug) detail.querySelector(".dd-term").focus({ preventScroll: true });
        else {
          var word = Array.from(listPane.querySelectorAll(".dl-item")).find(function (b) { return b.getAttribute("data-slug") === previous; });
          (word || input).focus({ preventScroll: true });
        }
        if (slug && browser.matchMedia("(max-width: 700px)").matches) browser.scrollTo(0, 0);
        else if (slug && detail.getBoundingClientRect().top < 0) detail.scrollIntoView({ block: "start" });
      }

      /* ---- the word list (look-up view) ---- */
      function drawList() {
        listPane.textContent = "";
        var q = dictState.q.trim();
        if (!hits.length) {
          listPane.appendChild(el("p", { class: "dict-empty", text: "No match for \u201c" + q + "\u201d. Try a shorter word, or check the spelling." }));
          return;
        }
        var lastL = null;
        hits.forEach(function (e) {
          var L = q ? "" : plain(e.term).charAt(0).toUpperCase();
          if (/^[0-9]/.test(L)) L = "#";
          if (L && L !== lastL) { listPane.appendChild(el("div", { class: "dl-letter", text: L })); lastL = L; }
          var slug = termSlug(e.term);
          var b = el("button", { type: "button", class: "dl-item" + (slug === dictState.sel ? " on" : ""), "data-slug": slug, html: highlight(e.term, q) });
          b.addEventListener("click", function () { select(slug); });
          listPane.appendChild(b);
        });
        var on = listPane.querySelector(".dl-item.on");
        if (on) on.scrollIntoView({ block: "nearest" }); else listPane.scrollTop = 0;
      }

      /* ---- browse views (cards or list), as before ---- */
      function drawBrowse() {
        browse.textContent = "";
        var q = dictState.q.trim().toLowerCase();
        if (!hits.length) { browse.appendChild(el("p", { class: "dict-empty", text: "No match. Try a shorter word, or check the spelling." })); return; }
        var groups = {}, order = [];
        var inTerm = function (e) { return plain(e.term).toLowerCase().indexOf(q) >= 0; };
        hits.forEach(function (e) {
          var L = q ? (inTerm(e) ? "Matching words" : "Mentioned in an explanation") : plain(e.term).charAt(0).toUpperCase();
          if (/^[0-9]/.test(L)) L = "#";
          if (!groups[L]) { groups[L] = []; order.push(L); }
          groups[L].push(e);
        });
        order.forEach(function (L) {
          var g = el("section", { class: "dict-group" }, [el("div", { class: "dict-letter", text: L })]);
          groups[L].forEach(function (e) {
            var open = el("button", { type: "button", class: "term", html: highlight(e.term, q), title: "Open this word" });
            open.addEventListener("click", function () { view.mode = "lookup"; modeSel.value = "lookup"; applyView(true); select(termSlug(e.term)); });
            g.appendChild(el("article", { class: "entry", id: "term-" + termSlug(e.term) }, [
              open,
              el("div", { class: "def", html: inlineMd(e.def) }),
              e.ex ? el("div", { class: "ex" }, [el("span", { class: "ex-label", text: "Example" }), el("span", { html: inlineMd(e.ex) })]) : null
            ]));
          });
          browse.appendChild(g);
        });
      }

      function update() {
        hits = filtered();
        count.textContent = hits.length === D.length ? D.length + " words" : hits.length + " of " + D.length + " words";
        if (view.mode === "lookup") { drawList(); showDetail(); } else drawBrowse();
      }
      function applyView(remember) {
        page.classList.toggle("mode-lookup", view.mode === "lookup");
        browse.className = "dict-list view-" + (view.mode === "list" ? "list" : "cards") + " cols-" + view.cols;
        colWrap.hidden = view.mode === "lookup";
        if (remember) {
          dictView = view;
          saveView(view);
        }
        update();
      }
      input.addEventListener("input", function () { dictState.q = input.value; update(); });
      /* arrow up and down step through the words in the look-up view, also while typing in the search box */
      function handleKey(e) {
        if (view.mode !== "lookup" || (e.key !== "ArrowDown" && e.key !== "ArrowUp") || e.altKey || e.ctrlKey || e.metaKey) return;
        var ae = main.ownerDocument.activeElement;
        if (ae && (/^(TEXTAREA|SELECT)$/.test(ae.tagName) || (ae.tagName === "INPUT" && ae !== input))) return;
        if (!hits.length) return;
        var i = -1;
        hits.forEach(function (h, j) { if (termSlug(h.term) === dictState.sel) i = j; });
        var j = e.key === "ArrowDown" ? Math.min(hits.length - 1, i + 1) : Math.max(0, i - 1);
        e.preventDefault();
        if (j !== i) select(termSlug(hits[j].term));
      }
      catSel.addEventListener("change", function () { dictState.cat = catSel.value; drawTopics(); update(); });
      modeSel.addEventListener("change", function () { view.mode = modeSel.value; applyView(true); });
      colSel.addEventListener("change", function () { view.cols = colSel.value; applyView(true); });
      applyView();
      if (dictState.sel && view.mode === "lookup") browser.setTimeout(function () {
        if (page.isConnected) select(dictState.sel);
      }, 0);
      return handleKey;
    }
    return renderDict;
  }
