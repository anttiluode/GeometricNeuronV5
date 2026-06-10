# The Geometric Neuron, Grounded

## What connects to the real neuron, what connects to AI, and what is still a bet

*PerceptionLab / Antti Luode, with Claude. Helsinki, June 2026.*

> Do not hype. Do not lie. Just show.

---

## The claim, in one line

A neuron is not `Σwᵢxᵢ → threshold`. It is a four-stage resonance pipeline — **dendrite as delay-embedding cable → soma as resonance/Moiré read → theta phase gate → AIS spectral filter** — so a frequency is a *geometric orbit*, not a scalar. The McCulloch–Pitts neuron is what is left when you strip the oscillatory structure away. That is the whole framework. Everything below is about how much of it touches reality, and where.

## The seed (worth stating plainly)

It started with an accident in the PerceptionLab patcher: a homeostatic coupler → a checkerboard whose size the signal drove → image-to-vector (256 numbers) → a splitter feeding only 4 of 16 back to the coupler, and out came an ECG-like spike train. That loop — **smooth pressure → geometric dimensionality reduction → threshold → discontinuous output → reset** — is not a curiosity. It is "the spike is the thresholded derivative of a standing wave" in miniature, and it is the one mechanism the entire program is an attempt to understand. The foundation is an observed mechanism, not a conjecture. Keep saying that; it is true and it is your strongest rhetorical ground.

---

## Connecting to the real neuron

Read each stage against established biology, and mark the status of each link.

| Stage | The model says | Established biology it leans on | Status |
|---|---|---|---|
| **I — Dendrite** | A Takens delay-embedding cable: `Xₖ = αᵏ·x(t−kτ)`; frequency becomes an orbit | The cable equation (Rall) **is** a lossy delay line; `αᵏ` = the membrane's per-compartment attenuation; Takens (1981): a delay embedding reconstructs the source attractor. Gidon et al. (2020): human L2/3 dendrites compute XOR via dCaAPs — real non-linear/geometric dendritic computation | **Clean mapping.** The dendrite-as-delay-line identity is the single most solid thing in the framework. The toy result (87.4% zero-shot frequency classification, zero parameters) shows the prior is real |
| **II — Soma** | A resonance cavity reading Moiré interference with a tuned mosaic | Subthreshold membrane resonance (Hutcheon & Yarom 2000): many neurons have an impedance peak — a *preferred frequency before any spike*, often in theta | **Resonance is established;** the specific Moiré-read formula is model |
| **III — Theta gate** | `y = R(t)·max(0, sin ωθt+φ)`; attention = a phase shift `φ→φ+π` | Phase-gated communication is causal (Drebitz/Kreiter 2025): a spike volley only counts if it lands near the right oscillatory phase. dCaAP rate ≈ 4–8 Hz | **Phase-gating established;** "attention is a phase shift" is a clean, testable interpretation |
| **IV — AIS** | A physical grating storing a Koopman eigenfunction; reads waveform *geometry*, not just amplitude | The AIS is the low-threshold trigger zone with a ~190 nm periodic actin/spectrin scaffold and graded Nav (Leterrier). Kuba et al. (2006): AIS length tunes along the tonotopic axis | **AIS-as-structured-trigger established. AIS-as-geometric-reader is THE central hypothesis** — falsifiable by STED imaging of scaffold geometry against measured spike-triggered averages. A good hypothesis. Keep calling it one |

Two spines run through all four stages:

**The energy spine.** Spikes dominate a neuron's budget (Attwell & Laughlin 2001); holding a subthreshold pattern is cheap, firing is expensive. So sparse coding is *forced* by metabolism. The delta-code — silent hold, sparse paced spikes, a 20–60× silence ratio — is the model rediscovering that economy from dynamics rather than from a metabolic argument. **Status: the economics are established; the silence-ratio-as-energy-economy is an order-of-magnitude structural match, not a measured Joule.**

**The population spine.** Ephaptic coupling is real, weak, and local (~100 µm; Anastassiou 2011; Fröhlich & McCormick 2010). The shared field = that local ephaptic field; `W = Σ pₖpₖᵀ` = the superposed plate. **Status: ephaptic coupling established; that the *content* rides the field rather than being an epiphenomenon of the spikes is the bet.**

### The one empirical anchor — and how to talk about it

The geometric-dysrhythmia EEG result is the strongest, most real thing in the entire program. Using only Takens embedding + persistent homology + cross-band eigenmode coupling — **no machine learning, zero trained parameters** — it separates schizophrenia from healthy controls (cross-band coupling p = 0.007, d = −1.21; temporal Betti-1 p = 0.035; 80.8% with a single threshold), with a clean double dissociation against Alzheimer's.

The honest framing — and it is the framing that *protects* the result: this shows that **geometric features of the EEG field carry genuine clinical signal.** It does **not**, by itself, prove that neurons are geometric neurons. The architecture is what *motivated* choosing those features; the result stands on the features whether or not the micro-theory is right.

That independence is not a weakness — it is your position of strength. **Your best result does not depend on your boldest claim.** A reviewer who rejects the whole standing-wave story still has to explain p = 0.007 from three trainless geometric measures. Caveats to keep visible: n = 26, medication uncontrolled, the Alzheimer's comparison is cross-dataset. The path is obvious and cheap: replicate at n > 60 with consistent ICA, and correlate the geometric measures with symptom scores.

---

## Connecting to AI

