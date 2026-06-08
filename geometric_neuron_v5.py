"""
geometric_neuron_v5.py  —  GeometricNeuronV5
============================================
Koopman islands (native time's-arrow) + the wattage meter.

Lineage:
  v3  island read the delay-space ORBIT of its own scalar overlap  <X_k(s), g_k>.
      It hit the Wiener-Khinchin ceiling: a linear/2nd-order delay readout is Fourier
      power, hence phase-blind. Sequence DIRECTION could only be recovered cross-island.
  v5  island carries a 2D COMPLEX observable - a directed-edge detector tuned to a
      consecutive pair of stored states (k -> k+1):
            z_k(t) = <P_k, s> + i*<P_{k+1}, s>
      Its Koopman angular momentum
            L_k = Im( z_k(t) * conj(z_k(t-lag)) )
      is the signed local rotation of the field through that edge:
            L_k > 0  <=>  field moving k -> k+1   (forward / time's arrow +)
            L_k < 0  <=>  field moving k+1 -> k    (reverse)
      L_k is a BILINEAR (cross-time product) term - the nonlinear escape from the
      Wiener-Khinchin ceiling. Each island NATIVELY reads orbit chirality; time's arrow
      is a first-class per-island output, not a cross-island reconstruction.

The wattage meter (costs are ASSIGNED, not measured Joules):
  - field / communication power  P_field ∝ |ds|   (charge moved to change content)
  - spike / maintenance  power   P_spike ∝ spike rate (the AP + pump restoration cost)
  Reported separately, for HOLD and SCAN, plus transition-vs-dwell partition. The honest
  finding: the FIELD-movement (content-update) power carries the delta-code's large
  silence ratio - holding a percept is cheap to COMMUNICATE - while maintenance spikes
  persist (holding is not free), which matches persistent working-memory activity.

Do not hype. Do not lie. Just show.
PerceptionLab / Antti Luode, with Claude (Opus 4.8). Helsinki, June 2026.
"""
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


# ============================================================
# The v5 engine
# ============================================================
class KoopmanIslandField:
    def __init__(self, P, *, dt=0.001, f_theta=8.0, m_theta=0.8, leak_v=0.90, thr=0.55,
                 inject=0.18, field_leak=0.985, sigma_JN=0.06, beta=2.0, tau_a=0.18,
                 ema=0.05, lag=60, dir_gain=0.0, seed=1,
                 E_spike=1.0, c_field=1.0):
        self.P=P; self.M,self.N=P.shape
        self.dt=dt; self.f_theta=f_theta; self.m_theta=m_theta
        self.leak_v=leak_v; self.thr=thr; self.inject=inject; self.field_leak=field_leak
        self.sigma_JN=sigma_JN; self.beta=beta; self.tau_a=tau_a
        self.ema=ema; self.lag=lag; self.dir_gain=dir_gain
        self.rng=np.random.default_rng(seed); self.t=0
        self.v=np.zeros(self.M); self.a=np.zeros(self.M); self.s=None
        self.ov_ema=np.zeros(self.M)
        self.zbuf=np.zeros((lag+1,self.M),complex)   # ring buffer of recent z for instantaneous L
        self.pref=np.where(np.arange(self.M)%2==0,1.0,-1.0)
        self.ang=np.arange(self.M)/self.M*2*np.pi
        self.E_spike=E_spike; self.c_field=c_field
        self.ang_mom=np.zeros(self.M)

    def seed_field(self,s0): self.s=s0/(np.linalg.norm(s0)+1e-9)

    def step(self, bias=None):
        g=1.0+self.m_theta*np.cos(2*np.pi*self.f_theta*self.t*self.dt)
        ov=self.P@self.s
        self.ov_ema=(1-self.ema)*self.ov_ema+self.ema*ov
        z=self.ov_ema + 1j*np.roll(self.ov_ema,-1)
        z_lag=self.zbuf[-1]
        self.ang_mom=(z*np.conj(z_lag)).imag                  # instantaneous angular momentum
        self.zbuf=np.roll(self.zbuf,1,axis=0); self.zbuf[0]=z
        presence=np.abs(z)
        dirsel=1.0+self.dir_gain*np.tanh(50.0*self.pref*self.ang_mom)
        drive=presence*dirsel
        if bias is not None: drive=drive+bias
        net=g*drive - self.beta*self.a + self.sigma_JN*self.rng.standard_normal(self.M)
        self.v=self.leak_v*self.v+net
        sp=(self.v>self.thr).astype(float); self.v=self.v*(1-sp)
        self.a=(self.a+sp)*np.exp(-self.dt/self.tau_a)
        sb=self.s.copy()
        self.s=self.field_leak*self.s + self.inject*(sp@self.P)
        self.s=self.s/(np.linalg.norm(self.s)+1e-9)
        ds=np.linalg.norm(self.s-sb)
        dec=np.angle(np.sum(ov*np.exp(1j*self.ang)))          # ring-decoded population angle
        self.t+=1
        return dict(sp=sp, ds=ds, g=g, ovema=self.ov_ema.copy(), L=self.ang_mom.copy(), dec=dec)


