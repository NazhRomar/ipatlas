(function () {
  "use strict";

  const HISTORY_LIMIT = 20;
  const MAP_ZOOM = 10;

  const state = {
    requestId: 0, 
    history: [],
    selectedIp: null,
    current: null,
    map: null,
    marker: null,
  };

  const $ = (id) => document.getElementById(id);

  class ApiError extends Error {
    constructor(message, status, code) {
      super(message);
      this.status = status;
      this.code = code;
    }
  }

  async function api(path, options) {
    let resp;
    try {
      resp = await fetch(path, options);
    } catch (err) {
      throw new ApiError("Could not reach the IPAtlas server. Is it running?", 0, "network_error");
    }
    if (resp.status === 204) {
      return null;
    }
    let body = null;
    try {
      body = await resp.json();
    } catch (err) {
      body = null;
    }
    if (!resp.ok) {
      const info = body && body.error;
      throw new ApiError(
        (info && info.message) || "Request failed (HTTP " + resp.status + ").",
        resp.status,
        info && info.code
      );
    }
    return body;
  }

  function isNum(value) {
    return typeof value === "number" && Number.isFinite(value);
  }

  function text(id, value, fallback) {
    const empty = value === null || value === undefined || value === "";
    $(id).textContent = empty ? (fallback === undefined ? "—" : fallback) : String(value);
  }

  function formatTime(iso) {
    if (!iso) {
      return "—";
    }
    const d = new Date(iso);
    return Number.isNaN(d.getTime()) ? String(iso) : d.toLocaleString();
  }

  function localTimeIn(tz) {
    if (!tz) {
      return null;
    }
    try {
      return new Intl.DateTimeFormat(undefined, { timeZone: tz, hour: "numeric", minute: "2-digit" })
        .format(new Date());
    } catch (err) {
      return null; 
    }
  }

  async function copyText(button) {
    const value = button.dataset.value;
    if (!value) {
      return;
    }
    try {
      await navigator.clipboard.writeText(value);
      button.dataset.flash = "Copied";
    } catch (err) {
      button.dataset.flash = "Copy failed";
    }
    setTimeout(() => { delete button.dataset.flash; }, 1400);
  }

  function showBanner(message, kind) {
    const el = $("banner");
    el.textContent = message;
    el.className = "banner " + kind;
    el.hidden = false;
  }

  function hideBanner() {
    const el = $("banner");
    el.hidden = true;
    el.textContent = "";
  }

  function showError(err) {
    const status = err.status || 0;
    let message = err.message || "Something went wrong.";
    if (status === 404) {
      message = "That does not look like an IPv4 or IPv6 address.";
    }
    // Amber for user mistakes, red for upstream / server problems.
    const kind = status === 400 || status === 404 || status === 422 ? "warn" : "error";
    showBanner(message, kind);
  }

  function setAddress(family, address, failed) {
    const value = $("ipv" + family + "-value");
    const status = $("ipv" + family + "-status");
    const copy = $("copy-ipv" + family);
    if (address) {
      value.textContent = address;
      value.classList.remove("muted");
      status.textContent = "Detected";
      status.className = "status ok";
      copy.disabled = false;
      copy.dataset.value = address;
      return;
    }
    value.textContent = failed ? "Unavailable" : "Not detected";
    value.classList.add("muted");
    status.textContent = failed ? "Detection failed" : "Not detected on this network";
    status.className = "status " + (failed ? "bad" : "off");
    copy.disabled = true;
    delete copy.dataset.value;
  }

  function renderAddresses(ipv4, ipv6, failed) {
    setAddress("4", ipv4, failed);
    setAddress("6", ipv6, failed);
  }

  function initMap() {
    if (typeof window.L === "undefined") {
      showMapNote("Map library could not be loaded");
      return;
    }
    state.map = window.L.map("map", { worldCopyJump: true, fadeAnimation: false }).setView([20, 0], 2);
    window.L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 18,
      attribution: "&copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors",
    }).addTo(state.map);
  }

  function showMapNote(message) {
    const note = $("map-note");
    note.textContent = message;
    note.hidden = false;
  }

  function updateMap(loc) {
    if (!state.map) {
      return;
    }
    if (state.marker) {
      state.marker.remove();
      state.marker = null;
    }
    if (!(isNum(loc.latitude) && isNum(loc.longitude))) {
      showMapNote("No coordinates returned");
      return;
    }
    $("map-note").hidden = true;
    const popup = document.createElement("div");
    const title = document.createElement("strong");
    title.textContent = loc.ip;
    popup.appendChild(title);
    popup.appendChild(document.createElement("br"));
    popup.appendChild(document.createTextNode(
      [loc.city, loc.country].filter(Boolean).join(", ") || "Unknown location"
    ));
    state.marker = window.L.marker([loc.latitude, loc.longitude]).addTo(state.map).bindPopup(popup);
    state.map.setView([loc.latitude, loc.longitude], MAP_ZOOM);
    state.marker.openPopup();
  }

  function render(loc) {
    state.selectedIp = loc.ip;
    state.current = loc;

    text("r-ip", loc.ip);
    const badge = $("r-badge");
    badge.textContent = loc.version === 6 ? "IPv6" : "IPv4";
    badge.className = "ver-square " + (loc.version === 6 ? "v6" : "v4");
    badge.hidden = false;

    const copy = $("copy-result");
    copy.hidden = false;
    copy.dataset.value = loc.ip;

    text("r-place", loc.city || loc.country, "Unknown location");
    text("r-region", [loc.region, loc.country, loc.postal].filter(Boolean).join(" · "), "");
    const cc = $("r-cc");
    cc.textContent = loc.country_code || "";
    cc.hidden = !loc.country_code;

    text(
      "r-coords",
      isNum(loc.latitude) && isNum(loc.longitude)
        ? loc.latitude.toFixed(4) + ", " + loc.longitude.toFixed(4)
        : null,
      "No coordinates returned"
    );

    text("m-asn", loc.asn, "Unknown");
    text("m-org", loc.org);
    text("m-time", localTimeIn(loc.timezone));
    text("m-tz", loc.timezone, "Timezone unknown");
    text("m-cached", loc.cached ? "Cached" : "Live");
    text("m-fetched", (loc.source || "Unknown source") + " · " + formatTime(loc.fetched_at));

    updateMap(loc);
    markSelected();
  }

  function markSelected() {
    document.querySelectorAll("#history-list .history-item").forEach((btn) => {
      const item = state.history[Number(btn.dataset.index)];
      if (item && item.ip === state.selectedIp) {
        btn.setAttribute("aria-current", "true");
      } else {
        btn.removeAttribute("aria-current");
      }
    });
  }

  function renderHistory() {
    const list = $("history-list");
    list.textContent = "";
    text("history-count", String(state.history.length));
    $("clear-history").disabled = state.history.length === 0;

    if (state.history.length === 0) {
      const li = document.createElement("li");
      li.className = "history-empty";
      li.textContent = "No lookups yet.";
      list.appendChild(li);
      return;
    }

    state.history.forEach((item, index) => {
      const li = document.createElement("li");
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "history-item";
      btn.dataset.index = String(index);
      btn.title = "Looked up " + formatTime(item.fetched_at);

      const icon = document.createElement("span");
      icon.className = "hi-icon " + (item.version === 6 ? "v6" : "v4");
      icon.textContent = item.version === 6 ? "v6" : "v4";

      const body = document.createElement("span");
      body.className = "hi-text";
      const ip = document.createElement("span");
      ip.className = "hi-ip";
      ip.textContent = item.ip;
      const place = document.createElement("span");
      place.className = "hi-place";
      place.textContent = [item.city, item.country].filter(Boolean).join(", ") || "Unknown location";
      body.append(ip, place);

      btn.append(icon, body);
      li.appendChild(btn);
      list.appendChild(li);
    });
    markSelected();
  }

  async function loadHistory() {
    try {
      state.history = await api("/api/history?limit=" + HISTORY_LIMIT);
    } catch (err) {
      state.history = [];
      showError(err);
    }
    renderHistory();
  }

  async function loadMe() {
    const id = ++state.requestId;
    try {
      const data = await api("/api/lookup/me");
      if (id !== state.requestId) {
        return;
      }
      renderAddresses(data.ipv4, data.ipv6, false);
      render(data.location);
    } catch (err) {
      if (id !== state.requestId) {
        return;
      }
      showError(err);
      text("r-place", "No location yet");
      text("r-region", "Your own location could not be loaded. Look up an IP above to see where it is.");

      try {
        const addresses = await api("/api/myip");
        renderAddresses(addresses.ipv4, addresses.ipv6, false);
      } catch (err2) {
        renderAddresses(null, null, true);
      }
    }
    await loadHistory();
  }

  function setPending(pending) {
    const btn = $("lookup-btn");
    btn.disabled = pending;
    btn.textContent = pending ? "Looking…" : "Look up";
  }

  async function lookup(raw) {
    const ip = raw.trim();
    hideBanner();
    if (!ip) {
      showBanner("Enter an IPv4 or IPv6 address to look up.", "warn");
      return;
    }
    const id = ++state.requestId;
    setPending(true);
    try {
      const loc = await api("/api/lookup/" + encodeURIComponent(ip));
      if (id !== state.requestId) {
        return;
      }
      render(loc);
      await loadHistory();
    } catch (err) {
      if (id === state.requestId) {
        showError(err);
      }
    } finally {
      if (id === state.requestId) {
        setPending(false);
      }
    }
  }

  async function clearHistory() {
    try {
      await api("/api/history", { method: "DELETE" });
      state.history = [];
      renderHistory();
    } catch (err) {
      showError(err);
    }
  }

  function init() {
    initMap();

    $("lookup-form").addEventListener("submit", (event) => {
      event.preventDefault();
      lookup($("ip-input").value);
    });

    $("presets").addEventListener("click", (event) => {
      const chip = event.target.closest(".chip");
      if (chip) {
        $("ip-input").value = chip.dataset.ip;
        lookup(chip.dataset.ip);
      }
    });

    $("history-list").addEventListener("click", (event) => {
      const btn = event.target.closest(".history-item");
      const item = btn && state.history[Number(btn.dataset.index)];
      if (item) {
        hideBanner();
        render(item); 
      }
    });

    ["copy-ipv4", "copy-ipv6", "copy-result"].forEach((id) => {
      $(id).addEventListener("click", () => copyText($(id)));
    });

    $("clear-history").addEventListener("click", clearHistory);

    setInterval(() => {
      if (state.current) {
        text("m-time", localTimeIn(state.current.timezone));
      }
    }, 30000);

    loadMe();
  }

  document.addEventListener("DOMContentLoaded", init);
})();