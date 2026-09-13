/* charts.js — the four marks, drawn by hand in SVG.
 *
 * No chart library. Every mark here encodes one thing and the axes are shared
 * across all of them: the vertical scale is always rank percentile, 0 to 100,
 * 100 = best of the twenty. Keeping one scale means the curve, the table bar
 * and the scatter can be read against each other without a translation step.
 */
(function (global) {
  "use strict";

  var NS = "http://www.w3.org/2000/svg";

  function el(name, attrs, parent) {
    var n = document.createElementNS(NS, name);
    if (attrs) for (var k in attrs) if (attrs[k] !== null && attrs[k] !== undefined) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  }

  function clear(node) { while (node.firstChild) node.removeChild(node.firstChild); }

  function css(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }

  /* Contestation is ordinal, so it gets a one-hue sequential ramp with a
   * neutral floor — never a second categorical colour, and never colour alone:
   * every use is paired with the word. */
  /* Measured in rank POSITIONS, not percentile points. With 18 companies a rank
   * percentile can only take 18 values 5.88 apart, so an IQR quoted in points is
   * a quantised quantity wearing a decimal. Positions are what it means. */
  var VERDICTS = [
    { key: "robust",    label: "robust",    max: 1.5,      cls: "v-robust" },
    { key: "contested", label: "contested", max: 3.0,      cls: "v-contested" },
    { key: "opinion",   label: "opinion",   max: Infinity, cls: "v-opinion" }
  ];

  function verdict(positions) {
    for (var i = 0; i < VERDICTS.length; i++) if (positions < VERDICTS[i].max) return VERDICTS[i];
    return VERDICTS[2];
  }

  /* ================================================================ bar
   * One row of the ranking table: min–max whisker, interquartile box, median
   * tick. The box width IS the contestation, so the eye compares widths down
   * the column without reading a single number.
   */
  function distributionBar(svg, d, opts) {
    clear(svg);
    var w = opts.width, h = opts.height, pad = 5;
    svg.setAttribute("viewBox", "0 0 " + w + " " + h);
    var x = function (v) { return pad + (v / 100) * (w - 2 * pad); };
    var mid = h / 2;
    var v = verdict(d.positions);

    el("line", { x1: pad, x2: w - pad, y1: mid, y2: mid, class: "bar-track" }, svg);

    if (!isFinite(d.consensus)) return v;

    el("line", { x1: x(d.min), x2: x(d.max), y1: mid, y2: mid, class: "bar-whisker" }, svg);
    el("line", { x1: x(d.min), x2: x(d.min), y1: mid - 4, y2: mid + 4, class: "bar-cap" }, svg);
    el("line", { x1: x(d.max), x2: x(d.max), y1: mid - 4, y2: mid + 4, class: "bar-cap" }, svg);

    var bx = x(d.p25), bw = Math.max(3, x(d.p75) - x(d.p25));
    el("rect", { x: bx, y: mid - 7, width: bw, height: 14, rx: 4, class: "bar-iqr " + v.cls }, svg);
    el("line", { x1: x(d.consensus), x2: x(d.consensus), y1: mid - 9, y2: mid + 9, class: "bar-median" }, svg);
    return v;
  }

  /* ================================================================ curve
   * Every company's scores sorted best-to-worst and overlaid. A flat line is a
   * company every defensible method agrees about; a steep one is a company
   * whose rating is a choice. This is the whole argument in one mark, which is
   * why it gets the largest panel.
   */
  function specificationCurve(svg, res, opts) {
    clear(svg);
    var W = opts.width, H = opts.height;
    var m = { t: 14, r: 16, b: 30, l: 38 };
    svg.setAttribute("viewBox", "0 0 " + W + " " + H);

    var iw = Math.max(140, W - m.l - m.r), ih = Math.max(80, H - m.t - m.b);
    var n = res.companies[0] ? res.companies[0].sorted.length : 0;
    if (!n) return;

    var X = function (i) { return m.l + (n === 1 ? iw / 2 : (i / (n - 1)) * iw); };
    var Y = function (v) { return m.t + ih - (v / 100) * ih; };

    // grid + y axis
    [0, 25, 50, 75, 100].forEach(function (t) {
      el("line", { x1: m.l, x2: W - m.r, y1: Y(t), y2: Y(t), class: t === 50 ? "grid grid-mid" : "grid" }, svg);
      el("text", { x: m.l - 8, y: Y(t) + 3.5, class: "axis-label", "text-anchor": "end" }, svg).textContent = t;
    });

    var sel = opts.selected;

    // every company, recessive
    res.companies.forEach(function (c) {
      if (c.index === sel) return;
      var pts = [];
      for (var i = 0; i < c.sorted.length; i++) pts.push(X(i) + "," + Y(c.sorted[c.sorted.length - 1 - i]));
      el("polyline", { points: pts.join(" "), class: "curve-ghost" }, svg);
    });

    // the selected company, with its interquartile band behind it
    var c = res.companies[sel];
    if (c && isFinite(c.consensus)) {
      el("rect", {
        x: m.l, y: Y(c.p75), width: iw, height: Math.max(1, Y(c.p25) - Y(c.p75)),
        class: "curve-band"
      }, svg);
      el("line", { x1: m.l, x2: W - m.r, y1: Y(c.consensus), y2: Y(c.consensus), class: "curve-median" }, svg);

      var pts = [];
      for (var i = 0; i < c.sorted.length; i++) pts.push(X(i) + "," + Y(c.sorted[c.sorted.length - 1 - i]));
      el("polyline", { points: pts.join(" "), class: "curve-halo" }, svg);
      el("polyline", { points: pts.join(" "), class: "curve-main" }, svg);

      el("text", { x: W - m.r, y: Y(c.consensus) - 7, class: "curve-tag", "text-anchor": "end" }, svg)
        .textContent = c.name + " · consensus " + c.consensus.toFixed(0);
    }

    el("text", { x: m.l, y: H - 8, class: "axis-label" }, svg)
      .textContent = "best method";
    el("text", { x: W - m.r, y: H - 8, class: "axis-label", "text-anchor": "end" }, svg)
      .textContent = n.toLocaleString() + " scores · worst method";

    // hover crosshair over the selected company's curve
    var hover = el("g", { class: "curve-hover", visibility: "hidden" }, svg);
    var hLine = el("line", { y1: m.t, y2: m.t + ih, class: "crosshair" }, hover);
    var hDot = el("circle", { r: 4.5, class: "crosshair-dot" }, hover);

    var hit = el("rect", { x: m.l, y: m.t, width: iw, height: ih, fill: "transparent" }, svg);
    hit.style.cursor = "crosshair";

    hit.addEventListener("pointermove", function (e) {
      if (!c || !isFinite(c.consensus)) return;
      var box = svg.getBoundingClientRect();
      var px = ((e.clientX - box.left) / box.width) * W;
      var i = Math.round(((px - m.l) / iw) * (n - 1));
      i = Math.max(0, Math.min(n - 1, i));
      var v = c.sorted[c.sorted.length - 1 - i];
      hover.setAttribute("visibility", "visible");
      hLine.setAttribute("x1", X(i)); hLine.setAttribute("x2", X(i));
      hDot.setAttribute("cx", X(i)); hDot.setAttribute("cy", Y(v));
      if (opts.onHover) opts.onHover({ rank: i, value: v, total: n, company: c });
    });
    hit.addEventListener("pointerleave", function () {
      hover.setAttribute("visibility", "hidden");
      if (opts.onHover) opts.onHover(null);
    });
  }

  /* ================================================================ scatter
   * Consensus against contestation. The quadrants are the product: the left
   * half is information you can act on, the right half is a warning label.
   */
  function contestationMap(svg, res, opts) {
    clear(svg);
    var W = opts.width, H = opts.height;
    var m = { t: 30, r: 18, b: 40, l: 40 };
    svg.setAttribute("viewBox", "0 0 " + W + " " + H);
    var iw = Math.max(120, W - m.l - m.r), ih = Math.max(80, H - m.t - m.b);

    var pts = res.companies.filter(function (c) { return isFinite(c.consensus); });
    if (!pts.length) return;

    var maxSpread = Math.max(10, Math.ceil(Math.max.apply(null, pts.map(function (c) { return c.spread; })) / 5) * 5);
    var X = function (v) { return m.l + (v / maxSpread) * iw; };
    var Y = function (v) { return m.t + ih - (v / 100) * ih; };

    [0, 25, 50, 75, 100].forEach(function (t) {
      el("line", { x1: m.l, x2: W - m.r, y1: Y(t), y2: Y(t), class: "grid" }, svg);
      el("text", { x: m.l - 8, y: Y(t) + 3.5, class: "axis-label", "text-anchor": "end" }, svg).textContent = t;
    });

    // the two verdict thresholds, which is where the quadrant lines belong
    [12, 25].forEach(function (t) {
      if (t > maxSpread) return;
      el("line", { x1: X(t), x2: X(t), y1: m.t, y2: m.t + ih, class: "grid grid-mid" }, svg);
      el("text", { x: X(t), y: H - 20, class: "axis-label", "text-anchor": "middle" }, svg).textContent = t;
    });
    el("line", { x1: m.l, x2: W - m.r, y1: Y(50), y2: Y(50), class: "grid grid-mid" }, svg);

    // Quadrant names sit outside the plot rather than inside it, where they
    // were landing on top of the points they describe.
    el("text", { x: m.l, y: m.t - 11, class: "quad-label" }, svg)
      .textContent = "\u2190 every method agrees";
    el("text", { x: W - m.r, y: m.t - 11, class: "quad-label", "text-anchor": "end" }, svg)
      .textContent = "the method decides \u2192";

    var labelled = {};
    var bySpread = pts.slice().sort(function (a, b) { return b.spread - a.spread; });
    labelled[bySpread[0].index] = 1;
    var byCons = pts.slice().sort(function (a, b) { return b.consensus - a.consensus; });
    labelled[byCons[0].index] = 1;
    labelled[byCons[byCons.length - 1].index] = 1;
    labelled[opts.selected] = 1;

    pts.forEach(function (c) {
      var v = verdict(c.positions);
      var g = el("g", { class: "dot-group" + (c.index === opts.selected ? " is-selected" : "") }, svg);
      g.dataset.company = c.index;
      el("circle", { cx: X(c.spread), cy: Y(c.consensus), r: 9, class: "dot-hit" }, g);
      el("circle", { cx: X(c.spread), cy: Y(c.consensus), r: c.index === opts.selected ? 7 : 5, class: "dot " + v.cls }, g);
      if (labelled[c.index]) {
        // A company at rank 100 sits on the top gridline, where the label would
        // land on the header text. Flip it under the dot instead.
        var ly = Y(c.consensus) - 11;
        if (ly < m.t + 4) ly = Y(c.consensus) + 17;
        el("text", {
          x: Math.min(W - m.r - 12, Math.max(m.l + 12, X(c.spread))), y: ly,
          class: "dot-label" + (c.index === opts.selected ? " is-selected" : ""),
          "text-anchor": "middle"
        }, g).textContent = c.name;
      }
      g.addEventListener("click", function () { if (opts.onSelect) opts.onSelect(c.index); });
      g.style.cursor = "pointer";
    });

    el("text", { x: m.l, y: H - 6, class: "axis-title" }, svg)
      .textContent = "contestation, rank points \u2192";
    el("text", {
      x: 11, y: m.t + ih / 2, class: "axis-title", "text-anchor": "middle",
      transform: "rotate(-90 11 " + (m.t + ih / 2) + ")"
    }, svg).textContent = "consensus rank \u2192";
  }

  /* ================================================================ pillars
   * Three grades plus the weight each is carrying. Direct-labelled, because
   * the three pillar hues sit below 3:1 against the surface and colour must
   * never be the only channel.
   */
  function pillarBars(root, scores, weights, pillars, composite, names) {
    root.innerHTML = "";
    pillars.forEach(function (p, i) {
      var v = scores[p], w = weights[i];
      var row = document.createElement("div");
      row.className = "pillar-row" + (w === 0 ? " is-off" : "");
      row.innerHTML =
        '<span class="pillar-name"><i class="swatch swatch-' + p + '"></i>' + names[p] + "</span>" +
        '<span class="pillar-weight">' + Math.round(w * 100) + "%</span>" +
        '<span class="pillar-track"><i class="pillar-fill pillar-' + p + '" style="width:' +
        (isFinite(v) ? v.toFixed(1) : 0) + '%"></i></span>' +
        '<span class="pillar-value">' + (isFinite(v) ? v.toFixed(1) : "\u2014") + "</span>";
      root.appendChild(row);
    });
    var tot = document.createElement("div");
    tot.className = "pillar-row is-total";
    tot.innerHTML =
      '<span class="pillar-name">Composite</span><span class="pillar-weight"></span>' +
      '<span class="pillar-track"><i class="pillar-fill pillar-total" style="width:' +
      (isFinite(composite) ? composite.toFixed(1) : 0) + '%"></i></span>' +
      '<span class="pillar-value">' + (isFinite(composite) ? composite.toFixed(1) : "\u2014") + "</span>";
    root.appendChild(tot);
  }

  /* ================================================================ pivot
   * The grid is a complete balanced factorial, so the variance of a company's
   * rank decomposes into main effects with no design correction. This is the
   * answer to "your score is uncertain" that a warning label cannot give: it
   * names the one choice that decides the rest.
   */
  function pivotBars(root, d, copy) {
    root.innerHTML = "";
    if (!d || !d.ranked) { root.innerHTML = '<p class="note">\u2014</p>'; return; }
    var max = Math.max.apply(null, d.ranked.map(function (a) { return d.axes[a]; }).concat([1]));
    d.ranked.forEach(function (a, i) {
      var v = d.axes[a];
      var row = document.createElement("div");
      row.className = "src-row" + (i === 0 ? " is-pivot" : "");
      row.innerHTML =
        '<span class="src-name">' + (copy[a] || { label: a }).label + "</span>" +
        '<span class="src-track"><i class="src-fill ' +
        (i === 0 ? "src-method" : "src-weights") + '" style="width:' +
        ((v / max) * 100).toFixed(1) + '%"></i></span>' +
        '<span class="src-value">' + v.toFixed(0) + "%</span>";
      root.appendChild(row);
    });
  }

  /* ================================================================ dominance
   * A total ordering of eighteen companies is a claim the data cannot support.
   * What survives is a partial order: the pairs where one company outranks the
   * other under essentially every method. Solid corners are the settled block;
   * the mush in the middle is the part of a league table that is fiction.
   */
  function dominanceMatrix(svg, res, dom, M, onSelect, selected) {
    clear(svg);
    var order = res.companies.slice().sort(function (a, b) {
      return (b.consensus || 0) - (a.consensus || 0);
    });
    var n = order.length, pad = 34, cell = 15;
    var W = pad + n * cell + 6, H = pad + n * cell + 6;
    svg.setAttribute("viewBox", "0 0 " + W + " " + H);

    for (var a = 0; a < n; a++) {
      var i = order[a].index;
      el("text", { x: pad - 4, y: pad + a * cell + cell / 2 + 3,
                   class: "dot-label" + (i === selected ? " is-selected" : ""),
                   "text-anchor": "end" }, svg).textContent = order[a].name;
      var t = el("text", { x: pad + a * cell + cell / 2, y: pad - 5,
                   class: "dot-label" + (i === selected ? " is-selected" : ""),
                   "text-anchor": "start",
                   transform: "rotate(-90 " + (pad + a * cell + cell / 2) + " " + (pad - 5) + ")" }, svg);
      t.textContent = order[a].name;

      for (var b = 0; b < n; b++) {
        var j = order[b].index;
        if (i === j) {
          el("rect", { x: pad + b * cell, y: pad + a * cell, width: cell - 1,
                       height: cell - 1, class: "dom-self" }, svg);
          continue;
        }
        var v = dom.D[i * dom.nC + j];
        if (v !== v) continue;
        // shade by v itself, so dark means "the row wins". Shading by |v-0.5|
        // would make the matrix symmetric and hide the direction entirely.
        var settled = v > 0.95;
        var g = el("rect", {
          x: pad + b * cell, y: pad + a * cell, width: cell - 1, height: cell - 1,
          rx: 2, class: "dom-cell" + (settled ? " is-settled" : ""),
          "fill-opacity": (0.04 + 0.92 * v).toFixed(3)
        }, svg);
        g.appendChild(el("title", {}, null)).textContent =
          order[a].name + " outranks " + order[b].name + " in " +
          Math.round(v * 100) + "% of methods in view";
      }
    }
  }

  /* ================================================================ sources
   * Two spreads in the same units, so the slider's own influence can be
   * compared with the influence of the method choices rather than asserted.
   */
  function sourceBars(root, dec) {
    root.innerHTML = "";
    var max = Math.max(dec.methodMean, dec.weightsMean, 1);
    [
      ["Scope and measurement", dec.methodMean, "src-method", "the 72 specifications"],
      ["Pillar weighting", dec.weightsMean, "src-weights", "the whole weight simplex"]
    ].forEach(function (r) {
      var row = document.createElement("div");
      row.className = "src-row";
      row.innerHTML =
        '<span class="src-name">' + r[0] + '<em>' + r[3] + "</em></span>" +
        '<span class="src-track"><i class="src-fill ' + r[2] + '" style="width:' +
        ((r[1] / max) * 100).toFixed(1) + '%"></i></span>' +
        '<span class="src-value">' + (isFinite(r[1]) ? r[1].toFixed(1) : "—") + "</span>";
      root.appendChild(row);
    });
  }

  global.Charts = {
    verdict: verdict,
    VERDICTS: VERDICTS,
    distributionBar: distributionBar,
    specificationCurve: specificationCurve,
    contestationMap: contestationMap,
    pillarBars: pillarBars,
    pivotBars: pivotBars,
    dominanceMatrix: dominanceMatrix,
    sourceBars: sourceBars,
    el: el,
    clear: clear,
    css: css
  };
})(window);
