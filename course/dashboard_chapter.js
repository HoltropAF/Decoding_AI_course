  /* Split a rendered document into sections at each H2. Returns null for short documents. */
  function makeSections(prose, force, el) {
    var kids = Array.prototype.slice.call(prose.children);
    var h2s = kids.filter(function (k) { return k.tagName === "H2"; }).length;
    var words = prose.textContent.split(/\s+/).length;
    if (h2s < 2 || (!force && (h2s < 4 || words < 700))) return null;
    var secs = [], cur = { title: "Introduction", nodes: [] }, part = null;
    kids.forEach(function (k) {
      if (k.classList && k.classList.contains("partmark")) { part = k.textContent; return; }
      if (k.tagName === "H2") { if (cur.nodes.length) secs.push(cur); cur = { title: k.textContent.trim(), nodes: [k], part: part }; part = null; }
      else cur.nodes.push(k);
    });
    secs.push(cur);
    secs.forEach(function (sct) {
      while (sct.nodes.length && sct.nodes[sct.nodes.length - 1].tagName === "HR") sct.nodes.pop();
    });
    if (secs.length > 1 && secs[0].title === "Introduction") {
      var meaningful = secs[0].nodes.filter(function (n) { return !/^(H1|HR)$/.test(n.tagName); }).length;
      if (!meaningful) secs[0].nodes = secs[0].nodes.filter(function (n) { return n.tagName !== "HR"; });
    }
    prose.textContent = "";
    prose.classList.add("paged");
    secs.forEach(function (sct) {
      sct.el = el("section", { class: "docsec" });
      sct.nodes.forEach(function (n) { sct.el.appendChild(n); });
      sct.words = sct.el.textContent.split(/\s+/).length;
      sct.short = sct.title.replace(/^\d+\.\s*/, "");
      prose.appendChild(sct.el);
    });
    return secs;
  }

  function renderChapter(container, d, options, services) {
    var { slots, openIndex, touchOnly, linkable, onOpen, makeNoteEditor } = options;
    var { el, renderMd, linkTerms, makeReader, readableBlocks, docHeader, partIcon, scrollBehavior } = services;
    var browser = container.ownerDocument.defaultView;
    var prose = renderMd(d.md, d.path, true);
    var secs = makeSections(prose, d.parts, el);
    var nowPart;
    var toolsTo = slots ? slots.tools : container;

    if (!secs) {
      if (linkable) linkTerms(prose);
      toolsTo.appendChild(makeReader(function () { return readableBlocks(prose); }, { root: prose, compact: !!slots }));
      container.appendChild(prose);
      container.appendChild(docHeader(d));
      return [];
    }
    if (linkable) secs.forEach(function (sct) { linkTerms(sct.el); });

    /* One page, every H2 section folds open and closed. */
    var key = d.path;
    var parts = [];
    prose.classList.remove("paged");
    prose.classList.add("collapsible");
    secs.forEach(function (sct, j) {
      var h2 = sct.el.querySelector(":scope > h2");
      if (!h2) { sct.el.classList.add("intro"); return; }        // introduction: always visible
      var body = el("div", { class: "secbody" });
      var nodes = Array.prototype.slice.call(sct.el.childNodes).filter(function (nd) { return nd !== h2; });
      nodes.forEach(function (nd) { body.appendChild(nd); });
      var mins = el("span", { class: "mins", text: "~" + Math.max(1, Math.round(sct.words / 200)) + " min" });
      var icon = el("span", { class: "secicon", "aria-hidden": "true" }); icon.innerHTML = partIcon(parts.length);
      var head = el("div", { class: "sechead", role: "button", tabindex: "0" }, [el("span", { class: "chev", "aria-hidden": "true", text: "\u203a" }), icon, h2, mins]);
      sct.el.textContent = "";
      sct.el.appendChild(head);
      sct.el.appendChild(body);
      var id = key + "#" + j;
      var part = { el: sct.el, head: head, body: body, id: id, title: h2.textContent.trim(), partLabel: sct.part || null, mins: Math.max(1, Math.round(sct.words / 200)) };
      if (sct.part) prose.insertBefore(el("div", { class: "partlabel", text: sct.part }), sct.el);
      part.set = function (open) {
        sct.el.classList.toggle("open", open);
        if (open && nowPart) { nowPart.innerHTML = "Reading: <b></b>"; nowPart.querySelector("b").textContent = part.title; }
        if (open && onOpen) onOpen(parts.indexOf(part), part.title);
        if (part.sideLink) part.sideLink.classList.toggle("active", open);
        body.hidden = !open;
        head.setAttribute("aria-expanded", open ? "true" : "false");
      };
      part.set(false);   /* every section starts closed whenever the page is opened */
      function toggle() { if (body.hidden) openOnly(part, true); else part.set(false); }
      head.addEventListener("click", toggle);
      head.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); e.stopPropagation(); toggle(); } });
      part.open = function () { openOnly(part, true); };
      parts.push(part);
    });
    if (touchOnly) {
      var sx = null, sy = null;
      prose.addEventListener("touchstart", function (e) {
        if (e.touches.length !== 1 || e.target.closest("table, pre, .tablewrap, figure, input, textarea")) { sx = null; return; }
        sx = e.touches[0].clientX; sy = e.touches[0].clientY;
      }, { passive: true });
      prose.addEventListener("touchend", function (e) {
        if (sx === null) return;
        var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy; sx = null;
        if (Math.abs(dx) < 90 || Math.abs(dy) > 45) return;
        var cur = parts.filter(function (pt) { return !pt.body.hidden; })[0];
        var k = cur ? parts.indexOf(cur) : -1;
        var to = dx < 0 ? parts[k + 1] : parts[k - 1];
        if (to) openOnly(to, true);
      }, { passive: true });
    }
    parts.forEach(function (pt, k) {
      var nx = parts[k + 1];
      if (!nx) return;
      var b = el("button", { class: "btn primary", type: "button", text: "Next: " + nx.title + " \u2192" });
      b.addEventListener("click", function () { openOnly(nx, true); });
      pt.body.appendChild(el("div", { class: "nextpart" }, [b]));
    });
    function scrollToPart(part, behavior) {
      var banner = slots && slots.banner;
      var offset = banner && browser.getComputedStyle(banner).position === "sticky" ? banner.getBoundingClientRect().height + 16 : 16;
      var y = Math.max(0, part.head.getBoundingClientRect().top + browser.scrollY - offset);
      try { browser.scrollTo({ top: y, behavior: behavior }); } catch (error) { browser.scrollTo(0, y); }
    }
    if (openIndex !== null && openIndex !== undefined && parts[openIndex]) {
      browser.setTimeout(function () {
        if (!prose.isConnected) return;
        var target = parts[openIndex];
        openOnly(target, false);
        scrollToPart(target, "auto");
      }, 120);
    }
    var total = secs.reduce(function (acc, sct) { return acc + sct.words; }, 0);
    /* accordion: opening one section closes the others */
    function openOnly(target, scroll) {
      parts.forEach(function (pt) { if (pt !== target) pt.set(false); });
      target.set(true);
      if (scroll) scrollToPart(target, scrollBehavior());
    }
    var secbar = el("div", { class: "secbar" }, [
      el("span", { class: "where", text: parts.length + " sections \u00b7 ~" + Math.max(1, Math.round(total / 200)) + " min \u00b7 click a title to open it" })
    ]);

    var reader = makeReader(function () { return readableBlocks(prose); }, {
      root: prose, compact: !!slots,
      startAt: function () {
        var open = parts.filter(function (pt) { return !pt.body.hidden; })[0];
        return open ? open.head.querySelector("h2") : null;
      },
      onBlock: function (blockEl) {
        parts.forEach(function (pt) { if (pt.el.contains(blockEl) && pt.body.hidden) openOnly(pt, false); });
      }
    });

    (slots ? slots.secs : container).appendChild(secbar);
    if (slots) { nowPart = el("span", { class: "nowpart" }); slots.secs.appendChild(nowPart); }
    if (slots && makeNoteEditor) {
      var npanel = el("div", { class: "notepanel", hidden: "hidden" }, [
        makeNoteEditor(),
        el("a", { class: "allnotes", href: "#notes", text: "All my notes \u2192" })
      ]);
      var nbtn = el("button", { class: "btn notebtn", type: "button", "aria-expanded": "false", text: "\u270e Notes" });
      nbtn.addEventListener("click", function () {
        var open = npanel.hidden;
        npanel.hidden = !open; nbtn.setAttribute("aria-expanded", open ? "true" : "false");
        if (open) { var ta = npanel.querySelector("textarea"); if (ta) ta.focus(); }
      });
      toolsTo.appendChild(nbtn);
      slots.banner.appendChild(npanel);
    }
    toolsTo.appendChild(reader);

    container.appendChild(prose);
    container.appendChild(docHeader(d));
    return parts;
  }
