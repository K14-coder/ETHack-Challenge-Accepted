/* app.js — state, controls, and wiring.
 *
 * One rule governs the interaction: every control on the left changes a number
 * on the right immediately, and nothing is recomputed on a server. The pillar
 * cube is in memory, the last three steps cost microseconds, so the ranking
 * really does reorder while the thumb is still moving. That responsiveness is
 * the argument: a score you can visibly move with a switch is a choice.
 */
(function () {
  "use strict";

  var PILLAR_NAME = { E: "Environment", S: "Social", G: "Governance", F: "Finance" };

  var AXIS_COPY = {
    base: { label: "Exposure base", help:
      "Per what unit of exposure. For a quantity this divides: EBITDA, equity, or barrels produced. For a rate it selects the population the reporter already divided by; for agency leverage it selects the agency. Production exists for the nine producers only." },
    window: { label: "Window", help:
      "Latest takes each company's most recent reported year, so a company that has published FY2025 is compared with one that has not. Fiscal year holds everyone to the last complete year. Bloomberg ships both as separate products (B p.34)." },
    direction: { label: "Direction", help:
      "Where the company stands, or how far it has moved. The financial pillar is one fiscal year, so under change it has no trajectory and drops out." },
    polarity: { label: "Polarity", help:
      "For 15 fields the two defensible conventions disagree about which way is better. Long CEO tenure is entrenchment or it is experience. Orthodox takes the governance reading, stability the continuity reading, neutral scores them 50 and lets them decide nothing." },
    normalizer: { label: "Normaliser", help:
      "How a raw value becomes a grade. MSCI normalises against percentile benchmarks. Bloomberg rejects percentiles in print and fits log(impact) = log(intensity) + g·log(activity), scoring the residual — that is the elasticity option (B pp.41, 45–46)." },
    peerset: { label: "Peer set", help:
      "Bloomberg's five BECS peer groups, the producers/downstream split, or all eighteen. A group below three members is graded against the sector, because two members can only ever return 0 and 100." },
    inclusion: { label: "Evidence bar", help:
      "How demanding the model is about what counts. A field must be reported by this share of the peer set, and a policy flag must clear this substantive tier. At the strict end the Social pillar has no fields left at sector level — which is the finding, not a bug." },
    missing: { label: "Missing data", help:
      "Excluded drops the field and redistributes the weights, which is Bloomberg's sub-issue rule. Worst case grades the silence zero. Capped drops it, then limits the pillar by its own disclosure: 30 + √DF × 70, which is Bloomberg's Issue Score (B p.26)." },
    aggregator: { label: "Aggregation", help:
      "MSCI takes a weighted arithmetic mean. Bloomberg uses a shifted power mean at every level, holding that E, S, G and F cannot compensate for one another. The geometric mean is the strict end of the same family." }
  };

  var OPTION_COPY = {
    ebitda: "EBITDA", equity: "equity", production: "output",
    latest: "latest", fy_common: "fiscal year", mean3: "3-year mean",
    level: "level", change: "change",
    orthodox: "orthodox", neutral: "neutral", stability: "stability",
    percentile: "percentile", winsor: "winsorised", log: "log min–max",
    elasticity: "elasticity",
    subgroup: "BECS group", chain: "producers", sector: "all 18",
    permissive: "permissive", majority: "majority", strict: "strict",
    exclude: "excluded", worst: "worst case", cap: "capped",
    arithmetic: "arithmetic", pmean05: "power p=½", geometric: "geometric"
  };

  var PRESET_COPY = {
    equal: "Equal", env_led: "Environment-led", social_led: "Social-led",
    gov_led: "Governance-led", finance_led: "Finance-led"
  };

  var data, M, state, els = {}, lastResult = null, heavyTimer = null;
  var inspectedSpec = null;
  var rowPositions = {}, tbodyTop = null;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ------------------------------------------------------------------ state */

  function defaultState() {
    var raw = {};
    M.pillars.forEach(function (p) { raw[p] = 100 / M.pillars.length; });
    var axes = {};
    M.order.forEach(function (a) { axes[a] = "all"; });
    return { raw: raw, axes: axes, selected: 0 };
  }

  function weights() {
    var t = 0;
    M.pillars.forEach(function (p) { t += state.raw[p]; });
    if (t <= 0) return M.pillars.map(function () { return 1 / M.pillars.length; });
    return M.pillars.map(function (p) { return state.raw[p] / t; });
  }

  /* The four weights are a point on a simplex, so moving one has to move the
   * others — and the thumbs have to move with it, or the control lies about
   * what it is doing. The remainder is redistributed in proportion to where the
   * other three already sat, which is the least surprising rule: it preserves
   * their relative balance and only changes the share this pillar takes. */
  function setWeight(p, v) {
    v = Math.max(0, Math.min(100, v));
    var others = M.pillars.filter(function (q) { return q !== p; });
    var rest = 100 - v;
    var sum = 0;
    others.forEach(function (q) { sum += state.raw[q]; });
    if (sum <= 1e-9) {
      others.forEach(function (q) { state.raw[q] = rest / others.length; });
    } else {
      others.forEach(function (q) { state.raw[q] = (state.raw[q] * rest) / sum; });
    }
    state.raw[p] = v;
    syncWeightUI(p);
  }

  function syncWeightUI(skip) {
    M.pillars.forEach(function (q) {
      var el = document.getElementById("w-" + q);
      if (q !== skip) el.value = state.raw[q];
      document.getElementById("wo-" + q).textContent = Math.round(state.raw[q]) + "%";
    });
  }

  /* ------------------------------------------------------------------ build */

  function buildControls() {
    M.pillars.forEach(function (p) {
      var row = document.createElement("div");
      row.className = "wrow";
      row.innerHTML =
        '<label for="w-' + p + '"><i class="swatch swatch-' + p + '"></i>' +
        PILLAR_NAME[p] + ' <em>' + data.meta.field_counts[p] + '</em></label>' +
        '<output id="wo-' + p + '"></output>' +
        '<input type="range" id="w-' + p + '" min="0" max="100" step="1" value="' +
        state.raw[p] + '" aria-label="' + PILLAR_NAME[p] + ' weight">';
      els.weights.appendChild(row);
      var input = row.querySelector("input");
      input.addEventListener("input", function () {
        setWeight(p, +input.value);
        clearPresets();
        render({ light: true });
      });
      input.addEventListener("change", function () { render(); });
    });

    Object.keys(data.meta.presets).forEach(function (k, i) {
      var w = data.meta.presets[k];
      var b = document.createElement("button");
      b.type = "button";
      b.className = "chip";
      b.textContent = PRESET_COPY[k] || k;
      b.setAttribute("aria-pressed", i === 0 ? "true" : "false");
      b.addEventListener("click", function () {
        M.pillars.forEach(function (p) { state.raw[p] = (w[p] || 0) * 100; });
        syncWeightUI();
        clearPresets();
        b.setAttribute("aria-pressed", "true");
        render();
      });
      els.presets.appendChild(b);
    });

    M.order.forEach(function (axis) {
      var copy = AXIS_COPY[axis] || { label: axis, help: "" };
      var block = document.createElement("div");
      block.className = "axis";
      block.innerHTML =
        '<div class="axis-head"><span>' + copy.label + "</span>" +
        '<button type="button" class="info" aria-label="What this choice means" ' +
        'data-tip="' + copy.help.replace(/"/g, "&quot;") + '">?</button></div>';
      var seg = document.createElement("div");
      seg.className = "seg";
      seg.setAttribute("role", "group");
      seg.setAttribute("aria-label", copy.label);
      ["all"].concat(M.opts[axis]).forEach(function (o) {
        var b = document.createElement("button");
        b.type = "button";
        b.textContent = o === "all" ? "vary" : (OPTION_COPY[o] || o);
        b.setAttribute("aria-pressed", state.axes[axis] === o ? "true" : "false");
        b.addEventListener("click", function () {
          state.axes[axis] = o;
          seg.querySelectorAll("button").forEach(function (x) {
            x.setAttribute("aria-pressed", "false");
          });
          b.setAttribute("aria-pressed", "true");
          render();
        });
        seg.appendChild(b);
      });
      block.appendChild(seg);
      els.axes.appendChild(block);
    });

    els.reset.addEventListener("click", function () {
      state = defaultState();
      syncControls();
      render();
    });
  }

  function clearPresets() {
    els.presets.querySelectorAll("button").forEach(function (b) {
      b.setAttribute("aria-pressed", "false");
    });
  }

  function syncControls() {
    syncWeightUI();
    clearPresets();
    var first = els.presets.querySelector("button");
    if (first) first.setAttribute("aria-pressed", "true");
    els.axes.querySelectorAll(".seg").forEach(function (seg) {
      seg.querySelectorAll("button").forEach(function (b, j) {
        b.setAttribute("aria-pressed", j === 0 ? "true" : "false");
      });
    });
  }

  /* ------------------------------------------------------------------ table */

  function captureRows() {
    rowPositions = {};
    tbodyTop = els.tbody.getBoundingClientRect().top;
    els.tbody.querySelectorAll("tr").forEach(function (tr) {
      rowPositions[tr.dataset.company] = tr.getBoundingClientRect().top;
    });
  }

  function flipRows() {
    if (reduceMotion || !els.tbody.animate) return;
    if (tbodyTop === null ||
        Math.abs(els.tbody.getBoundingClientRect().top - tbodyTop) > 0.5) return;
    els.tbody.querySelectorAll("tr").forEach(function (tr) {
      var prev = rowPositions[tr.dataset.company];
      if (prev === undefined) return;
      var delta = prev - tr.getBoundingClientRect().top;
      if (Math.abs(delta) < 0.5) return;
      tr.getAnimations().forEach(function (a) { a.cancel(); });
      tr.animate([{ transform: "translateY(" + delta + "px)" }, { transform: "none" }],
                 { duration: 300, easing: "cubic-bezier(.22,1,.36,1)" });
    });
  }

  function renderTable(res, dec) {
    var order = res.companies.slice().sort(function (a, b) {
      if (!isFinite(a.consensus)) return 1;
      if (!isFinite(b.consensus)) return -1;
      return b.consensus - a.consensus || a.spread - b.spread;
    });
    captureRows();

    var existing = {};
    els.tbody.querySelectorAll("tr").forEach(function (tr) {
      existing[tr.dataset.company] = tr;
    });
    var byIndex = {};
    (dec || []).forEach(function (d) { byIndex[d.index] = d; });

    var frag = document.createDocumentFragment();
    order.forEach(function (c, i) {
      var tr = existing[c.index];
      if (!tr) {
        tr = document.createElement("tr");
        tr.dataset.company = c.index;
        tr.tabIndex = 0;
        tr.innerHTML =
          '<td class="c-pos"></td>' +
          '<td class="c-name"><b></b><span class="grp"></span></td>' +
          '<td class="c-num c-consensus"></td>' +
          '<td class="c-bar"><svg preserveAspectRatio="none" aria-hidden="true"></svg></td>' +
          '<td class="c-num c-spread"></td>' +
          '<td class="c-verdict"><span class="pill"></span></td>' +
          '<td class="c-pivot"></td>' +
          '<td class="c-num c-cov"></td>';
        tr.addEventListener("click", function () { select(c.index); });
        tr.addEventListener("keydown", function (e) {
          if (e.key === "Enter" || e.key === " ") { e.preventDefault(); select(c.index); }
        });
      }
      tr.classList.toggle("is-selected", c.index === state.selected);
      if (c.index === state.selected) tr.setAttribute("aria-current", "true");
      else tr.removeAttribute("aria-current");

      tr.querySelector(".c-pos").textContent = i + 1;
      tr.querySelector(".c-name b").textContent = c.name;
      tr.querySelector(".c-name .grp").textContent = shortPeer(c.peers.subgroup);
      tr.querySelector(".c-consensus").textContent =
        isFinite(c.consensus) ? c.consensus.toFixed(0) : "—";
      tr.querySelector(".c-spread").textContent =
        isFinite(c.positions) ? c.positions.toFixed(1) : "—";
      tr.querySelector(".c-cov").textContent = c.coverage.toFixed(0) + "%";

      var v = Charts.distributionBar(tr.querySelector(".c-bar svg"), c,
                                     { width: 240, height: 28, step: M.step });
      var pill = tr.querySelector(".pill");
      pill.textContent = v.label;
      pill.className = "pill " + v.cls;

      var d = byIndex[c.index];
      tr.querySelector(".c-pivot").textContent =
        d && d.pivot ? (AXIS_COPY[d.pivot] || { label: d.pivot }).label.toLowerCase() : "—";

      frag.appendChild(tr);
    });
    els.tbody.appendChild(frag);
    flipRows();
  }

  function shortPeer(p) {
    return String(p).replace("Exploration & Production", "E&P")
      .replace("Oilfield Services & Equipment", "Services")
      .replace("Refining & Marketing", "Refining")
      .replace("Integrated Oils", "Integrated");
  }

  /* ----------------------------------------------------------------- detail */

  function describeSpec(s) {
    return M.order.map(function (a, i) {
      return OPTION_COPY[M.opts[a][M.level(s, i)]] || M.opts[a][M.level(s, i)];
    }).join(" · ");
  }

  function renderDetail(res, dec) {
    var c = res.companies[state.selected];
    var w = weights();
    els.detailName.textContent = c.name;
    els.detailGroup.textContent =
      shortPeer(c.peers.subgroup) + " · " + c.coverage.toFixed(0) +
      "% of the " + data.meta.n_fields + " fields reported";

    // best and worst specification for this company
    var best = null, worst = null;
    for (var k = 0; k < res.nSpec; k++) {
      var v = res.R[k * M.nC + state.selected];
      if (v !== v) continue;
      if (!best || v > best.v) best = { v: v, s: res.specIds[k] };
      if (!worst || v < worst.v) worst = { v: v, s: res.specIds[k] };
    }
    specCard(els.bestSpec, best, "Its best case");
    specCard(els.worstSpec, worst, "Its worst case");
    els.swing.textContent = best && worst
      ? ((best.v - worst.v) / M.step).toFixed(1) : "—";

    // pillar scores under the first specification in view
    var s0 = res.specIds[0], base = (s0 * M.nC + state.selected) * M.nP;
    var scores = {}, num = 0, den = 0;
    M.pillars.forEach(function (p, i) {
      var v = M.P[base + i];
      scores[p] = v;
      if (v === v && w[i] > 0) { num += w[i] * v; den += w[i]; }
    });
    Charts.pillarBars(els.pillars, scores, w, M.pillars,
                      den > 0 ? num / den : NaN, PILLAR_NAME);
    var ev = data.evidence[M.opts.peerset[M.level(s0, M.order.indexOf("peerset"))] +
                           "|" + M.opts.inclusion[M.level(s0, M.order.indexOf("inclusion"))]];
    var exp = data.expected[M.opts.peerset[M.level(s0, M.order.indexOf("peerset"))] +
                            "|" + M.opts.inclusion[M.level(s0, M.order.indexOf("inclusion"))]];
    els.pillarNote.textContent = ev
      ? "Fields behind each pillar under this specification: " +
        M.pillars.map(function (p, i) {
          return p + " " + ev[state.selected][i] + "/" + exp[state.selected][i];
        }).join(", ") + "."
      : "";

    // the decomposition
    var d = (dec || []).filter(function (x) { return x.index === state.selected; })[0];
    Charts.pivotBars(els.pivot, d, AXIS_COPY);
    els.pivotNote.textContent = d && d.explained
      ? "Main effects account for " + d.explained.toFixed(0) +
        "% of the movement in this company's rank. The remainder is interaction " +
        "between the axes — choices that only matter in combination."
      : "";
  }

  function specCard(node, entry, title) {
    if (!entry) { node.innerHTML = "<h4>" + title + "</h4><p>—</p>"; return; }
    node.innerHTML =
      "<h4>" + title + ' <span class="spec-rank">' + entry.v.toFixed(0) + "</span></h4>" +
      "<dl>" + M.order.map(function (a, i) {
        var o = M.opts[a][M.level(entry.s, i)];
        return "<div><dt>" + (AXIS_COPY[a] || { label: a }).label + "</dt><dd>" +
               (OPTION_COPY[o] || o) + "</dd></div>";
      }).join("") + "</dl>";
  }

  /* ------------------------------------------------------------------ header */

  function renderHeadline(res, dom) {
    var finite = res.companies.filter(function (c) { return isFinite(c.consensus); });
    var pos = finite.map(function (c) { return c.positions; })
                    .sort(function (a, b) { return a - b; });
    var med = SC.quantileSorted(pos, 0.5);
    var widest = finite.slice().sort(function (a, b) {
      return (b.max - b.min) - (a.max - a.min);
    })[0];

    els.statSpecs.textContent = res.nSpec.toLocaleString();
    els.statSpread.textContent = isFinite(med) ? med.toFixed(1) : "—";
    els.statN.textContent = M.nC;
    if (widest) {
      els.statSwingName.textContent = widest.name;
      els.statSwing.textContent = ((widest.max - widest.min) / M.step).toFixed(0);
    }
    if (dom) {
      els.statSettled.textContent = dom.settled;
      els.statPairs.textContent = dom.pairs;
    }
    els.collapse.hidden = res.nSpec !== 1;
  }

  /* ------------------------------------------------------------------ render */

  function render(opts) {
    opts = opts || {};
    var specIds = SC.selectSpecs(M, state.axes);
    els.specCount.textContent = specIds.length.toLocaleString();
    if (!specIds.length) { els.empty.hidden = false; return; }
    els.empty.hidden = true;

    var w = weights();
    var res = SC.evaluate(M, specIds, w);
    lastResult = res;

    renderHeadline(res, null);
    renderTable(res, null);
    renderDetail(res, null);
    drawCharts(res);
    refreshInspector(res);

    // The decomposition and the dominance matrix walk the whole selection a
    // second time, so they settle after the thumb stops rather than competing
    // with it for the frame.
    clearTimeout(heavyTimer);
    heavyTimer = setTimeout(function () {
      var dec = SC.decompose(M, res);
      var dom = SC.dominance(M, res);
      res.dec = dec; res.dom = dom;
      renderHeadline(res, dom);
      renderTable(res, dec);
      renderDetail(res, dec);
      Charts.dominanceMatrix(els.dom, res, dom, M, select, state.selected);
    }, opts.light ? 320 : 30);
  }

  function panelWidth(svg, fallback) {
    var w = svg.parentNode.getBoundingClientRect().width;
    return w > 120 ? Math.round(w) : fallback;
  }

  /* Position i on the curve is a different specification for every company,
   * because each company's scores are sorted independently. This maps a point
   * back to the nine choices that produced it. */
  function curveOrder(res, companyIdx) {
    var pairs = [];
    for (var k = 0; k < res.nSpec; k++) {
      var v = res.R[k * M.nC + companyIdx];
      if (v === v) pairs.push([v, res.specIds[k]]);
    }
    pairs.sort(function (a, b) { return b[0] - a[0]; });
    return pairs;
  }

  /* The inspected specification survives a weight change, but its score does
   * not: the whole point is that the same method gives a different answer under
   * a different weighting. So re-read it on every render rather than leaving a
   * stale number under the cursor. */
  function refreshInspector(res) {
    if (inspectedSpec === null) return;
    var order = curveOrder(res, state.selected);
    for (var i = 0; i < order.length; i++) {
      if (order[i][1] === inspectedSpec) {
        showMethod(inspectedSpec, order[i][0], i, order.length,
                   M.names[state.selected]);
        return;
      }
    }
    // the pinned method is no longer in view, or this company has no score for it
    els.inspector.classList.remove("is-live");
    inspectedSpec = null;
    els.inspWhere.textContent =
      "That method is not in the current selection. Hover the curve to pick another.";
  }

  function showMethod(specIdx, value, rank, total, name) {
    inspectedSpec = specIdx;
    els.inspRank.textContent = isFinite(value) ? value.toFixed(0) : "—";
    els.inspWhere.textContent =
      "method " + (rank + 1).toLocaleString() + " of " + total.toLocaleString() +
      " for " + name;
    els.inspAxes.innerHTML = M.order.map(function (a, i) {
      var o = M.opts[a][M.level(specIdx, i)];
      return '<div><dt>' + (AXIS_COPY[a] || { label: a }).label + "</dt><dd>" +
             (OPTION_COPY[o] || o) + "</dd></div>";
    }).join("");
    var w = weights();
    els.inspWeights.innerHTML = M.pillars.map(function (p, i) {
      return '<span><i class="swatch swatch-' + p + '"></i>' + PILLAR_NAME[p] +
             " <b>" + Math.round(w[i] * 100) + "%</b></span>";
    }).join("");
    els.inspector.classList.add("is-live");
  }

  function drawCharts(res) {
    var order = curveOrder(res, state.selected);
    Charts.specificationCurve(els.curve, res, {
      width: panelWidth(els.curve, 620), height: 300, selected: state.selected,
      step: M.step,
      onHover: function (h) {
        if (!h) { els.curveTip.hidden = true; return; }
        els.curveTip.hidden = false;
        els.curveTipRank.textContent = h.value.toFixed(0);
        els.curveTipText.textContent =
          "method " + (h.rank + 1).toLocaleString() + " of " + h.total.toLocaleString();
        var e = order[h.rank];
        if (e) showMethod(e[1], e[0], h.rank, order.length, h.company.name);
      }
    });
    Charts.contestationMap(els.map, res, {
      width: panelWidth(els.map, 480), height: 300, selected: state.selected,
      step: M.step, onSelect: select
    });
    if (res.dom) Charts.dominanceMatrix(els.dom, res, res.dom, M, select, state.selected);
  }

  function select(i) {
    if (state.selected === i) return;
    state.selected = i;
    els.tbody.querySelectorAll("tr").forEach(function (tr) {
      var on = +tr.dataset.company === i;
      tr.classList.toggle("is-selected", on);
      if (on) tr.setAttribute("aria-current", "true");
      else tr.removeAttribute("aria-current");
    });
    if (lastResult) {
      renderDetail(lastResult, lastResult.dec);
      drawCharts(lastResult);
      refreshInspector(lastResult);
    }
  }

  /* -------------------------------------------------------------------- boot */

  function boot() {
    data = window.MODEL;
    M = SC.prepare(data);
    state = defaultState();

    ["weights", "presets", "axes", "reset", "specCount", "tbody", "curve", "map",
     "dom", "pillars", "pillarNote", "pivot", "pivotNote", "detailName",
     "detailGroup", "bestSpec", "worstSpec", "swing", "statSpread", "statSpecs",
     "statN", "statSwing", "statSwingName", "statSettled", "statPairs",
     "collapse", "empty", "curveTip", "curveTipRank", "curveTipText", "datasetNote",
     "inspector", "inspRank", "inspWhere", "inspAxes", "inspWeights", "inspPin"
    ].forEach(function (id) { els[id] = document.getElementById(id); });

    els.datasetNote.textContent =
      data.meta.n_companies + " companies · " + data.meta.n_fields + " fields · " +
      data.meta.n_specs.toLocaleString() + " specifications · " +
      data.meta.years[0] + "–" + data.meta.years[data.meta.years.length - 1];
    document.body.classList.toggle("is-synthetic", !data.meta.real);

    buildControls();
    syncWeightUI();

    // clicking the inspector collapses the whole grid onto the method under the
    // cursor, which is exactly what a published score is: one cell, no error bar
    els.inspPin.addEventListener("click", function () {
      if (inspectedSpec === null) return;
      M.order.forEach(function (a, i) {
        state.axes[a] = M.opts[a][M.level(inspectedSpec, i)];
      });
      els.axes.querySelectorAll(".seg").forEach(function (seg, ai) {
        var want = state.axes[M.order[ai]];
        seg.querySelectorAll("button").forEach(function (b, j) {
          var o = j === 0 ? "all" : M.opts[M.order[ai]][j - 1];
          b.setAttribute("aria-pressed", o === want ? "true" : "false");
        });
      });
      render();
    });

    render();
    requestAnimationFrame(function () { if (lastResult) drawCharts(lastResult); });

    var t;
    window.addEventListener("resize", function () {
      clearTimeout(t);
      t = setTimeout(function () { if (lastResult) drawCharts(lastResult); }, 120);
    });

    document.addEventListener("keydown", function (e) {
      var tgt = e.target;
      if (tgt && tgt.closest && tgt.closest("input, button, select, a")) return;
      var order = Array.prototype.map.call(els.tbody.querySelectorAll("tr"),
                                           function (tr) { return +tr.dataset.company; });
      var at = order.indexOf(state.selected);
      if (e.key === "ArrowDown" && at < order.length - 1) { e.preventDefault(); select(order[at + 1]); }
      if (e.key === "ArrowUp" && at > 0) { e.preventDefault(); select(order[at - 1]); }
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
