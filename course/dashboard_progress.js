  function createProgressStore(storage, key) {
    var core = ["done", "conf", "visited", "notes", "exp", "slide", "sub"];
    var flags = ["done", "ticks", "visited", "readParts"];
    var readingDefaults = { readbar: true, ticks: true, mins: true };
    var speechDefaults = { rate: 1, voice: "", auto: false };

    function isRecord(value) {
      return value !== null && typeof value === "object" && !Array.isArray(value);
    }

    function normalize(raw, strict) {
      if (strict && (!isRecord(raw) || core.some(function (field) { return !isRecord(raw[field]); }))) {
        throw new Error("Invalid progress backup");
      }
      if (!isRecord(raw)) raw = {};
      function map(field, valid) {
        var entries = isRecord(raw[field]) ? Object.entries(raw[field]) : [];
        var usable = entries.filter(function (entry) { return valid(entry[1]); });
        if (strict && raw[field] !== undefined && (!isRecord(raw[field]) || usable.length !== entries.length)) {
          throw new Error("Invalid progress field: " + field);
        }
        return Object.assign(Object.create(null), Object.fromEntries(usable.filter(function (entry) {
          return entry[0] !== "__proto__" && entry[0] !== "constructor" && entry[0] !== "prototype";
        })));
      }
      function index(value) { return Number.isInteger(value) && value >= 0; }
      function rating(value) { return value === undefined || Number.isInteger(value) && value >= 1 && value <= 5; }
      var state = {
        conf: map("conf", function (value) { return isRecord(value) && rating(value.pre) && rating(value.post); }),
        notes: map("notes", function (value) { return typeof value === "string"; }),
        exp: map("exp", function () { return true; }),
        slide: map("slide", function (value) { return index(value) || typeof value === "boolean"; }),
        sub: map("sub", index),
        last: typeof raw.last === "string" ? raw.last : null,
        lastTitle: typeof raw.lastTitle === "string" ? raw.lastTitle : "",
        fs: ["s", "m", "l"].includes(raw.fs) ? raw.fs : "m",
        zoom: [0.75, 0.9, 1].includes(raw.zoom) ? raw.zoom : 0.75,
        prefs: Object.assign({}, readingDefaults),
        tts: Object.assign({}, speechDefaults)
      };
      flags.forEach(function (field) { state[field] = map(field, function (value) { return typeof value === "boolean"; }); });
      Object.keys(readingDefaults).forEach(function (field) {
        if (isRecord(raw.prefs) && typeof raw.prefs[field] === "boolean") state.prefs[field] = raw.prefs[field];
      });
      if (isRecord(raw.tts)) {
        if (typeof raw.tts.rate === "number" && raw.tts.rate >= 0.8 && raw.tts.rate <= 2.5) state.tts.rate = raw.tts.rate;
        if (typeof raw.tts.voice === "string") state.tts.voice = raw.tts.voice;
        if (typeof raw.tts.auto === "boolean") state.tts.auto = raw.tts.auto;
      }
      return state;
    }

    function save(state) {
      try { storage().setItem(key, JSON.stringify(state)); return true; }
      catch (error) { return false; }
    }

    return {
      load: function () {
        try { return normalize(JSON.parse(storage().getItem(key)), false); }
        catch (error) { return normalize({}, false); }
      },
      save: save,
      restore: function (text) {
        var candidate;
        try { candidate = normalize(JSON.parse(text), true); }
        catch (error) { return { error: "invalid" }; }
        return save(candidate) ? { state: candidate } : { error: "storage" };
      },
      reset: function (state) {
        var candidate = normalize({ fs: state.fs, zoom: state.zoom, prefs: state.prefs, tts: state.tts }, false);
        return save(candidate) ? candidate : null;
      }
    };
  }