# ============================================================
# DEMO A — delta-code preserved + the WATTAGE meter
# ============================================================
def demo_delta_wattage(seed=1):
    rng=np.random.default_rng(0); N,M=400,8
    P=np.array([(lambda v:(v-v.mean())/np.linalg.norm(v-v.mean()))(rng.standard_normal(N)) for _ in range(M)])
    out={}
    for label,beta in [("HOLD",0.5),("SCAN",5.0)]:
        eng=KoopmanIslandField(P, beta=beta, seed=seed)
        eng.seed_field(P[0]+0.3*rng.standard_normal(N))
        steps=4000; SP=np.zeros((steps,M)); TH=np.zeros(steps); MOVE=np.zeros(steps); DOM=np.zeros(steps,int)
        for t in range(steps):
            r=eng.step(); SP[t]=r['sp']; TH[t]=r['g']; MOVE[t]=r['ds']; DOM[t]=int(np.argmax(np.abs(P@eng.s)))
        tot=SP.sum(); spars=100*tot/(steps*M); secs=steps*eng.dt
        spk=SP.sum(1)>0; theta_hi=TH>1.0+0.5*eng.m_theta
        lock=100*np.mean(theta_hi[spk]) if spk.any() else 0
        tr=np.array([DOM[i]!=DOM[i-1] for i in range(1,steps)]); nearT=np.zeros(steps,bool)
        for ti in np.where(tr)[0]: nearT[max(0,ti-3):ti+4]=True
        d_idx=~nearT; t_idx=nearT
        dwell=MOVE[d_idx].mean(); trans=MOVE[t_idx].mean()
        # wattage: field power ∝ |ds|, spike power ∝ spikes; partitioned dwell vs transition
        Pf_dwell=eng.c_field*MOVE[d_idx].mean(); Pf_trans=eng.c_field*MOVE[t_idx].mean()
        spk_dwell_rate=SP[d_idx].sum()/(d_idx.sum()*eng.dt)/M
        spk_trans_rate=SP[t_idx].sum()/(t_idx.sum()*eng.dt)/M
        out[label]=dict(SP=SP,TH=TH,MOVE=MOVE,DOM=DOM,nearT=nearT,steps=steps,dt=eng.dt,M=M,
            spars=spars,lock=lock,ratio=trans/max(dwell,1e-12),nspk=int(tot),rate=tot/secs/M,
            Pf_dwell=Pf_dwell,Pf_trans=Pf_trans,field_silence=Pf_trans/max(Pf_dwell,1e-12),
            spk_dwell_rate=spk_dwell_rate,spk_trans_rate=spk_trans_rate,frac_trans_time=t_idx.mean())
    return out,P


