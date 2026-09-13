/* compute.js — the last three steps of the formula, browser side.
 *
 * `model/export_web.py` ships a cube
 *
 *     P[spec][company][pillar]     0..100, null where there is no score
 *
 * over the full 17,496-cell grid, in a canonical nested-product order. The
 * pillar weights enter only after that, so everything a user can move lives
 * downstream of the cube and the page can do the rest itself:
 *
 *     T = weighted power mean of the four pillar scores
 *     R = rank percentile of T across the companies that have one
 *         then the median and IQR over whichever specifications are in view
 *
 * The arithmetic is the same arithmetic as `model/spec.py`, and the spec index
 * decode is verified against it cell by cell.
 */
(function (global) {
  "use strict";

  function prepare(m) {
    var order = m.meta.axis_order,
      opts = m.meta.axes,
      nC = m.companies.length,
      nP = m.meta.pillars.length,
      nS = m.P.length;

    // mixed-radix: the grid is a full nested product, so a spec index decodes
    // to its nine choices without shipping a spec table at all
    var radix = order.map(function (a) { return opts[a].length; });
    var stride = new Array(order.length);
    var acc = 1;
    for (var i = order.length - 1; i >= 0; i--) { stride[i] = acc; acc *= radix[i]; }

    var P = new Float64Array(nS * nC * nP);
    for (var s = 0; s < nS; s++) {
      var rowS = m.P[s];
      for (var c = 0; c < nC; c++) {
        var rowC = rowS[c];
        for (var p = 0; p < nP; p++) {
          var v = rowC[p];
          P[(s * nC + c) * nP + p] = (v === null || v === undefined) ? NaN : v;
        }
      }
    }

    // the aggregator is a per-spec property, so cache it rather than decoding
    // it inside the hot loop
    var aggAxis = order.indexOf("aggregator");
    var aggOf = new Uint8Array(nS);
    for (s = 0; s < nS; s++) aggOf[s] = level(s, aggAxis);

    function level(specIdx, axisIdx) {
      return Math.floor(specIdx / stride[axisIdx]) % radix[axisIdx];
    }

    return {
      raw: m, order: order, opts: opts, radix: radix, stride: stride,
      nC: nC, nP: nP, nS: nS, P: P, aggOf: aggOf, level: level,
      pillars: m.meta.pillars,
      names: m.companies.map(function (c) { return c.ticker; }),
      step: m.meta.rank_step
    };
  }

  /** Spec indices matching a set of pinned axis choices. `pins[axis]` is an
   *  option string, or "all" to leave that axis varying. */
  function selectSpecs(M, pins) {
    var out = [];
    var fixed = [];
    for (var a = 0; a < M.order.length; a++) {
      var pick = pins[M.order[a]];
      if (pick && pick !== "all") {
        fixed.push([a, M.opts[M.order[a]].indexOf(pick)]);
      }
    }
    for (var s = 0; s < M.nS; s++) {
      var ok = true;
      for (var k = 0; k < fixed.length; k++) {
        if (M.level(s, fixed[k][0]) !== fixed[k][1]) { ok = false; break; }
      }
      if (ok) out.push(s);
    }
    return out;
  }

  /* Bloomberg's shifted power mean. p = 1 is the arithmetic mean MSCI uses,
   * p = 0.5 is Bloomberg's, p -> 0 is the geometric mean. On this 0..100 scale
   * the shift that matches their s = 1 on 0..10 is s = 10. Weights renormalise
   * over the pillars a company actually has. */
  var SHIFT = 10;

  function combine(M, s, c, w, agg, out) {
    var base = (s * M.nC + c) * M.nP, tot = 0, acc = 0, v, wi;
    for (var p = 0; p < M.nP; p++) {
      v = M.P[base + p];
      if (v !== v) continue;
      wi = w[p];
      if (wi <= 0) continue;
      tot += wi;
      if (agg === 0) acc += wi * v;
      else if (agg === 1) acc += wi * Math.sqrt(v + SHIFT);
      else acc += wi * Math.log(v + SHIFT);
    }
    if (tot <= 0) return NaN;
    acc /= tot;
    if (agg === 0) return acc;
    if (agg === 1) return acc * acc - SHIFT;
    return Math.exp(acc) - SHIFT;
  }

  function rankPercentile(T, idx, out) {
    var n = T.length, m = 0, i;
    for (i = 0; i < n; i++) { out[i] = NaN; if (T[i] === T[i]) idx[m++] = i; }
    if (m < 2) return out;
    var live = idx.subarray(0, m);
    Array.prototype.sort.call(live, function (a, b) { return T[b] - T[a]; });
    i = 0;
    while (i < m) {
      var j = i;
      while (j + 1 < m && T[live[j + 1]] === T[live[i]]) j++;
      var pct = (100 * (m - ((i + j) / 2 + 1))) / (m - 1);
      for (var k = i; k <= j; k++) out[live[k]] = pct;
      i = j + 1;
    }
    return out;
  }

  function quantileSorted(a, q) {
    var n = a.length;
    if (!n) return NaN;
    if (n === 1) return a[0];
    var h = (n - 1) * q, lo = Math.floor(h), hi = Math.ceil(h);
    return a[lo] + (h - lo) * (a[hi] - a[lo]);
  }

  /**
   * Run every selected specification.
   * Returns per-company distributions, and R laid out [spec][company] for the
   * decomposition and the dominance matrix.
   */
  function evaluate(M, specIds, weights) {
    var nC = M.nC, nS = specIds.length;
    var T = new Float64Array(nC), R = new Float64Array(nC);
    var idx = new Int32Array(nC);
    var all = new Float64Array(nS * nC);

    for (var k = 0; k < nS; k++) {
      var s = specIds[k], agg = M.aggOf[s];
      for (var c = 0; c < nC; c++) T[c] = combine(M, s, c, weights, agg);
      rankPercentile(T, idx, R);
      all.set(R, k * nC);
    }

    var companies = [];
    for (c = 0; c < nC; c++) {
      var v = [];
      for (k = 0; k < nS; k++) {
        var r = all[k * nC + c];
        if (r === r) v.push(r);
      }
      v.sort(function (a, b) { return a - b; });
      var p25 = quantileSorted(v, 0.25), p75 = quantileSorted(v, 0.75);
      var spread = p75 - p25;
      companies.push({
        index: c, name: M.names[c],
        peers: M.raw.companies[c].peers,
        coverage: M.raw.companies[c].coverage,
        n: v.length,
        consensus: quantileSorted(v, 0.5),
        p25: p25, p75: p75, spread: spread,
        positions: spread / M.step,
        min: v.length ? v[0] : NaN,
        max: v.length ? v[v.length - 1] : NaN,
        sorted: v
      });
    }
    return { companies: companies, R: all, specIds: specIds, nSpec: nS };
  }

  /**
   * Which axis decides this company's rating.
   *
   * The grid is a complete balanced factorial, so the variance of a company's
   * rank percentile decomposes into main effects with no design correction:
   * eta2 = SS(axis) / SS(total). Whatever the main effects leave unexplained is
   * interaction between the axes, and it is reported rather than hidden.
   */
  function decompose(M, res) {
    var nC = M.nC, nS = res.nSpec, out = [];
    for (var c = 0; c < nC; c++) {
      var y = [], sIdx = [];
      for (var k = 0; k < nS; k++) {
        var r = res.R[k * nC + c];
        if (r === r) { y.push(r); sIdx.push(res.specIds[k]); }
      }
      var row = { index: c, name: M.names[c], axes: {}, explained: 0, n: y.length };
      if (y.length < 4) { out.push(row); continue; }
      var gm = 0, i;
      for (i = 0; i < y.length; i++) gm += y[i];
      gm /= y.length;
      var sst = 0;
      for (i = 0; i < y.length; i++) sst += (y[i] - gm) * (y[i] - gm);
      if (sst <= 0) { out.push(row); continue; }

      for (var a = 0; a < M.order.length; a++) {
        var nL = M.radix[a], sum = new Float64Array(nL), cnt = new Float64Array(nL);
        for (i = 0; i < y.length; i++) {
          var L = M.level(sIdx[i], a);
          sum[L] += y[i]; cnt[L]++;
        }
        var ss = 0;
        for (var L2 = 0; L2 < nL; L2++) {
          if (!cnt[L2]) continue;
          var d = sum[L2] / cnt[L2] - gm;
          ss += cnt[L2] * d * d;
        }
        var eta = (100 * ss) / sst;
        row.axes[M.order[a]] = eta;
        row.explained += eta;
      }
      row.ranked = Object.keys(row.axes).sort(function (x, z) {
        return row.axes[z] - row.axes[x];
      });
      row.pivot = row.ranked[0];
      row.pivotPct = row.axes[row.pivot];
      out.push(row);
    }
    return out;
  }

  /** P(i outranks j) over every specification both companies score in. */
  function dominance(M, res) {
    var nC = M.nC, nS = res.nSpec;
    var D = new Float64Array(nC * nC).fill(NaN);
    for (var i = 0; i < nC; i++) {
      for (var j = 0; j < nC; j++) {
        if (i === j) continue;
        var w = 0, n = 0;
        for (var k = 0; k < nS; k++) {
          var a = res.R[k * nC + i], b = res.R[k * nC + j];
          if (a !== a || b !== b) continue;
          n++;
          if (a > b) w++;
        }
        if (n) D[i * nC + j] = w / n;
      }
    }
    var settled = 0, pairs = 0;
    for (i = 0; i < nC; i++) {
      for (j = i + 1; j < nC; j++) {
        var v = D[i * nC + j];
        if (v !== v) continue;
        pairs++;
        if (v > 0.95 || v < 0.05) settled++;
      }
    }
    return { D: D, nC: nC, settled: settled, pairs: pairs };
  }

  global.SC = {
    prepare: prepare, selectSpecs: selectSpecs, evaluate: evaluate,
    decompose: decompose, dominance: dominance,
    quantileSorted: quantileSorted
  };
})(window);