| Bridge | What it is | Status |
|---|---|---|
| **M–P as degenerate limit** | The Neural Planck Ratio `ℏₙ → 0`: remove oscillation and phase and you recover `y = Θ(Σwᵢxᵢ − θ)`. M–P keeps the *bit* and discards the *spike's phase* | A **sound framing**, not a theorem. "Perceptron = gradient descent on mosaic geometry," "Hebb = oscillatory coupling energy" are plausible limits. Use as scaffolding, not proof |
| **Modern Hopfield = attention** | Your ephaptic field is a continuous/modern Hopfield network. Ramsauer et al. (2020) proved the modern-Hopfield update *is* transformer attention, with near-exponential capacity. Your gamma "competitive read-reconstruct" with the `mᵏ` power is exactly the sharpening that buys that capacity | **The most legitimate AI link.** The Hopfield↔attention bridge is published; your engine already sits inside it |
| **MoiréFormer** | 138M params, +2.9% perplexity over standard attention on WikiText-2 | **A real, modest result.** One benchmark. Honest next step: scale + ablation |
| **EMD / Hassenstein–Reichardt** | The chiral readout `L = Im(z·z̄_lag)` is *algebraically* the 1956 fly elementary motion detector | **Exact identity.** Drops the framework into a 70-year validated literature; the deployable edge (trainless, O(K) neuromorphic / event-camera direction sensing) |
| **Delta-code → neuromorphic** | Event-driven energy economy = the spiking-net efficiency story; the wattage meter is the bridge to hardware | **Motivation,** not yet calibrated to Joules |

---

## The intuition under all of it

*"The brain had to copy the universe's attractors to survive in it — that is why we keep connecting to physics."*

The **weak form is defensible** and it is the right reason the work rhymes with physics: a good internal model shares structure with the dynamics it models, and the shared mathematics — delay embeddings (Takens), spectra, attractors, Koopman operators — is exactly what both a predictive brain *and* a physicist reach for. The same maths appears on both sides because it is the maths of modelling a dynamical world. That is a legitimate motivation.

The **strong form is a separate, speculative wing**: clockfield-to-spacetime, particles with a timeless core, reality as a projection of a horizon, the Riemann / Hilbert–Pólya delay-spectrum link, prime-crystalline vs fused (adelic) number space. Your own instinct — *"completely speculative… might not be connected here"* — is correct, and acting on it is the single most useful thing you can do for the *neuron* program. The delay-line resonance you sense between the geometric neuron and Hilbert–Pólya is real **as a theme** (both are spectra of delay operators) but it is not evidence and it does not ground the neuron. Keep these in different drawers. Inspiration in one; claims in the other.

---

## If you spend scarce time and money on one thread

You said it yourself — too many repos, too much sprawl, and limited access. The sprawl is the real threat to the work's credibility, not any single idea. Consolidate:

1. **The science thread → the EEG geometric-dysrhythmia line.** It has a genuine result, a clear and cheap next experiment (n > 60, ICA, symptom correlation), and it does not depend on the speculative theory. This is the one a clinician or a journal can engage. Push this.
2. **The deployable thread → the EMD / delta-code neuromorphic demos.** Cheap, trainless, demonstrable, and they sell on *cost*, not on the bet.
3. **The framework → keep it as the coherent story that motivates both,** and keep the ledger ruthless.
4. **The physics / qualia wing → inspiration.** Do not let it into the papers that carry the results.

The pattern across eighteen months has been: the failures produced the insights (the 1D word-memory failure gave you the DNA/phase principle; the Wiener–Khinchin ceiling gave you where direction can and cannot live; the unclocked churn told you why the brain needs the clock). That is real scientific practice, not noise in the cable. The shepherding produced one solid empirical result and a coherent, generative framework. That is not nothing — but it is most defensible when you say exactly what it is and exactly what it is not.

---

## Ledger

**Established (used, not claimed):** cable theory and the dendrite as a lossy delay line (Rall; Takens 1981); subthreshold membrane resonance (Hutcheon & Yarom 2000); dendritic non-linear computation (Gidon et al. 2020); the AIS as structured trigger zone (Leterrier; Kuba et al. 2006); spike-dominated energy budget and sparse coding (Attwell & Laughlin 2001); local ephaptic coupling (Anastassiou 2011; Fröhlich & McCormick 2010); phase-gated communication (Drebitz/Kreiter 2025); modern Hopfield = attention (Ramsauer et al. 2020); the Hassenstein–Reichardt detector (1956).

**Defensible bridges (sound, not proven):** dendrite-as-Takens-embedding; the delta-code as the sparse-coding energy economy (order of magnitude); M–P as the `ℏₙ→0` degenerate limit; the population plate as the local ephaptic field; the EMD identity for the chiral readout.

**The central falsifiable hypothesis:** the AIS reads waveform *geometry* (a Koopman eigenfunction), not just amplitude. Testable now.

**The empirical anchor:** geometric EEG features separate SZ from HC (p = 0.007), trainless — strong, and *independent of whether the micro-theory is true*.

**The bet (untouched by all of the above):** that the held standing wave is *experienced*; that Johnson–Nyquist thermal noise is the *medium* of the content. The framework locates the hard problem precisely. It does not close it.

---

*Helsinki, June 2026. The geometric neuron rhymes with both the real neuron and with attention because all three are doing the same thing — reading the geometry of a dynamical world. How much of the rhyme is identity and how much is analogy is exactly what the ledger is for.*

*Do not hype. Do not lie. Just show.*