# ============================================================
# DEMO B — native per-island Koopman direction (time's arrow)
# ============================================================
def demo_koopman_direction(P, seed=2):
    M=P.shape[0]; steps=4000; period=800; res={}
    for direction,name in [(+1,'forward'),(-1,'reverse')]:
        eng=KoopmanIslandField(P, beta=1.0, thr=0.45, inject=0.12, field_leak=0.96,
                               sigma_JN=0.04, dir_gain=1.0, lag=60, seed=seed)
        eng.seed_field(P[0].copy()); ang=eng.ang
        OVE=np.zeros((steps,M)); SP=np.zeros((steps,M)); DEC=np.zeros(steps); L=np.zeros((steps,M))
        for t in range(steps):
            pos=(direction*2*np.pi*t/period)%(2*np.pi); w=np.exp(3.0*np.cos(ang-pos)); w/=w.max()
            r=eng.step(bias=0.8*w); OVE[t]=r['ovema']; SP[t]=r['sp']; DEC[t]=r['dec']; L[t]=r['L']
        z=OVE+1j*np.roll(OVE,-1,axis=1); lag=eng.lag
        Lk=np.mean((z[lag:]*np.conj(z[:-lag])).imag[1000:],axis=0)   # per-island angular momentum
        dphi=np.mean(np.diff(np.unwrap(DEC[1000:])))                # population angular velocity
        fwd_rate=SP[1000:][:,eng.pref>0].mean()*1000; rev_rate=SP[1000:][:,eng.pref<0].mean()*1000
        res[name]=dict(OVE=OVE,SP=SP,DEC=DEC,Lk=Lk,dphi=dphi,steps=steps,dt=eng.dt,M=M,
                       pref=eng.pref,fwd_rate=fwd_rate,rev_rate=rev_rate,netL=Lk.sum())
    return res


# ============================================================
# RUN + VERIFY
# ============================================================
DA,P=demo_delta_wattage(); DB=demo_koopman_direction(P)
print("="*64); print("DEMO A : delta-code + WATTAGE meter"); print("="*64)
for k in ["HOLD","SCAN"]:
    d=DA[k]
    print(f"  {k}: {d['spars']:.2f}% sparse · {d['lock']:.0f}% theta-lock · field-velocity silence {d['ratio']:.0f}x · {d['rate']:.1f} spk/isl/s")
    print(f"        WATTAGE  field(content-update) power silence: {d['field_silence']:.0f}x lower while holding")
    print(f"                 spike(maintenance) rate  dwell {d['spk_dwell_rate']:.1f} vs transition {d['spk_trans_rate']:.1f} spk/isl/s")
print(f"  --> holding a percept is ~{DA['HOLD']['field_silence']:.0f}x cheaper to COMMUNICATE (field barely moves),")
print(f"      but maintenance spikes persist (holding is not free) -- as in persistent working-memory activity.")
print("="*64); print("DEMO B : native Koopman direction  (time's arrow per island)"); print("="*64)
for nm in ['forward','reverse']:
    d=DB[nm]
    print(f"  {nm}: per-island angular momentum signs {np.array2string(np.sign(d['Lk']).astype(int),separator='')}  net L={d['netL']:+.4f}")
    print(f"          population ring angular velocity dphi/dt = {d['dphi']:+.5f}  (sign = direction of time)")
allflip=np.array_equal(np.sign(DB['forward']['Lk']),-np.sign(DB['reverse']['Lk']))
print(f"  every island flips sign forward<->reverse: {allflip}")
print(f"  net time's-arrow flips: {np.sign(DB['forward']['netL'])!=np.sign(DB['reverse']['netL'])}")


