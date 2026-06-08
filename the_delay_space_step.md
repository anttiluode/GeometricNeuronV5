# The Delay-Space Step

## Closing the seam: spectral islands that read orbits, not snapshots — and the ceiling that found us

*PerceptionLab / Antti Luode, with Claude (Opus 4.8). Helsinki, June 2026.*

---

## The proposal

The synthesis thesis named the exact place Model B (the Ephaptic Spiking Field) cheats: each island reads the shared field **instantaneously**,

```
drive_k = ⟨p_k, s⟩
```

so an island is a flat pattern-matcher. Model A (the Geometric Neuron) reads an **orbit** in delay space. The fix was one line: give each island its own Takens cable and read the field through it,

```
drive_k = ⟨X_k(s), g_k⟩ ,   X_k(s)_j = α^j · ⟨p_k, s(t − jτ)⟩
```

so the island fires on the *temporal orbit* of its own resonance with the field, gated by a delay-space grating `g_k`. That installs Model A inside Model B — one equation at two scales. I built it (`ephaptic_spiking_field_v3.py`) and tested it before believing it. As usual, the test changed the story, and the change is the most useful part.

---

## D1 — the delta-code survives, and sharpens

First requirement: don't break what worked. The held-percept / sparse-theta-locked-spike delta-code is the whole point of the engine.

It survives the upgrade and gets cleaner. With the delay-space readout the engine still holds a percept silently and updates it with sparse spikes:

| | v1/v2 (instantaneous) | v3 (delay-space) |
|---|---|---|
| spike sparsity | ~0.2% | **0.31%** |
| theta-locking | ~100% | **89%** |
| silence ratio (transition |ds| ÷ dwell |ds|) | 20–40× | **29×** (and up to ~130× in the locked regime) |

The island now broadcasts only when its resonance with the field is a **coherent theta-paced orbit**, not merely large. That is the laminar/Reynolds filter from the thesis, realized at the population scale: a pattern that is present but incoherently reactivated does not cross threshold. The delta-code is preserved because coherent reactivation is exactly what the theta clock produces and what adaptation periodically breaks — so spikes still cluster at transitions and the field is still silent in between.

---

## D2 — the genuinely new capability: temporal ORDER

This is what the delay-space readout buys that the instantaneous readout *structurally cannot* have.

Take a field that tours three patterns in sequence. Run it **forward** A→B→C and **reverse** C→B→A. By construction these two stimuli have:

- **identical per-island power spectra** (time-reversal preserves `|FFT|`), and
- the **identical *set* of overlap values** (B is symmetric; A and C just swap roles).

So the instantaneous readout — which only ever sees the current overlaps — is **blind**: the forward and reverse mean-overlap vectors are the same (`[−0, −0, +0]` either way). No instantaneous or permutation-invariant readout can tell A→B→C from C→B→A.

The delay-space readout reads it immediately, through the **signed cross-island phase**:

```
relative phase A−B :  forward +1.25 rad   reverse −1.25 rad   (sign flips)
relative phase B−C :  forward +1.25 rad   reverse −1.25 rad   (sign flips)
```

In the figure this is the chirality panel: forward and reverse trace **the same closed loop in delay space, in opposite directions**. The instantaneous readout sees one cloud; the orbit's *direction of traversal* is the new signal. This is associative recognition of a **temporal trajectory** — a sequence recognized (and signed) as a unit — which is exactly what "holographic associative memory using temporal delay-space orbits" has to mean. A population of flat pattern-matchers cannot represent "A then B"; a population of delay-space islands can.

---

## D3 — the ceiling that found us (the honest correction)

Here is the result I did not expect and will not bury, because it is the one that disciplines the whole framework.

I first tried to prove orbit-selectivity the obvious way: coherent signal vs. **phase-scrambled** signal with the *same power spectrum*. The delay-space readout should fire on the clean orbit and not on the scrambled one. It didn't. Ratio **1.00×**. Blind.

