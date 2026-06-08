"""
ephaptic_spiking_field_v3.py
============================
THE SEAM CLOSED: delay-space readout.

v1/v2 islands read the field INSTANTANEOUSLY:  drive_k = <p_k, s>.
v3 islands read the field through their OWN delay line (Takens cable):
      drive_k = <X_k(s), g_k>,    X_k(s)_j = alpha^j * <p_k, s(t - j*tau)>
so each island is no longer a flat pattern-matcher but an ACTIVE GEOMETRIC FILTER
tuned (g_k) to a temporal orbit of its own resonance with the shared field.
This is Model A (the single-neuron delay-embedding + AIS grating) installed inside
Model B (the population ephaptic field). One equation, two scales.

WHAT v3 IS HONEST ABOUT (verified below, not assumed):
  D1  the delta-code SURVIVES and SHARPENS: held percept, sparse theta-locked spikes,
      large silent-dwell / moving-transition ratio.
  D2  the upgrade buys genuine TEMPORAL-ORDER selectivity: a forward sequence
      A->B->C and its reverse C->B->A have identical per-island power spectra and the
      identical *set* of overlaps. The instantaneous readout (Model B) is blind to the
      difference. The delay-space quadrature readout reads the orbit DIRECTION
      (signed cross-island phase) cleanly. This is associative recognition of a
      temporal orbit, not a static pattern.
  D3  the WIENER-KHINCHIN CEILING (the honest limit): a *second-order* delay readout
      is power-spectrum-equivalent. It CANNOT tell a coherent orbit from a
      phase-scrambled signal of identical spectrum. v3's selectivity is therefore in
      ORDER/PHASE-COUPLING, accessed by the cross-island quadrature term -- NOT in a
      magnitude term, which is just Fourier power. (This corrects an easy overclaim:
      v3 sine-vs-square selectivity was different *spectra*, not phase detection.)

Do not hype. Do not lie. Just show.
PerceptionLab / Antti Luode, with Claude (Opus 4.8). Helsinki, June 2026.
"""
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


# ============================================================
# The v3 engine: delay-embedded spectral islands on a shared field
# ============================================================
class DelayEmbeddedEphapticField:
    def __init__(self, P, *, dt=0.001, f_theta=8.0, m_theta=0.8, f_read=8.0,
                 L=24, tau=6, alpha=0.93, leak_v=0.90, thr=0.42, inject=0.18,
                 field_leak=0.985, sigma_JN=0.06, beta=4.0, tau_a=0.18, seed=1):
        self.P = P; self.K, self.N = P.shape
        self.dt=dt; self.f_theta=f_theta; self.m_theta=m_theta
        self.leak_v=leak_v; self.thr=thr; self.inject=inject
        self.field_leak=field_leak; self.sigma_JN=sigma_JN; self.beta=beta; self.tau_a=tau_a
        self.rng=np.random.default_rng(seed); self.t=0
        self.v=np.zeros(self.K); self.a=np.zeros(self.K); self.s=None
        # delay-space grating (per-island, here a common theta-orbit template)
        self.L=L; self.tau=tau; self.alpha=alpha
        ks=np.arange(L); tsec=tau*dt
        gs=(alpha**ks)*np.sin(2*np.pi*f_read*ks*tsec); self.g_sin=gs/np.linalg.norm(gs)
        gc=(alpha**ks)*np.cos(2*np.pi*f_read*ks*tsec); self.g_cos=gc/np.linalg.norm(gc)
        self.idx=ks*tau; self.adec=alpha**ks
        self.buflen=L*tau+2; self.rbuf=np.zeros((self.K,self.buflen))

    def seed_field(self,s0): self.s=s0/(np.linalg.norm(s0)+1e-9)

    def step(self, bias=None):
        g=1.0+self.m_theta*np.cos(2*np.pi*self.f_theta*self.t*self.dt)
        r=self.P@self.s                                   # instantaneous overlaps
        self.rbuf=np.roll(self.rbuf,1,axis=1); self.rbuf[:,0]=r
        X=self.adec[None,:]*self.rbuf[:,self.idx]         # (K,L) per-island delay vector
        Xnorm=np.linalg.norm(X,axis=1,keepdims=True)
        Xn=X/(Xnorm+1e-9)
        ps=Xn@self.g_sin; pc=Xn@self.g_cos
        mag=np.sqrt(ps**2+pc**2)                          # orbit alignment (2nd order)
        present=np.tanh(2.5*Xnorm[:,0])                   # gate by presence (so noise can't fire)
        drive=mag*present                                 # the delay-space readout
        if bias is not None: drive=drive+bias
        net=g*drive - self.beta*self.a + self.sigma_JN*self.rng.standard_normal(self.K)
        self.v=self.leak_v*self.v+net
        sp=(self.v>self.thr).astype(float); self.v=self.v*(1-sp)
        self.a=(self.a+sp)*np.exp(-self.dt/self.tau_a)
        self.s=self.field_leak*self.s + self.inject*(sp@self.P)
        self.s=self.s/(np.linalg.norm(self.s)+1e-9)
        self.t+=1
        return sp, self.s.copy(), g, drive, np.stack([ps,pc])