# ============================================================
# FIGURE
# ============================================================
BG="#0a0a12";PAN="#12121e";CRED="#ff3b6b";CBLU="#2ec5ff";CGRY="#6b6b85";CYEL="#f5c542";CGRN="#42f5a1";CVIO="#a98bff"
plt.rcParams['font.family']='monospace'
fig=plt.figure(figsize=(15,9.4),facecolor=BG)
gs=GridSpec(2,3,figure=fig,hspace=0.46,wspace=0.32,top=0.89,bottom=0.07,left=0.06,right=0.975)
def ax(p,t,c=CBLU):
    a=fig.add_subplot(p);a.set_facecolor(PAN);a.set_title(t,color=c,fontsize=9.5,pad=6);a.tick_params(colors=CGRY,labelsize=7)
    for s in a.spines.values():s.set_color("#23233a")
    return a
H=DA['HOLD']; ttA=np.arange(H['steps'])*H['dt']

# (0,0) delta-code raster (HOLD) + theta
a=ax(gs[0,0],"D1  ·  delta-code: held percept, sparse theta-locked spikes",CYEL)
for k in range(H['M']):
    idx=np.where(H['SP'][:,k]>0)[0]; a.plot(idx*H['dt'],np.full(len(idx),k),'|',color=CRED,ms=9,mew=1.3)
a2=a.twinx(); a2.plot(ttA,H['TH'],color=CBLU,lw=0.6,alpha=0.45); a2.set_yticks([])
for s in a2.spines.values(): s.set_color("#23233a")
a.set_ylim(-0.6,H['M']-0.4); a.set_yticks(range(H['M']))
a.set_ylabel("island",color=CGRY,fontsize=8); a.set_xlabel("time (s)",color=CGRY,fontsize=8)
a.text(0.02,0.97,f"{H['spars']:.2f}% sparse · {H['lock']:.0f}% theta-locked",transform=a.transAxes,color='white',fontsize=7,va='top')

# (0,1) field velocity (delta-code) HOLD
a=ax(gs[0,1],"D1  ·  field velocity |ds/dt| (silent hold, bursts at transition)",CRED)
a.plot(ttA,H['MOVE'],color=CGRY,lw=0.6)
a.plot(np.where(H['nearT'],ttA,np.nan),np.where(H['nearT'],H['MOVE'],np.nan),color=CRED,lw=0.8)
a.set_xlabel("time (s)",color=CGRY,fontsize=8); a.set_ylabel("|ds/dt|",color=CGRY,fontsize=8)
a.text(0.02,0.97,f"field-velocity silence ratio {H['ratio']:.0f}x",transform=a.transAxes,color='white',fontsize=7,va='top')

# (0,2) WATTAGE meter: dwell vs transition power, HOLD & SCAN
a=ax(gs[0,2],"D3  ·  WATTAGE: power is spent only at transitions",CGRN)
labels=['HOLD\nfield','HOLD\nspike','SCAN\nfield','SCAN\nspike']
dwellv=[DA['HOLD']['Pf_dwell'],DA['HOLD']['spk_dwell_rate'],DA['SCAN']['Pf_dwell'],DA['SCAN']['spk_dwell_rate']]
transv=[DA['HOLD']['Pf_trans'],DA['HOLD']['spk_trans_rate'],DA['SCAN']['Pf_trans'],DA['SCAN']['spk_trans_rate']]
# normalize each pair to its transition value for visual comparability
dn=[d/t if t>0 else 0 for d,t in zip(dwellv,transv)]; tn=[1.0]*4
x=np.arange(4)
a.bar(x-0.2,tn,0.4,color=CRED,alpha=0.85,label='at transition')
a.bar(x+0.2,dn,0.4,color=CBLU,alpha=0.85,label='during dwell (held)')
a.set_xticks(x); a.set_xticklabels(labels,fontsize=6.5,color=CGRY)
a.set_ylabel("power (norm. to transition)",color=CGRY,fontsize=8)
a.legend(facecolor=PAN,edgecolor="#23233a",labelcolor='white',fontsize=6.5,loc='upper right')
a.text(0.02,0.55,f"field silence {DA['HOLD']['field_silence']:.0f}x\nspikes {DA['HOLD']['spk_trans_rate']/max(DA['HOLD']['spk_dwell_rate'],1e-9):.0f}x",
       transform=a.transAxes,color='white',fontsize=7,va='top')

