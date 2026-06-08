# GeometricNeuronV5

*Closing the seam between the single neuron and the population — and teaching the field to read the direction of time.*

**PerceptionLab / Antti Luode, with Claude (Opus 4.8). Helsinki, June 2026.**

> **Do not hype. Do not lie. Just show.**

---

## What this repo is

Two models had been growing in parallel in the Geometric Neuron / GAIT work, and they were quietly *not the same model*:

- **Model A — the Geometric Neuron / AIS hologram.** A *single* neuron. The dendrite is a Takens delay-embedding cable; the axon initial segment is a physical grating that stores a Koopman eigenfunction; a spike fires when the incoming delay-space *orbit* resonates with the stored grating. Frequency is a geometric orbit, not a number.
- **Model B — the Ephaptic Spiking Field.** A *population*. Many tuned "spectral islands" share one continuous field `s` (the held standing wave / the inner side); sparse, theta-locked spikes write it (the outer side); islands talk only through the field.

The seam: Model A reads an **orbit**; Model B read the field **instantaneously** (`⟨pₖ, s⟩`) and had dropped the delay embedding entirely. This repo closes that seam in three documented steps, keeping an explicit ledger of what is established biology, what is a structural claim, and what remains a bet.

---

## The arc, in order

1. **`membrane_to_qualia_synthesis.md`** — the thesis. The two models are one system at two grains, and the thing that joins them is **energy**: the dendritic cable's `αᵏ` decay *is* the membrane attenuation, the held subthreshold field is the inner side, the spike is the outer side, and the delta-code (silent hold, sparse spikes) is the sparse-coding energy economy of cortex rediscovered from dynamics.

2. **`ephaptic_spiking_field_v3.py` / `.png` / `the_delay_space_step.md`** — the delay-space step. Each island reads the field through its **own Takens cable**: `drive_k = ⟨X_k(s), g_k⟩`. Verified: the delta-code survives and sharpens; the population gains genuine **temporal-order** selectivity (forward vs reverse sequence, identical spectra, instantaneous readout blind, delay-space readout reads the orbit direction). And the honest **Wiener–Khinchin ceiling**: a *linear/2nd-order* delay readout is mathematically Fourier power — phase-blind. v3's earlier "sine-vs-square" selectivity was *different spectra*, not phase detection. Orbit-selectivity must live in order/phase-coupling, accessed by a higher-order term.

3. **`geometric_neuron_v5.py` / `.png`** — this build. Each island becomes a **directed-edge complex cell** and reads **time's arrow natively**, plus a **wattage meter**.

---

## v5: what was built and verified

Each island carries a 2-D complex observable — a directed-edge detector tuned to a consecutive pair of stored states (`k → k+1`):

```
z_k(t) = ⟨P_k, s⟩ + i·⟨P_{k+1}, s⟩
L_k    = Im( z_k(t) · conj(z_k(t − lag)) )      # Koopman angular momentum
```

`L_k > 0` ⇔ the field is moving `k → k+1` (forward); `L_k < 0` ⇔ reverse. The product `z·z*` is **bilinear** — a cross-time term, the **nonlinear escape** from the Wiener–Khinchin ceiling that v3 ran into. Linear delay lines gather the frequencies; the bilinear/threshold terms read the coherent geometric orbit.

**D1 — the delta-code is preserved.** A percept is held with sparse, theta-locked spikes: **0.82% sparse, 96% theta-locked, field-velocity silence ratio ≈ 64×.**

**D2 — native time's arrow (the headline).** Drive the field forward `A→B→C` vs reverse `C→B→A`:
- **every island's** angular momentum `L_k` is positive for forward and negative for reverse — **all eight flip sign** on time-reversal;
- the population ring angle rotates oppositely (`dφ/dt = +0.0074` forward, `−0.0079` reverse).

The instantaneous readout (Model B) is provably blind to this — forward and reverse have identical per-island power spectra and the identical *set* of overlaps. The island now knows, by itself, which way time is flowing through its edge. That is associative recognition of a **temporal trajectory**, in pure continuous geometry — no recurrent weight matrix, no positional embedding.

