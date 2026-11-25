  function renderWrapUp(container, model, services) {
    var { el, isChecked, setChecked, readNote, editNote, addNote, refreshNavigation, showMessage, noteEditor, noteBody } = services;
    var total = model.items.length;
    var completion = el("div", { class: "donecard" }, [
      el("div", {}, [el("h3", { text: "\u2713 You finished " + model.label + "!" }),
        el("p", { text: "Nicely done. Tell a colleague one thing you learned, and come back to the Dictionary whenever a word slips your mind." })]),
      el("a", { class: "btn primary", href: model.next.href, text: model.next.text })
    ]);
    var page = el("div", { class: "card prose wrapup" });
    page.appendChild(el("h2", { text: "Wrap-up" }));
    page.appendChild(el("p", { text: "Before you move on: tick off what you've done, read back what you saved while reading, and write down anything you want to remember or bring to the group session. Everything stays in this browser." }));

    /* 1. done when */
    page.appendChild(el("h3", { text: "Done when" }));
    var fill = el("span");
    var count = el("span", { class: "muted", role: "status" });
    page.appendChild(el("div", { class: "wu-count" }, [el("div", { class: "wu-bar" }, [fill]), count]));
    var list = el("div", { class: "wu-checks" });
    function updateChecklist() {
      var done = model.items.filter(function (item) { return isChecked(item.id); }).length;
      fill.style.width = (total ? Math.round(100 * done / total) : 0) + "%";
      count.textContent = done + " of " + total + " done";
      if (total && done === total) container.insertBefore(completion, page);
      else completion.remove();
    }
    model.items.forEach(function (item) {
      var key = item.id, id = "chk-" + key;
      var input = el("input", { type: "checkbox", id: id });
      var label = el("label", { class: "check", for: id }, [input, el("span", { text: item.text })]);
      input.checked = isChecked(key);
      label.classList.toggle("on", input.checked);
      input.addEventListener("change", function () {
        if (!setChecked(key, input.checked)) {
          input.checked = isChecked(key);
          showMessage("Couldn't save this checklist change. Try again.");
          return;
        }
        label.classList.toggle("on", input.checked);
        updateChecklist();
        refreshNavigation();
      });
      list.appendChild(label);
    });
    page.appendChild(list);

    /* 2. notes from this chapter */
    page.appendChild(el("h3", { text: "Your notes from this chapter" }));
    var view = el("div", { class: "wu-notes" });
    var editBox = el("div", { class: "wu-edit", hidden: "hidden" });
    function paint() {
      view.textContent = "";
      var v = readNote().trim();
      if (v) view.appendChild(noteBody(v));
      else view.appendChild(el("p", { class: "nc-empty", text: "Nothing saved yet. While you read, select a sentence and choose \u201cSave to my notes\u201d, or use the \u270e Notes button; it all shows up here." }));
    }
    paint();
    var editBtn = el("button", { class: "btn small", type: "button", text: "\u270e Edit these notes" });
    editBtn.addEventListener("click", function () {
      var opening = editBox.hidden;
      if (opening) { editBox.textContent = ""; editBox.appendChild(noteEditor("Your notes for " + model.label, readNote(), editNote, "No unpublished results or patient information here, please.")); }
      editBox.hidden = !opening; view.hidden = opening;
      editBtn.textContent = opening ? "\u2713 Done" : "\u270e Edit these notes";
      if (!opening) { paint(); refreshNavigation(); }
      else { var ta = editBox.querySelector("textarea"); if (ta) ta.focus(); }
    });
    page.appendChild(view);
    page.appendChild(editBox);
    page.appendChild(el("div", { class: "wu-tools" }, [editBtn, el("a", { href: model.notesHref, text: "All my notes \u2192" })]));

    /* 3. add a note */
    page.appendChild(el("h3", { text: "Anything to add?" }));
    if (model.question) page.appendChild(el("p", { class: "wu-question" }, [el("span", { class: "label", text: "Something to think about" }), el("span", { text: model.question })]));
    var ta = el("textarea", { class: "wu-new", "aria-label": "Add a note", placeholder: "A question for the group, something to try in your own work, what you'd tell a colleague\u2026" });
    var add = el("button", { class: "btn primary", type: "button", text: "Add to my notes" });
    var status = el("span", { class: "muted", role: "status", "aria-live": "polite" });
    add.addEventListener("click", function () {
      var v = ta.value.trim(); if (!v) { ta.focus(); return; }
      if (!addNote(v)) {
        status.textContent = "Couldn't save in this browser. Retry or copy your draft.";
        ta.focus();
        return;
      }
      ta.value = ""; paint(); refreshNavigation();
      status.textContent = "Added."; setTimeout(function () { status.textContent = ""; }, 1800);
    });
    page.appendChild(ta);
    page.appendChild(el("div", { class: "wu-tools" }, [add, status]));
    page.appendChild(el("p", { class: "muted wu-foot", text: "No unpublished results or patient information in your notes, please." }));
    container.appendChild(page);
    updateChecklist();
  }
