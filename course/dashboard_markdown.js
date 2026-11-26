  function parseCourseMarkdown(md, el, parse, esc) {
    var box = el("div", { class: "prose" });
    if (parse) {
      box.innerHTML = parse(md);
    } else {
      box.innerHTML = '<p class="offline">The formatting library could not start. Showing the plain text.</p><pre>' + esc(md) + "</pre>";
    }
    return box;
  }

  function resolvePath(base, rel) {
    var parts = base.split("/").slice(0, -1);
    rel.split("/").forEach(function (seg) {
      if (seg === "..") parts.pop();
      else if (seg && seg !== ".") parts.push(seg);
    });
    return parts.join("/");
  }

  function rewriteMarkdownLinks(box, basePath, routeForPath, fileHref) {
    box.querySelectorAll("a[href]").forEach(function (a) {
      var h = a.getAttribute("href");
      if (/^[a-z]+:/i.test(h)) { a.target = "_blank"; a.rel = "noopener"; return; }
      if (h.charAt(0) === "#") return;
      var p = resolvePath(basePath, h.split("#")[0]);
      var route = routeForPath(p);
      if (route) a.setAttribute("href", "#" + route);
      else { a.setAttribute("href", fileHref(p)); a.target = "_blank"; a.rel = "noopener"; }
    });
  }

  function bindMarkdownChecklist(box, basePath, services) {
    var { isChecked, setChecked, showFailure } = services;
    // Checklists can be ticked off. "Done when" items share their state with the Progress page.
    var occurrences = new Map();
    box.querySelectorAll('input[type="checkbox"]').forEach(function (c) {
      var li = c.closest("li"), text = li ? li.cloneNode(true) : box.ownerDocument.createElement("span");
      text.querySelectorAll("ul,ol").forEach(function (child) { child.remove(); });
      var txt = text.textContent.replace(/\s+/g, " ").trim();
      var marker = text.innerHTML.match(/<!-- checklist:([a-z0-9-]+) -->/);
      var field = marker ? "done" : "ticks";
      var occurrence = occurrences.get(txt) || 0;
      if (!marker) occurrences.set(txt, occurrence + 1);
      var key = marker ? marker[1] : JSON.stringify([basePath, txt, occurrence]);
      c.disabled = false; c.checked = isChecked(field, key);
      if (txt) c.setAttribute("aria-label", txt);
      c.addEventListener("change", function () {
        if (setChecked(field, key, c.checked)) return;
        c.checked = isChecked(field, key);
        showFailure();
      });
      if (li) {
        li.classList.add("tick");
        li.addEventListener("click", function (ev) {
          if (ev.target === c || (ev.target.closest && (ev.target.closest("a, button") || ev.target.closest("li") !== li))) return;
          c.checked = !c.checked; c.dispatchEvent(new box.ownerDocument.defaultView.Event("change"));
        });
      }
    });
  }

  function formatCourseProse(box, services) {
    var { el, figureRatio, figureLauncher, copyBlock } = services;
    box.querySelectorAll("table").forEach(function (t) {
      var w = el("div", { class: "tablewrap" });
      t.parentNode.insertBefore(w, t); w.appendChild(t);
    });
    box.querySelectorAll("h3").forEach(function (h3) { if (/^(\d{4}|Around \d{4}|Late \d{4}s|Spring \d{4}|\d{1,2} \w+ \d{4}|\w+ \d{4}) · /.test(h3.textContent)) h3.classList.add("tl-event"); });
    box.querySelectorAll("p").forEach(function (p) { var f = p.firstElementChild; if (f && f.tagName === "EM" && /^(In the course|Source):$/.test(f.textContent.trim()) && p.textContent.indexOf(f.textContent) === 0) p.classList.add("tl-meta"); });
    var figNo = 0;
    box.querySelectorAll("p > img:only-child").forEach(function (img) {
      var p = img.parentNode;
      if (p.textContent.trim()) return;
      var fig = el("figure", { class: "fig" });
      var ratio = figureRatio(img.getAttribute("src"));
      if (ratio > 3.6) fig.classList.add("wide");
      p.parentNode.insertBefore(fig, p);
      fig.appendChild(figureLauncher(img));
      p.parentNode.removeChild(p);
      var next = fig.nextElementSibling;
      if (next && next.tagName === "P" && next.children.length === 1 && next.firstElementChild.tagName === "EM" &&
          next.textContent.trim() === next.firstElementChild.textContent.trim()) {
        figNo++;
        fig.appendChild(el("figcaption", { text: "Figure " + figNo + ". " + next.textContent.trim().replace(/^Figure\s+\d+\.\s*/, "") }));
        next.parentNode.removeChild(next);
      }
      /* float beside the text only if enough plain running text follows before the next block element */
      var chars = 0, sib = fig.nextElementSibling;
      while (sib && /^(P|UL|OL)$/.test(sib.tagName)) { chars += sib.textContent.length; sib = sib.nextElementSibling; }
      /* landscape figures use the full text width; only upright ones float beside the text */
      var asked = img.getAttribute("title") === "full";
      if (asked) img.removeAttribute("title");
      if (asked || ratio >= 1.6 || !ratio) fig.classList.add("full");
      else if (chars >= 650) fig.classList.add("float");
    });
    box.querySelectorAll("blockquote").forEach(function (bq) {
      var first = bq.querySelector("p > strong:first-child");
      if (first && /^AI-researched/i.test(first.textContent)) bq.classList.add("ai-note");
      if (first && /^So what (is|are) /i.test(first.textContent)) bq.classList.add("explainer");
      var lab = first ? first.textContent.trim() : "";
      var kind = /^In this chapter/i.test(lab) ? "opener" : /^In short/i.test(lab) ? "recap" :
                 /^Coffee/i.test(lab) ? "aside coffee" : /^(Tip|It.s okay|Side note|Good to know)/i.test(lab) ? "aside" :
                 /^Watch out/i.test(lab) ? "watch" : /^In practice/i.test(lab) ? "practice" : "";
      if (kind) { bq.classList.add("box"); kind.split(" ").forEach(function (k) { bq.classList.add(k); }); }
    });
    /* a copy button on every code block, so prompts and code can be reused in one click */
    box.querySelectorAll("pre").forEach(function (pre) {
      var wrap = el("div", { class: "codewrap" });
      pre.parentNode.insertBefore(wrap, pre); wrap.appendChild(pre);
      var btn = el("button", { class: "copybtn", type: "button", text: "Copy", "aria-label": "Copy this block" });
      btn.addEventListener("click", function () { copyBlock(pre, btn); });
      wrap.appendChild(btn);
    });
    box.querySelectorAll("details.think > summary").forEach(function (sm) {
      if (sm.firstChild && sm.firstChild.nodeType === 3) sm.firstChild.nodeValue = sm.firstChild.nodeValue.replace(/^\s*Pause and think:\s*/i, "").replace(/^./, function (c) { return c.toUpperCase(); });
    });
    var doc = box.ownerDocument;
    var cw = doc.createTreeWalker(box, doc.defaultView.NodeFilter.SHOW_COMMENT), comments = [];
    while (cw.nextNode()) comments.push(cw.currentNode);
    comments.forEach(function (c) {
      var t = c.data.trim();
      if (t.indexOf("speak:") === 0) {
        var prev = c.previousSibling;
        while (prev && prev.nodeType !== 1) prev = prev.previousSibling;
        var target = prev && prev.classList && prev.classList.contains("tablewrap") ? prev.querySelector("table") : prev;
        if (target) target.setAttribute("data-speak", t.slice(6).trim());
      }
      else if (t.indexOf("part:") === 0) {   /* <!-- part: Name --> groups the sections that follow */
        c.parentNode.insertBefore(el("p", { class: "partmark", text: t.slice(5).trim() }), c);
      }
      c.parentNode.removeChild(c);
    });
  }