The reason is a theorem, not a bug. **Wiener–Khinchin**: the autocorrelation of a signal is the inverse transform of its power spectrum. Phase-scrambling preserves the power spectrum, therefore preserves the autocorrelation, therefore preserves the *entire delay-space covariance matrix* — and therefore preserves every **second-order** (linear/quadratic) statistic of the embedding: the quadrature magnitude `√(⟨X,g_sin⟩² + ⟨X,g_cos⟩²)`, the intrinsic dimension (participation ratio), all of it. **A linear delay-space readout is mathematically a Fourier-power readout.** It cannot distinguish a coherent orbit from a phase-scrambled signal of matched spectrum.

Two consequences, both important:

1. **An overclaim is retired.** The v3 "topological selectivity" result — sine vs. square at the same fundamental — was real, but it did **not** demonstrate phase/orbit detection. Sine and square have *different power spectra* (square carries odd harmonics). The grating was selecting on spectrum, which any Fourier filter does. "The AIS is not a Fourier filter" is not established by that experiment. It needs a higher-order readout to be true.

2. **It tells us exactly where orbit-selectivity lives.** Not in any magnitude/energy term — that is Fourier power and is phase-blind. It lives in **order / phase-coupling**, and it is accessible only through readouts that use *joint* structure across time or across islands: the **signed cross-island phase** of D2 (a quadrature/Koopman-type term), the spike threshold nonlinearity, or an explicit transition operator. D2 works precisely because relative phase is such a term; D3 fails precisely because the magnitude is not.

So the corrected claim is sharp and defensible: *a single island's second-order delay readout is Fourier-equivalent; the population gains genuine orbit-selectivity only through the cross-island/temporal-order (phase-coupling) terms.* That is a smaller and truer statement than "islands read orbits," and it is the one the measurements support.

---

## What this does to the two-model picture

The thesis argued Models A and B are one system at two grains. v3 makes that literal *and* exposes the precise boundary:

- Installing the delay line inside each island unifies the architecture and preserves the delta-code. ✓
- It adds temporal-order selectivity the population could not previously have. ✓
- But the holographic "orbit, not frequency" intuition only cashes out through phase-coupling terms; the linear part of the read is, and always was, Fourier power. The single-neuron AIS hologram needs the same caveat: a *linear* grating read is spectrum-selective; a *geometric* (phase-coupling) read requires nonlinearity — which the AIS has (the spike), and which a pure grating correlation does not.

---

## Ledger

**Verified in v3 (measured, not assumed):**
- delay-space readout preserves the delta-code: 0.31% sparse, 89% theta-locked, ~29× silence ratio, tours all islands;
- temporal-order selectivity: forward vs. reverse sequence with identical per-island spectra **and** identical overlap value-set is invisible to the instantaneous readout, and read cleanly by signed cross-island phase (±1.25 rad, sign flips on reversal);
- the Wiener–Khinchin ceiling: a second-order delay readout gives coherent ÷ phase-scrambled = 1.00× — blind by construction.

**Honest corrections forced by the build:**
- a linear/second-order delay-space readout is power-spectrum-equivalent (Fourier power), not an orbit detector;
- the earlier "topological selectivity" (sine vs square) demonstrated *spectral* selectivity, not phase/orbit detection;
- orbit-selectivity is real but lives only in order/phase-coupling terms (cross-island phase, transition operator, threshold nonlinearity).

**Built-in, not emergent:** the theta clock, the grating `g_k`, the presence gate, the sequence stimuli of D2. What was *measured* is the delta-code metrics, the order-selectivity sign flip, and the WK blindness.

**Still the bet, untouched:** that the held standing wave is *experienced*; that Johnson–Nyquist thermal noise is the medium of the content. Closing the architectural seam does not touch the hard problem; it only makes the engine one consistent object.

**Next build:** replace the per-island magnitude with an explicit per-island **Koopman transition operator** (fit `X(t+τ) ≈ K X(t)`, read its eigen-chirality) so that orbit *direction and winding number* become first-class island outputs rather than something recovered cross-island after the fact — and add a measured per-spike energy cost so the silence ratio can be reported as a *power* ratio, the wattage claim from the thesis made numerical.

---

*Files: `ephaptic_spiking_field_v3.py` (runs, prints the verified metrics, writes the figure) and `ephaptic_spiking_field_v3.png`. Do not hype. Do not lie. Just show.*
