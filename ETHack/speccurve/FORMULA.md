# The formula

One page. Every symbol in the code has the same name.

## Inputs

| Symbol | Meaning | Shape |
|---|---|---|
| `RAW[i,f,y,b]` | the reported number | 20 x 30 x 5 x 3 |
| `BASE[i,y,b]` | size denominator: revenue, volume, headcount | 20 x 5 x 3 |
| `type[f]` | `Q` quantity, `R` rate, `P` percentage, `B` boolean | 30 |
| `pol[f]` | `+1` if a lower raw value is better, `-1` if higher is better | 30 |
| `pil[f]` | pillar `E`, `S` or `F` | 30 |
| `grp[i]` | sub-industry group | 20 |

For `type = Q, P, B` the three `b`-slices of `RAW` hold the same number. For
`type = R` they hold the three published variants of the same rate (per
employee-hours, per contractor-hours, per total-workforce-hours), so the
exposure axis selects a variant instead of dividing.

## A specification

Five axes, one choice each:

| Axis | Options | n |
|---|---|---|
| `b` exposure base | revenue, volume, headcount | 3 |
| `w` window | latest year, 3-year mean | 2 |
| `d` direction | level, change | 2 |
| `z` normaliser | percentile, winsorised min-max, log min-max | 3 |
| `p` peer set | sub-group, whole sector | 2 |

**3 x 2 x 2 x 3 x 2 = 72 specifications.**

Four pillar weightings: `equal` (1/3, 1/3, 1/3), `env_led` (.60, .20, .20),
`social_led` (.20, .60, .20), `finance_led` (.20, .20, .60).

**72 x 4 = 288 scores per company.**

## Step 1 — remove the units

```
x[i,f,y] = RAW[i,f,y,b] / BASE[i,y,b]     if type[f] = Q
         = RAW[i,f,y,b]                   otherwise
```

## Step 2 and 3 — one number per field

```
d = level,  w = latest :  q[i,f] = x[i,f,5]
d = level,  w = mean3  :  q[i,f] = mean(x[i,f,3..5])
d = change, w = latest :  q[i,f] = (x[i,f,5] - x[i,f,3]) / |x[i,f,3]|
d = change, w = mean3  :  q[i,f] = (mean(x[i,f,3..5]) - mean(x[i,f,1..3])) / |mean(x[i,f,1..3])|
```

For `type = B`, "change" is the plain difference, because the denominator is 0.

## Step 4 — one direction

```
u[i,f] = pol[f] * q[i,f]          higher u = worse, always
```

## Step 5 — units become a grade, 0 to 100, 100 = best

Peer set `G(i,p)`; `U = { u[j,f] : j in G, reported }`; `m = |U|`.
A sub-group with fewer than `MIN_PEERS = 4` members is graded against the whole
sector instead, because a 2-member percentile can only return 0 or 100. That is
a rule, not a specification: it is not varied.

```
z = percentile        r = average rank of u[i,f] in U ascending, 1 = best
                      s = 100 * (m - r) / (m - 1)

z = winsor_minmax     lo, hi = 5th, 95th percentile of U
                      s = 100 * (hi - clip(u,lo,hi)) / (hi - lo)        [50 if hi = lo]

z = log_minmax        t = u                                      if min(U) > 0
                        = u - min(U) + 0.01*(max(U) - min(U))    otherwise
                      L = log(t)
                      s = 100 * (max L - L) / (max L - min L)           [50 if degenerate]
```

## Step 6 — aggregate, still 0 to 100

```
S_P[i]  = mean{ s[i,f] : f in P, reported }                  pillar score
T_k[i]  = ( sum_P W_k[P] * S_P[i] ) / ( sum_P W_k[P] * 1{S_P[i] exists} )
```

A weighted mean of 0-100 numbers is already 0-100. **Nothing is rescaled at the
end**, so there is no second hidden choice. Missing fields simply do not enter
the mean, and a missing pillar renormalises the weights.

## Step 7 — rank percentile

```
rho = average rank of T_k[i] descending over all 20, 1 = best
R   = 100 * (N - rho) / (N - 1)
```

## Step 8 — the two outputs

Over all 288 `(specification, weighting)` pairs, per company:

```
consensus = median R
spread    = P75(R) - P25(R)
```

`consensus` is the headline score. `spread` is how much that score is a choice
rather than a fact. Report both, always. A single number is the thing we are
arguing against.

## Order of operations, the one thing that must not be swapped

Aggregate the 30 fields **inside** each specification (step 6), **then** take the
distribution across specifications (step 8).

Do it the other way round, median across specifications first and aggregate
after, and averaging 30 numbers concentrates them: the spread collapses and the
output really does become "one score plus noise". Same inputs, opposite
conclusion, purely from the order.

## What is deliberately NOT varied

Pillar weights. They explain only 13.2% of the divergence between commercial
providers (Berg, Kolbel & Rigobon 2022: measurement 50.1%, scope 36.7%, weights
13.2%), and varying them is a convex combination of the same inputs, so it
concentrates on the equal-weighted answer by the central limit theorem. Weights
are handed to the user as four named views instead. The 72 specifications vary
scope and measurement, which is the other 86.8% and does not concentrate.