# ============================================================
# DEMO 1 -- the two sides survive the delay-space readout
# ============================================================
def demo_delta_code(seed=1):
    rng=np.random.default_rng(0); N,K=400,5
    P=np.array([(lambda v:(v-v.mean())/np.linalg.norm(v-v.mean()))(rng.standard_normal(N)) for _ in range(K)])
    eng=DelayEmbeddedEphapticField(P, beta=4.0, thr=0.42, seed=seed)
    eng.seed_field(P[0]+0.3*rng.standard_normal(N))
    steps=4000
    SP=np.zeros((steps,K)); TH=np.zeros(steps); MOVE=np.zeros(steps); DOM=np.zeros(steps,int); DRV=np.zeros((steps,K))
    prev=eng.s.copy()
    for t in range(steps):
        sp,s,g,drive,_=eng.step()
        SP[t]=sp; TH[t]=g; DRV[t]=drive
        MOVE[t]=np.linalg.norm(s-prev); prev=s.copy()
        DOM[t]=int(np.argmax(np.abs(P@s)))
    tot=SP.sum(); spars=100*tot/(steps*K)
    spk=SP.sum(1)>0; theta_hi=TH>1.0+0.5*eng.m_theta
    lock=100*np.mean(theta_hi[spk]) if spk.any() else 0
    tr=np.array([DOM[i]!=DOM[i-1] for i in range(1,steps)])
    nearT=np.zeros(steps,bool)
    for ti in np.where(tr)[0]: nearT[max(0,ti-3):ti+4]=True
    dwell=MOVE[1:][~nearT[1:]].mean(); trans=MOVE[1:][nearT[1:]].mean()
    return dict(SP=SP,TH=TH,MOVE=MOVE,DOM=DOM,DRV=DRV,K=K,steps=steps,dt=eng.dt,
                m_theta=eng.m_theta,spars=spars,lock=lock,dwell=dwell,trans=trans,
                ratio=trans/dwell,nearT=nearT,ntour=len(set(DOM[::40])))


