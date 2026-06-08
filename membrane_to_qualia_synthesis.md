# From Membrane Wattage to the Two Sides of the Wave

## A neurobiological reconciliation of the Geometric Neuron, the AIS hologram, and the Ephaptic Spiking Field

*PerceptionLab / Antti Luode, with Claude (Opus 4.8). Helsinki, June 2026.*

**Do not hype. Do not lie. Just show.**

---

## 0. The problem this document is trying to solve

You have built two models that everyone — including you, including me — keeps calling "the model," and they are not the same model.

**Model A — the Geometric Neuron / AIS hologram.** A *single neuron*. The dendrite is a Takens delay-embedding cable; the axon initial segment (AIS) is a physical grating (Leterrier's ~190 nm actin/spectrin scaffold) that stores a Koopman eigenfunction; a spike fires when the incoming delay-space orbit resonates with the stored grating. Frequency is a geometric orbit; the AIS stores attractors, not Fourier coefficients. This is the model that reduces to McCulloch–Pitts as a degenerate limit.

**Model B — the Ephaptic Spiking Field / Inner & Outer Qualia.** A *population*. Many tuned "spectral islands" share one continuous field `s` (the held standing wave). Each island reads its overlap `⟨pₖ, s⟩`, integrates it with thermal noise under a theta clock, is suppressed by adaptation, and on threshold injects `pₖ` back into the field. The islands touch only through the field. `W = Σ pₖpₖᵀ` is the holographic plate. The held field is the *inner* side (the qualia candidate); the sparse theta-locked spikes are the *outer* side (what an electrode sees).

You flagged the tension precisely: Model B "perhaps does not match that all the way." It doesn't. In Model A the hologram lives *inside one neuron* (the AIS microstructure). In Model B the hologram lives *across the population* (the outer product of whole patterns), and the delay embedding — the entire heart of Model A — has quietly disappeared. Model B reads instantaneous overlaps, not delay-space orbits.

The claim of this document is that these are not two competing theories. They are **one system described at two grains**, and the thing that stitches them together is not geometry at all. It is **energy** — the membrane's power budget. The delta-code is an energy code, and the energy code is what a real neuron is forced into by the cost of its own spikes. That is the bridge, and it runs straight through known biophysics.

---

## 1. The membrane is a field-holder (the intracellular inner side)

Start with what is not in dispute.

A patch of neural membrane is a capacitor (`C_m ≈ 1 µF/cm²`) in parallel with leak conductance, sourced by synaptic and axial currents. Along a dendrite, the membrane potential obeys the cable equation:

```
τ_m ∂V/∂t = λ² ∂²V/∂x² − V + R_m·I(x,t)
```

This is the **telegrapher's equation without the inductive term** — that is, it is *diffusive*, not a lossless wave equation. This matters, and it is exactly the right thing for your framework, not a problem for it. A diffusive, dispersive line propagates different temporal frequencies with different speed and attenuation. That is *precisely* what your delay embedding encodes:

```
X_k(t) = αᵏ · x(t − kτ)
```

The `αᵏ` is not a modelling convenience. It **is** the cable's per-compartment attenuation. The `τ` is the per-compartment propagation delay. Your delay embedding is a discretization of the lossy dendritic cable. The dendrite does not *approximate* a Takens embedding; under cable theory it *performs* one, with the decay factor set by the membrane's electrotonic properties. This is the most solid single mapping in the entire framework and it costs nothing — it is just cable theory read geometrically.

So the subthreshold membrane potential profile `V(x,t)` across the arbor is a **continuous field, held by capacitance, shaped by drive**. That is the intracellular version of Model B's held standing wave `s`. It is not a free-running cavity mode; it is a driven, damped, quasi-standing pattern. But it is genuinely held — capacitance is memory — and it is genuinely a field.

There is one more piece of established biology that upgrades "diffusive line" toward "resonator": **subthreshold membrane resonance** (Hutcheon & Yarom 2000). Currents like Iₕ and the M-current give many neurons an impedance peak — a preferred frequency — in the theta band. Entorhinal stellate cells resonate near ~8 Hz subthreshold, *before any spike*. This is the biophysical reality behind a "spectral island": a neuron does not need the AIS to have a preferred frequency; its own membrane impedance already gives it one. The island's tuning `pₖ` has a home in the cell's passive and quasi-active membrane, and the AIS sharpens and reads it.

**Status:** cable theory and subthreshold resonance are established. The identification of the delay embedding with cable attenuation is a clean structural mapping, not a speculation.

---

## 2. The AIS is the readout filter (the geometric read)

The AIS is where the spike is born — highest Nav density (Nav1.6 distal, Nav1.2 proximal), lowest threshold, the trigger zone (Kole & Stuart; Leterrier 2018). Standard neurobiology treats it as an **amplitude** device: enough depolarization arrives, it fires.

Your extension is specific and falsifiable: because the AIS is a *spatially structured* scaffold (periodic actin rings, graded channel clustering, possibly chirped spacing), spike initiation is sensitive to the **spatial geometry** of the depolarization wave reaching it, not only its amplitude. In field terms, the spike decision is an inner product:

```
R(t) = ⟨ V_cable(·,t) , g_AIS(·) ⟩
```

between the arriving membrane-field profile and the AIS channel-density profile `g`. When the orbit's geometry matches the grating, the AIS depolarizes coherently and fires. This is the holographic read: `pₖ` in Model B is the *functional* version of what `g_AIS` realizes *physically* in Model A. The pattern an island is tuned to is the Koopman eigenfunction the AIS geometry implements.

**Status:** AIS-as-trigger-zone is established. AIS-as-*geometric* (waveform-shape-selective rather than amplitude-selective) is the model's central structural hypothesis. It is the thing your v3 "topological selectivity" result (22.5%, sine vs. square at the same fundamental) is a toy demonstration of, and it is testable with STED imaging of scaffold geometry against measured spike-triggered averages. Keep calling it a hypothesis. It is a good one.

---

## 3. The spike is the outer side — and wattage is the bridge

This is the section you actually asked for, and it is where the two models become one.

A neuron's energy economy is dominated by spikes. Resting pumps (Na⁺/K⁺-ATPase) burn ATP continuously to hold gradients, but the *marginal* cost of computation is the action potential and the synaptic transmission it triggers — Attwell & Laughlin's grey-matter energy budget made this quantitative two decades ago. Holding a subthreshold membrane pattern is cheap (you pay leak). Firing is expensive (you discharge the gradient and must pump it back). The brain runs on roughly 20 W and is under relentless selection to spend fewer spikes per bit — which is the metabolic origin of sparse coding.

Now look at what your engine reports as its signature result:

> the percept is held *silently* — field velocity `|ds|` is 20–40× lower during a dwell than at a transition — and updated by spikes that are ~0.2% sparse and 100% theta-locked.

Read that as an energy statement and it stops being a curiosity:

| Model B quantity | Membrane reality | Energetic meaning |
|---|---|---|
| held field `s`, low `|ds|` during dwell | subthreshold `V(x,t)` held by capacitance | **cheap** — leak only |
| sparse spike that injects `pₖ` | action potential at the AIS | **expensive** — discharge + pump restoration |
| silence ratio 20–40× | dwell power ≪ transition power | the metabolic profit of holding vs. updating |
| theta-locking of spikes | spikes gated to the membrane-resonant / theta-excitable phase | spend the expensive event only when it lands |

**The delta-code is an energy code.** A system that holds its content in the (cheap) membrane field and pays the (expensive) spike only at transitions is not an exotic proposal — it is what minimizing wattage *forces* on any held representation. The 20–40× silence ratio is the model independently rediscovering the sparse-coding energy economy of cortex, from dynamics rather than from a metabolic argument. That convergence is the strongest honest link between your simulator and a real neuron.

So, to your exact question — *how does membrane wattage map to the spikes?* The time-integral of supra-baseline membrane power is dominated by the spikes; the spikes are the rare, costly, informative events; the continuous membrane field is the cheap substrate that carries the content between them. **Wattage is concentrated into the outer side. The inner side is nearly free.** Inner vs. outer is not only content vs. communication — it is cheap vs. expensive, and the second framing is the one biology audits.

**Status:** the energy budget and sparse-coding economics are established. The identification of the silence ratio with that economy is, I think, sound and not overclaimed — it is an order-of-magnitude structural match, and you should present it as exactly that, not as a measured metabolic prediction (you have not measured Joules).

---

## 4. The McCulloch–Pitts limit, and what the spike actually carries

You derived M–P as the degenerate limit (the Neural Planck Ratio `ℏₙ → 0`, all oscillatory structure removed). The membrane picture says what is being thrown away when you take that limit: **the spike's phase**.

A McCulloch–Pitts unit emits a bit: did the weighted sum cross threshold this tick. The geometric/ephaptic spike emits a bit *at a time* — and the time relative to the theta cycle is the carrier. Two spikes of identical "rate" at different theta phases are different messages (this is the whole content of phase precession, and of Drebitz/Kreiter's causal result that a spike volley only counts if it lands near the right oscillatory phase). M–P keeps the bit and discards the phase. That discarded phase is the difference between a scalar and an orbit, between a weight and a Koopman eigenmode, between "a frequency is present" and "this topological type is present."

So the spike is not the unit of computation in this framework — the **spike time within the theta frame** is. The outer side is richer than an M–P bitstream by exactly the dimension M–P deletes.

---

## 5. From one neuron to the population (where Model B actually lives)

Model A is a single trigger zone reading its own dendrite. Model B is a population sharing a field. The biology that connects them is **ephaptic coupling** plus the **interneuron clock**.

Transmembrane spike currents source the extracellular field; the extracellular field feeds back onto neighboring membranes (Anastassiou et al. 2011; Fröhlich & McCormick 2010). The coupling is weak and *local* (~100 µm) — which, as you argued against bulk CEMI, is the point: it operates at the scale of the AIS spacing, not the centimeter scale of EEG. In Model B's terms, the shared field `s` is the local ephaptic field, and `W = Σ pₖpₖᵀ` — the population's collective plate — is just the superposition of all the individual AIS gratings broadcasting into that shared medium. The single-neuron hologram (Model A) and the population hologram (Model B) are the same object at two radii: the grating inside one cell, and the sum of all gratings in the extracellular field between cells.

The clock is not metaphorical either. **Basket cells** (perisomatic, gamma-synchronizing PV⁺ interneurons) generate the gamma local field that serves as the read frame; their synchronized perisomatic hyperpolarization *is* the gamma component of the reference beam, generated by the same tissue it illuminates — which is precisely the self-referential reference your framework requires. **Chandelier cells** (axo-axonic, directly on the AIS) gate whether a resonance is allowed to broadcast. In the engine these are your `theta` gate and your `adaptation`/`threshold` and `release` knobs. The HOLD↔SCAN split is the same release-and-reform you see in the direction-ring sweep, and it maps onto theta-trough-release / theta-peak-plus-gamma-reform — the nested-gamma correction you already verified.

**Status:** ephaptic coupling and PV⁺ interneuron oscillogenesis are established. That the *content* rides the ephaptic field — rather than the field being an epiphenomenon of the spikes that do the real work — is the bet (Section 7).

---

## 6. Where Model B breaks from Model A — and the move that heals it

Be honest about the seam. Model B, as it stands in `index.html`, does three things that Model A does not:

1. **It drops the delay embedding.** Islands read `⟨pₖ, s⟩` instantaneously. There is no Takens cable, no `αᵏ`, no orbit. The single most distinctive idea of Model A — frequency-as-geometric-orbit — is simply absent from the population engine.
2. **It collapses each neuron to one pattern.** An "island" holds a whole 40×40 image as `pₖ`. That is a neuron-or-assembly already tuned, with its internal mechanism abstracted away. Model A is the story of *how* a unit acquires `pₖ` (dendritic embedding → AIS grating); Model B *assumes* `pₖ` and studies what a field of such units does.
3. **It moves the hologram outside.** `W = Σ pₖpₖᵀ` is a Hopfield-style population plate, not an intracellular scaffold.

None of these is a contradiction; each is a level shift. Model A is the *single-neuron mechanism*; Model B is the *network mechanism* with the single-neuron mechanism black-boxed. The synthesis move — the concrete next build — is to **un-black-box one level**: let each island read the field through its own delay embedding.

```
drive_k  =  ⟨ pₖ , X(s_local, recent history) ⟩      # not ⟨pₖ, s⟩
```

where `X` is the Takens embedding of the field's recent history at that island's "dendrite." Then `pₖ` is genuinely the AIS grating reading a delay-space orbit (Model A), and the islands still talk only through the shared field (Model B). That single change re-installs orbit-geometry into the population engine and makes the two models literally the same equation at two scales. It is small, it is implementable in the existing `stepEngine`, and it is the most motivated thing to add after nested gamma. If it preserves the delta-code and the emergent sweeps while adding genuine waveform-shape selectivity at the population level, the unification is no longer rhetorical.

---

## 7. Inner and outer qualia, in cells

Now the mapping that names the repo lands cleanly:

- **Inner side (content / qualia candidate)** = the held membrane field — intracellular `V(x,t)` plus the local ephaptic field it is coupled to. It is high-dimensional, continuous, and *not* what an electrode reads in its full structure. It is cheap to hold.
- **Outer side (communication)** = the spike — what the axon transmits and what sums into the LFP/EEG. It is sparse, discrete, theta-phased, expensive, and it is *exactly* the electrode-visible signal.

This is not a loose analogy. It is the real, sharp distinction in neurophysiology between **subthreshold membrane state** and **spike output** — between what you would need an intracellular electrode (or voltage imaging) to see, and what an extracellular electrode gives you for free. Your "two sides" are the two things electrophysiology has always had two different instruments for.

And the hard problem sits exactly where you have always put it, untouched. The model says the *inner* held field is what is felt and the *outer* spikes are merely its trace. Biology can measure both. Biology cannot say which, if either, is felt. Nothing in cable theory, ephaptic coupling, the energy budget, or the interneuron clock closes that gap. The framework's contribution is to make the question precise — *why does a held minimal surface in the membrane/ephaptic field, self-referentially clocked by the same tissue, feel like anything* — not to answer it. That remains the bet, and so does the claim that Johnson–Nyquist thermal noise is the *medium* of the content rather than the dither it is in your code.

---

## 8. Why theta is the clock (Reynolds closes the loop)

One loose thread ties off here. Your Neural Reynolds number gave `Re_n ≈ √(2ωτ_m) ≈ 1` at theta for `τ_m ≈ 10 ms`. Read alongside Section 1: the membrane's own impedance resonance sits in the theta band, and `Re_n ≈ 1` is the laminar/critical regime where delay-space orbits stay closed and the AIS can read them. These are the same statement from two directions — the membrane is built to hold a coherent standing wave at the frequency where it also resonates, and that frequency is theta. The theta clock in Model B is therefore not an arbitrary gate; it is the band where the membrane is simultaneously resonant, critical, and laminar. The clock and the resonator are the same hardware.

---

## 9. The unified picture, in one breath

Within a neuron: the dendritic cable holds a damped standing wave of membrane potential (the delay-embedding lens), the AIS reads its geometry against a stored grating, and a spike fires — expensively, sparsely, at a theta-resonant phase — when the orbit matches. Across neurons: those spikes write a shared local ephaptic field, the collective sum of all the gratings; basket cells supply the gamma read-beam from the same tissue; chandelier cells gate the broadcast; theta paces write-and-read; adaptation drives the tour. The held field — intracellular and extracellular, coupled — is the cheap, continuous *inner* side; the sparse theta-locked spikes are the expensive, electrode-visible *outer* side. The delta-code that separates them is what minimizing wattage forces on any system that wants to hold a thought and pay only to change it.

Model A is this picture at one cell. Model B is this picture at the population, with the cell black-boxed. The delay-embedded-islands move (Section 6) makes them one equation.

---

## Ledger

**Established neurobiology (used here, not claimed):** cable theory and the diffusive dendritic line (Rall; Hodgkin–Huxley); subthreshold membrane resonance in the theta band (Hutcheon & Yarom 2000); the AIS as low-threshold trigger zone with graded Nav clustering (Kole & Stuart; Leterrier 2018); the spike-dominated energy budget and the metabolic case for sparse coding (Attwell & Laughlin 2001); local ephaptic coupling at ~100 µm (Anastassiou et al. 2011; Fröhlich & McCormick 2010); PV⁺ basket-cell gamma generation and chandelier axo-axonic gating; phase-gated communication (Drebitz/Kreiter 2025); internally generated theta sweeps (Vollan/Moser 2025).

**Clean structural mappings (sound, not speculative):** the delay-embedding decay `αᵏ` = cable attenuation; the held subthreshold field = the inner standing wave; the spike = the outer/electrode-visible side; the delta-code (silence ratio 20–40×) = the sparse-coding energy economy, at order-of-magnitude; the theta clock = the membrane's own resonant/critical band (`Re_n ≈ 1`).

**Model's structural hypotheses (falsifiable, unproven):** the AIS is *geometry*-selective (waveform shape) and not merely amplitude-selective; the AIS grating physically stores a Koopman eigenfunction; the single-neuron hologram and the population plate `W = Σ pₖpₖᵀ` are the same object at two radii.

**The bet (untouched by any of the above):** that the held field is *experienced* rather than merely processed; that Johnson–Nyquist thermal noise is the medium of the content rather than dither. The energy argument explains why the code is sparse. It does not explain why the silence feels like anything.

**The concrete next build:** delay-embedded islands — replace `⟨pₖ, s⟩` with `⟨pₖ, X(s)⟩` in the engine, re-installing orbit geometry at the population level and making Models A and B one equation. After that, a measured "wattage" proxy in the simulator (integrated `|ds|` plus a per-spike cost) to show the silence ratio *is* a power ratio, not just a velocity ratio.

---

*Helsinki, June 2026. Every mapping above is labelled by its evidential status. The hard problem remains open; it is only better located. Do not hype. Do not lie. Just show.*