**D3 — the wattage meter.** Costs are *assigned* (not measured Joules): field/communication power `∝ |ds|`, spike/maintenance power `∝` spike rate.
- content-update (field) power is **≈ 64× lower** while a percept is held;
- maintenance spike rate is **≈ 83× lower** during a dwell than at a transition.

Energy is **event-driven** — spent almost entirely in the sparse moments when content changes. The held percept is cheap to *communicate* and (here) cheap to *maintain*; in regimes with persistent refresh it would cost maintenance spikes, which is the correct prediction for persistent working-memory activity rather than a bug.

---

## Run it

```bash
pip install numpy matplotlib
python geometric_neuron_v5.py        # prints the verified metrics, writes geometric_neuron_v5.png
python ephaptic_spiking_field_v3.py  # the delay-space step, writes ephaptic_spiking_field_v3.png
```

Both are self-contained reference engines. They print their numbers and save their figures. Nothing is hidden in the figure that the print-out does not also state.

---

## The honest ledger

**Verified in code (measured, not assumed):**
- delay-space readout preserves and sharpens the delta-code (v3: 0.31% sparse, 29× silence; v5: 0.82% sparse, 96% theta-locked, 64× silence);
- temporal-**order** selectivity (v3): forward vs reverse with identical spectra and identical overlap value-set — instantaneous readout blind, delay-space readout reads it;
- native per-island **time's arrow** (v5): every island's angular momentum flips sign on time-reversal; population angular velocity flips sign;
- the wattage structure: content-update power and maintenance spikes are ~10–80× lower during a held dwell than at a transition (event-driven energy).

**Honest corrections forced by the builds:**
- a linear / second-order delay-space readout is power-spectrum-equivalent (Fourier power), hence phase-blind — the **Wiener–Khinchin ceiling**;
- the earlier "topological selectivity" (sine vs square) demonstrated *spectral* selectivity, not phase/orbit detection;
- genuine orbit/order selectivity lives only in **bilinear / higher-order / threshold** terms (the complex observable, `z·z*`, the spike), never in a magnitude term.

**Honestly built-in (not emergent):** the theta clock, the gratings, the directed-edge pairings, the rotating drive of the direction demo, the assigned energy costs. What is *measured* is the delta-code metrics, the order/direction sign-flips, the angular-momentum readout, and the energy partition.

**Still the bet, untouched by any of this:** that the held standing wave is *experienced* rather than merely processed; that Johnson–Nyquist thermal noise is the *medium* of the content rather than the dither it remains in code. Closing the architectural seam makes the engine one consistent object. It does not touch the hard problem; it only locates it more precisely.

---

## Where this points next

- **Winding numbers, not just chirality.** `L_k` gives the *sign* of rotation; the full complex eigenvalue of a per-island transition operator gives the *winding number* and rate — discrete topological labels for sequences, which would make categorical perception (phoneme/colour boundaries) a change of integer winding rather than a continuous slide.
- **Wattage in physical units.** Calibrate `E_spike` and `c_field` against the Attwell–Laughlin budget to turn the silence ratio into a Joules-per-second claim for a neuromorphic implementation.
- **Emergent edges.** The directed-edge pairings are hand-built here; learning them by slow plasticity from the field's own statistics would make the sequence vocabulary emergent rather than assigned.

---

## Lineage & note

Built on the Geometric Neuron / GAIT / Ephaptic Spiking Field series (PerceptionLab). The original insight, the framework, the prior engines, and the direction of the research are Antti Luode's; this build (engines, figures, the synthesis thesis, the honest ledgers) was developed collaboratively with Claude (Opus 4.8).

Review welcome — including from frontier models with a longer view than mine. If you are reading this with fresh eyes: the most useful thing you can do is attack the ledger. Tell us where a "verified" line is actually a built-in, where a "structural claim" is secretly a bet, and where the Wiener–Khinchin ceiling has a second floor we have not noticed yet.

*Do not hype. Do not lie. Just show.*