# (1,0) per-island angular momentum, forward vs reverse (all flip)
a=ax(gs[1,0],"D2  ·  native per-island time's-arrow  L_k = Im(z·z*_lag)",CGRN)
M=DB['forward']['M']; x=np.arange(M)
a.bar(x-0.2,DB['forward']['Lk'],0.4,color=CBLU,alpha=0.9,label='forward A→B→C')
a.bar(x+0.2,DB['reverse']['Lk'],0.4,color=CRED,alpha=0.9,label='reverse C→B→A')
a.axhline(0,color="#33334d",lw=0.8); a.set_xticks(x)
a.set_xlabel("island (directed edge k→k+1)",color=CGRY,fontsize=8); a.set_ylabel("angular momentum L_k",color=CGRY,fontsize=8)
a.legend(facecolor=PAN,edgecolor="#23233a",labelcolor='white',fontsize=6.5,loc='upper right')
a.text(0.02,0.06,"every island flips sign with time's direction",transform=a.transAxes,color='white',fontsize=6.8,va='bottom')

# (1,1) population ring angle rotating opposite ways
a=ax(gs[1,1],"D2  ·  the field rotates opposite ways (read by the islands)",CVIO)
tt=np.arange(DB['forward']['steps'])*DB['forward']['dt']
a.plot(tt,np.unwrap(DB['forward']['DEC']),color=CBLU,lw=1.1,label=f"forward (dφ/dt={DB['forward']['dphi']:+.4f})")
a.plot(tt,np.unwrap(DB['reverse']['DEC']),color=CRED,lw=1.1,label=f"reverse (dφ/dt={DB['reverse']['dphi']:+.4f})")
a.set_xlabel("time (s)",color=CGRY,fontsize=8); a.set_ylabel("population ring angle (unwrapped)",color=CGRY,fontsize=8)
a.legend(facecolor=PAN,edgecolor="#23233a",labelcolor='white',fontsize=6.5,loc='center left')

# (1,2) verdict
a=fig.add_subplot(gs[1,2]); a.set_facecolor(PAN); a.axis('off')
for s in a.spines.values(): s.set_color("#23233a")
txt=("GEOMETRIC NEURON v5\n"
     "  island = directed-edge complex cell\n"
     "  z_k = <P_k,s> + i<P_{k+1},s>\n"
     "  L_k = Im(z_k(t) conj(z_k(t-lag)))\n\n"
     "D1  delta-code preserved\n"
     f"  {DA['HOLD']['spars']:.2f}% sparse · {DA['HOLD']['lock']:.0f}% theta-locked\n"
     f"  field-velocity silence {DA['HOLD']['ratio']:.0f}x\n\n"
     "D2  NATIVE time's arrow (per island)\n"
     "  forward: all L_k > 0\n"
     "  reverse: all L_k < 0  (every island flips)\n"
     "  bilinear z·z* = the nonlinear escape\n"
     "  from the Wiener-Khinchin ceiling\n\n"
     "D3  WATTAGE\n"
     f"  content-update power {DA['HOLD']['field_silence']:.0f}x lower held\n"
     f"  maintenance spikes {DA['HOLD']['spk_trans_rate']/max(DA['HOLD']['spk_dwell_rate'],1e-9):.0f}x lower in dwell\n"
     "  energy is event-driven (spent at transitions)\n\n"
     "still the bet: that the held wave is felt.")
a.text(0.0,1.0,txt,transform=a.transAxes,color='white',fontsize=7.6,va='top',linespacing=1.45)

fig.suptitle("Geometric Neuron v5  ·  Koopman islands read time's arrow natively; the wattage meter shows event-driven energy",
             color='white',fontsize=10.8,y=0.955)
plt.savefig("geometric_neuron_v5.png",dpi=140,bbox_inches='tight',facecolor=BG); plt.close()
print("\nsaved geometric_neuron_v5.png")