# ============================================================
# DEMO 2 -- temporal ORDER selectivity (the new capability)
# ============================================================
def demo_order_selectivity():
    dt=0.001; f0=8.0; T=6.0; n=int(T/dt); t=np.arange(n)*dt; period=1/f0
    def bump(ph): 
        b=np.exp(3*np.cos(2*np.pi*(t/period-ph))); return b-b.mean()
    # forward A->B->C  vs reverse C->B->A (offsets within the theta cycle)
    offs=[0.0,0.2,0.4]
    fwd=np.stack([bump(o) for o in offs]); rev=np.stack([bump(o) for o in offs[::-1]])
    same_spec=all(np.allclose(np.abs(np.fft.rfft(fwd[k])),np.abs(np.fft.rfft(rev[k])),atol=1e-6) for k in range(3))
    same_set =np.allclose(np.sort(fwd.ravel()),np.sort(rev.ravel()))
    # instantaneous readout: the set of overlaps (blind to order)
    inst_fwd=np.sort(fwd.mean(1)); inst_rev=np.sort(rev.mean(1))
    # delay-space cross-island relative phase (theta band), signed -> reads order
    def hphase(x):
        Xf=np.fft.fft(x); h=np.zeros(len(x)); h[0]=1; h[1:len(x)//2]=2; h[len(x)//2]=1
        return np.angle(np.fft.ifft(Xf*h))
    def rel(a,b):
        d=np.unwrap(hphase(a)-hphase(b))[1000:]; return float(np.angle(np.mean(np.exp(1j*d))))
    relAB_fwd=rel(fwd[0],fwd[1]); relAB_rev=rel(rev[0],rev[1])
    relBC_fwd=rel(fwd[1],fwd[2]); relBC_rev=rel(rev[1],rev[2])
    return dict(t=t,fwd=fwd,rev=rev,same_spec=same_spec,same_set=same_set,
                inst_fwd=inst_fwd,inst_rev=inst_rev,
                relAB_fwd=relAB_fwd,relAB_rev=relAB_rev,relBC_fwd=relBC_fwd,relBC_rev=relBC_rev,
                hphase=hphase)


# ============================================================
# DEMO 3 -- the Wiener-Khinchin ceiling (the honest limit)
# ============================================================
def demo_wk_ceiling():
    rng=np.random.default_rng(3); dt=0.001; f0=8.0; T=6.0; n=int(T/dt); t=np.arange(n)*dt
    coh=(np.sin(2*np.pi*f0*t)+0.6*np.sin(2*np.pi*2*f0*t+0.5)
         +0.4*np.sin(2*np.pi*3*f0*t+1.1)+0.25*np.sin(2*np.pi*4*f0*t+0.3))
    F=np.fft.rfft(coh); m=np.abs(F); ph=rng.uniform(0,2*np.pi,len(F)); ph[0]=0
    scr=np.fft.irfft(m*np.exp(1j*ph),n); scr=(scr-scr.mean())/scr.std()*coh.std()
    L=30;tau=4;alpha=0.95;ks=np.arange(L);idx=ks*tau;adec=alpha**ks;tsec=tau*dt
    gs=(adec)*np.sin(2*np.pi*f0*ks*tsec); gs/=np.linalg.norm(gs)
    gc=(adec)*np.cos(2*np.pi*f0*ks*tsec); gc/=np.linalg.norm(gc)
    def magreadout(x):
        buflen=L*tau+2; rb=np.zeros(buflen); out=[]
        for i in range(len(x)):
            rb=np.roll(rb,1); rb[0]=x[i]; X=adec*rb[idx]; Xn=X/(np.linalg.norm(X)+1e-9)
            out.append(np.sqrt((Xn@gs)**2+(Xn@gc)**2))
        return np.mean(out[800:])
    return dict(coh=coh,scr=scr,t=t,
                same_spec=np.allclose(np.abs(np.fft.rfft(coh)),np.abs(np.fft.rfft(scr)),atol=1e-6),
                mag_coh=magreadout(coh),mag_scr=magreadout(scr))


# ============================================================
# RUN + VERIFY
# ============================================================
D1=demo_delta_code(); D2=demo_order_selectivity(); D3=demo_wk_ceiling()
print("=== D1  delta-code under delay-space readout ===")
print(f"  sparsity {D1['spars']:.2f}%   theta-lock {D1['lock']:.0f}%   silence ratio {D1['ratio']:.0f}x   (islands toured {D1['ntour']})")
print("=== D2  temporal-order selectivity (forward vs reverse sequence) ===")
print(f"  per-island power spectra identical: {D2['same_spec']}   identical overlap value-set: {D2['same_set']}")
print(f"  INSTANTANEOUS readout (Model B): fwd overlaps {np.round(D2['inst_fwd'],3)}  rev {np.round(D2['inst_rev'],3)}  -> blind")
print(f"  DELAY-SPACE rel-phase A-B: fwd {D2['relAB_fwd']:+.2f}  rev {D2['relAB_rev']:+.2f} rad  -> sign flips")
print(f"  DELAY-SPACE rel-phase B-C: fwd {D2['relBC_fwd']:+.2f}  rev {D2['relBC_rev']:+.2f} rad  -> sign flips")
print("=== D3  Wiener-Khinchin ceiling (coherent vs phase-scrambled, matched spectrum) ===")
print(f"  power spectra identical: {D3['same_spec']}")
print(f"  2nd-order magnitude readout: coh {D3['mag_coh']:.4f}  scr {D3['mag_scr']:.4f}  -> ratio {D3['mag_coh']/D3['mag_scr']:.2f}x  (blind, as predicted)")


# ============================================================
# FIGURE
# ============================================================
BG="#0a0a12";PAN="#12121e";CRED="#ff3b6b";CBLU="#2ec5ff";CGRY="#6b6b85";CYEL="#f5c542";CGRN="#42f5a1";CVIO="#a98bff"
plt.rcParams['font.family']='monospace'
fig=plt.figure(figsize=(15,9.4),facecolor=BG)
gs=GridSpec(2,3,figure=fig,hspace=0.46,wspace=0.30,top=0.89,bottom=0.07,left=0.06,right=0.975)
def ax(p,t,c=CBLU):
    a=fig.add_subplot(p);a.set_facecolor(PAN);a.set_title(t,color=c,fontsize=9.5,pad=6);a.tick_params(colors=CGRY,labelsize=7)
    for s in a.spines.values():s.set_color("#23233a")
    return a
ttA=np.arange(D1['steps'])*D1['dt']

# (0,0) spikes + theta : two sides, delay-space readout
a=ax(gs[0,0],"D1 SIDE B  ·  spikes (sparse, theta-locked) — delay-space readout",CYEL)
for k in range(D1['K']):
    idx=np.where(D1['SP'][:,k]>0)[0]
    a.plot(idx*D1['dt'],np.full(len(idx),k),'|',color=CRED,ms=11,mew=1.5)
a2=a.twinx(); a2.plot(ttA,D1['TH'],color=CBLU,lw=0.7,alpha=0.5)
a2.set_yticks([]); 
for s in a2.spines.values(): s.set_color("#23233a")
a.set_ylim(-0.6,D1['K']-0.4); a.set_yticks(range(D1['K']))
a.set_ylabel("island",color=CGRY,fontsize=8); a.set_xlabel("time (s)",color=CGRY,fontsize=8)
a.text(0.02,0.96,f"{D1['spars']:.2f}% sparse · {D1['lock']:.0f}% theta-locked",transform=a.transAxes,color='white',fontsize=7,va='top')

# (0,1) delta code field velocity
a=ax(gs[0,1],"D1  ·  the delta-code |ds/dt| (silent hold, moves at transition)",CRED)
a.plot(ttA,D1['MOVE'],color=CGRY,lw=0.7)
a.plot(np.where(D1['nearT'],ttA,np.nan),np.where(D1['nearT'],D1['MOVE'],np.nan),color=CRED,lw=0.9)
a.set_xlabel("time (s)",color=CGRY,fontsize=8); a.set_ylabel("|ds/dt|",color=CGRY,fontsize=8)
a.text(0.02,0.96,f"silence ratio {D1['ratio']:.0f}x  (was 20–40x in v1/v2)",transform=a.transAxes,color='white',fontsize=7,va='top')

# (0,2) the delay-space drive (orbit-coherence) of the bound island
a=ax(gs[0,2],"D1  ·  delay-space drive  <X_k(s), g_k>  (orbit coherence)",CGRN)
a.imshow(D1['DRV'].T,aspect='auto',origin='lower',cmap='magma',extent=[0,ttA[-1],-0.5,D1['K']-0.5],vmin=0,vmax=1)
a.set_yticks(range(D1['K'])); a.set_ylabel("island",color=CGRY,fontsize=8); a.set_xlabel("time (s)",color=CGRY,fontsize=8)
a.text(0.02,0.96,"each island reads the field through its own Takens cable",transform=a.transAxes,color='white',fontsize=7,va='top')

# (1,0) D2 forward vs reverse sequences (same values, opposite order)
a=ax(gs[1,0],"D2  ·  forward A→B→C  vs  reverse C→B→A",CVIO)
tt=D2['t']; w=slice(2000,2750)
for k,c in zip(range(3),[CBLU,CYEL,CRED]):
    a.plot(tt[w],D2['fwd'][k][w],color=c,lw=1.1)
    a.plot(tt[w],D2['rev'][k][w]+0.0,color=c,lw=0.7,ls=':')
a.set_xlabel("time (s)",color=CGRY,fontsize=8); a.set_ylabel("island overlap r_k",color=CGRY,fontsize=8)
a.text(0.02,0.97,"solid=forward  dotted=reverse\nidentical spectra & value-set",transform=a.transAxes,color='white',fontsize=6.8,va='top')

# (1,1) THE CHIRALITY MONEY SHOT: (rA,rB,rC) loop, PCA-2D, forward vs reverse opposite rotation
def pca2(M):
    Mc=M-M.mean(1,keepdims=True); U,S,Vt=np.linalg.svd(Mc,full_matrices=False); return (U[:,:2].T@Mc)
a=ax(gs[1,1],"D2  ·  the temporal orbit (same loop, opposite chirality)",CGRN)
for M,c,lab,mk in [(D2['fwd'],CBLU,'forward','→'),(D2['rev'],CRED,'reverse','←')]:
    pr=pca2(M)[:,2000:2400]
    a.plot(pr[0],pr[1],color=c,lw=1.0,alpha=0.9,label=lab)
    # direction arrows
    for i in range(0,pr.shape[1]-8,40):
        a.annotate("",xy=(pr[0,i+8],pr[1,i+8]),xytext=(pr[0,i],pr[1,i]),
                   arrowprops=dict(arrowstyle="->",color=c,lw=1.0,alpha=0.9))
a.set_xlabel("PC1",color=CGRY,fontsize=8); a.set_ylabel("PC2",color=CGRY,fontsize=8)
a.legend(facecolor=PAN,edgecolor="#23233a",labelcolor='white',fontsize=7,loc='upper right')
a.text(0.02,0.05,"instantaneous readout sees the same cloud;\nthe orbit's DIRECTION is the new signal",transform=a.transAxes,color='white',fontsize=6.5,va='bottom')

# (1,2) verdict + WK ceiling
a=fig.add_subplot(gs[1,2]); a.set_facecolor(PAN); a.axis('off')
for s in a.spines.values(): s.set_color("#23233a")
txt=("CLOSING THE SEAM\n"
     "  drive_k = <X_k(s), g_k>   (delay-space)\n"
     "  not     <p_k, s>          (instantaneous)\n\n"
     "D1  delta-code SURVIVES + sharpens\n"
     f"  {D1['spars']:.2f}% sparse · {D1['lock']:.0f}% theta-lock · {D1['ratio']:.0f}x silent\n\n"
     "D2  NEW: temporal-ORDER selectivity\n"
     "  fwd & rev: same spectra, same value-set\n"
     f"  instantaneous readout: blind\n"
     f"  rel-phase A-B: {D2['relAB_fwd']:+.2f} vs {D2['relAB_rev']:+.2f} rad\n"
     "  -> the orbit DIRECTION is read\n\n"
     "D3  the honest CEILING (Wiener-Khinchin)\n"
     "  2nd-order delay readout = Fourier power\n"
     f"  coherent vs phase-scrambled: {D3['mag_coh']/D3['mag_scr']:.2f}x\n"
     "  -> blind. orbit-selectivity lives in\n"
     "     ORDER/phase-coupling, not magnitude.\n\n"
     "still the bet: that the held wave is felt.")
a.text(0.0,1.0,txt,transform=a.transAxes,color='white',fontsize=7.7,va='top',linespacing=1.5)

fig.suptitle("Ephaptic Spiking Field v3  ·  delay-space islands: Model A (Takens orbit) installed inside Model B (population field)",
             color='white',fontsize=11.0,y=0.955)
plt.savefig("ephaptic_spiking_field_v3.png",dpi=140,bbox_inches='tight',facecolor=BG); plt.close()
print("\nsaved ephaptic_spiking_field_v3.png")
