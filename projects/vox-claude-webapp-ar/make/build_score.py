import numpy as np, wave, struct, os
SR = 48000; DUR = 60.0
N = int(SR*DUR)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(1917)

def put(sig, t, pan=0.0, gain=1.0):
    i = int(t*SR)
    if i < 0: sig = sig[-i:]; i = 0
    n = min(len(sig), N-i)
    if n <= 0: return
    s = sig[:n]*gain
    lg = np.sqrt((1-pan)/2); rg = np.sqrt((1+pan)/2)
    L[i:i+n] += s*lg; R[i:i+n] += s*rg

def env(n, a, d, curve=3.0):
    e = np.ones(n); ai = int(a*SR); di = int(d*SR)
    if ai: e[:ai] = np.linspace(0,1,ai)
    if di: e[-di:] = np.linspace(1,0,di)**curve
    return e

def tone(f, dur, a=0.004, d=None, harm=(1.0,), gain=1.0):
    n = int(dur*SR); t = np.arange(n)/SR
    s = np.zeros(n)
    for k, amp in enumerate(harm, start=1):
        s += amp*np.sin(2*np.pi*f*k*t)
    return s*env(n, a, d if d is not None else dur*0.9)*gain

def noise(dur, a=0.001, d=None, lp=None, hp=None, gain=1.0):
    n = int(dur*SR)
    s = rng.standard_normal(n)
    if lp:  # one-pole lowpass
        al = np.exp(-2*np.pi*lp/SR); y = np.zeros(n); prev = 0.0
        for i in range(n): prev = al*prev + (1-al)*s[i]; y[i] = prev
        s = y
    if hp:
        ah = np.exp(-2*np.pi*hp/SR); y = np.zeros(n); prev = 0.0; px = 0.0
        for i in range(n): prev = ah*(prev + s[i] - px); px = s[i]; y[i] = prev
        s = y
    return s*env(n, a, d if d is not None else dur*0.8)*gain

# ── the bed: a low, breathing drone. no melody, nothing to compete with speech later.
t = np.arange(N)/SR
breath = 0.55 + 0.45*np.sin(2*np.pi*t/13.0)
bed  = 0.030*np.sin(2*np.pi*55.0*t)
bed += 0.016*np.sin(2*np.pi*82.5*t + 0.6)
bed += 0.008*np.sin(2*np.pi*110.0*t + 1.2)
bed *= breath
# a soft sub pulse every 2s — the clock the piece runs on
_pn = int(0.5*SR)
_pulse = 0.022*np.sin(2*np.pi*41.2*np.arange(_pn)/SR)*env(_pn,0.01,0.45,2.0)
for k in range(int(DUR/2.0)+1):
    _i = int(k*2.0*SR)
    _m = min(_pn, N-_i)
    if _m > 0: bed[_i:_i+_m] += _pulse[:_m]
L += bed*0.72; R += bed*0.72


def mix(*sigs):
    """Sum signals of differing lengths by zero-padding to the longest."""
    m = max(len(x) for x in sigs)
    out = np.zeros(m)
    for x in sigs: out[:len(x)] += x
    return out

STAMP = lambda p=1.0: mix(noise(0.022, lp=2600, hp=380, d=0.020, gain=0.30),
                          tone(150*p, 0.030, a=0.0007, d=0.028, gain=0.16))
TICK  = lambda: noise(0.007, hp=3200, d=0.006, gain=0.16)
OFF = dict(sc1=0.0, sc2=4.5, sc3=9.0, sc4=15.5, sc5=22.0,
           sc6=28.0, sc7=35.5, sc8=42.0, sc9=47.5, sc10=55.0)

# sc1 — five words stamping in, then the cursor
for i, ct in enumerate([0.25,0.67,1.09,1.51,1.93]):
    put(STAMP(1.0 + i*0.05), OFF['sc1']+ct, pan=-0.12+i*0.06, gain=0.85)
put(tone(880,0.05,a=0.002,d=0.045,gain=0.09), OFF['sc1']+2.35, 0.3)

# sc2 — box lands, arrow draws, arrowhead, then the strike
put(tone(98,0.22,a=0.002,d=0.20,harm=(1.0,0.3),gain=0.20), OFF['sc2']+0.30, -0.1)
put(noise(0.55, lp=1800, hp=600, a=0.02, d=0.5, gain=0.055), OFF['sc2']+0.45, 0.15)
put(STAMP(0.85), OFF['sc2']+1.00, 0.2)
put(mix(noise(0.26, hp=900, lp=5200, a=0.002, d=0.24, gain=0.26),
        tone(220,0.26,a=0.001,d=0.25,gain=0.10)), OFF['sc2']+2.35, -0.05)

# sc3 — three nodes as three rising tones; segments draw; then the stepped rotation
for i, (ct, f) in enumerate(zip([0.50,1.40,2.30], [392.0, 493.9, 587.3])):
    put(tone(f, 0.42, a=0.003, d=0.40, harm=(1.0,0.22,0.08), gain=0.17),
        OFF['sc3']+ct, pan=[-0.0,0.35,-0.35][i])
    put(STAMP(1.1), OFF['sc3']+ct, gain=0.5)
for i, ct in enumerate([2.55,2.83,3.11]):
    put(noise(0.42, lp=2400, hp=700, a=0.03, d=0.38, gain=0.075), OFF['sc3']+ct, pan=[-0.2,0.2,0.0][i])
for k in range(20):   # one tick per step of the 20-step rotation
    put(TICK(), OFF['sc3']+4.05+k*(1.7/20), pan=np.sin(k/20*2*np.pi)*0.4, gain=0.75)
put(tone(196,0.5,a=0.004,d=0.46,harm=(1.0,0.4),gain=0.13), OFF['sc3']+5.72)

# sc4 — the sweep descends; four files ignite
put(noise(3.6, lp=1500, hp=250, a=0.25, d=2.8, gain=0.065), OFF['sc4']+0.5)
for ct in [1.58,2.07,2.76,3.33]:
    put(mix(tone(1174.7,0.14,a=0.001,d=0.13,gain=0.085), TICK()*1.4), OFF['sc4']+ct, pan=-0.25)

# sc5 — the diff stamps line by line, mechanical and even
for i, ct in enumerate([0.40,0.66,0.92,1.18,1.44,1.70,1.96]):
    put(STAMP(0.9 + (i%3)*0.07), OFF['sc5']+ct, pan=0.18, gain=0.95)

# sc6 — two dull failures, one clean pass
for ct in [0.45,1.45]:
    put(mix(tone(110,0.30,a=0.004,d=0.28,harm=(1.0,0.5,0.2),gain=0.22),
            noise(0.18, lp=900, d=0.17, gain=0.10)), OFF['sc6']+ct, -0.1)
put(tone(659.3,0.75,a=0.004,d=0.70,harm=(1.0,0.3,0.12),gain=0.21), OFF['sc6']+2.25, 0.1)
put(tone(987.8,0.55,a=0.006,d=0.52,gain=0.08), OFF['sc6']+2.30, 0.25)
for i, ct in enumerate([1.07,1.91,2.59]):
    put(TICK(), OFF['sc6']+ct, gain=0.6)

# sc7 — the hero: a swell into the fill, then the bed itself drops away for the hold
put(tone(73.4, 1.5, a=0.9, d=0.55, harm=(1.0,0.55,0.25), gain=0.26), OFF['sc7']+0.6)
put(tone(146.8,0.9,a=0.01,d=0.85,harm=(1.0,0.3),gain=0.14), OFF['sc7']+1.15, -0.15)
put(STAMP(0.7), OFF['sc7']+1.65, gain=1.1)
duck_a, duck_b = int((OFF['sc7']+2.3)*SR), int((OFF['sc7']+6.3)*SR)
ramp = np.concatenate([np.linspace(1,0.12,int(0.5*SR)),
                       np.full(duck_b-duck_a-int(0.5*SR), 0.12)])
L[duck_a:duck_b] *= ramp; R[duck_a:duck_b] *= ramp

# sc8 — 50 tally ticks accelerating, then the highlight
times8 = [0.30,0.68,1.02,1.32,1.60,1.85,2.07,2.27,2.45,2.62,2.76,2.89,3.01,3.12,3.22,3.30,
          3.38,3.45,3.51,3.57,3.62,3.68,3.73,3.79,3.84,3.90,3.95,4.01,4.06,4.12,4.17,4.23,
          4.28,4.34,4.39,4.45,4.50,4.56,4.61,4.67,4.72,4.78,4.83,4.89,4.94,5.00,5.05,5.11,
          5.16,5.22]
for i, ct in enumerate(times8):
    put(TICK(), OFF['sc8']+ct, pan=(i%10-4.5)/9.0, gain=0.55+0.012*i)
put(tone(329.6,0.6,a=0.004,d=0.55,harm=(1.0,0.35),gain=0.19), OFF['sc8']+5.47, 0.0)

# sc9 — the whip, the key press, the snapshot stack sliding
put(noise(0.34, hp=400, lp=7000, a=0.03, d=0.30, gain=0.30), OFF['sc9']-0.06, 0.4)
put(mix(tone(120,0.07,a=0.001,d=0.065,gain=0.17), noise(0.05,hp=2000,d=0.045,gain=0.16)), OFF['sc9']+1.60, 0.3)
put(tone(160,0.05,a=0.001,d=0.045,gain=0.11), OFF['sc9']+1.72, 0.3)
put(noise(0.52, lp=2200, hp=500, a=0.04, d=0.46, gain=0.085), OFF['sc9']+2.10, -0.35)

# sc10 — the close
for i, ct in enumerate([0.45,0.71,0.97,1.23]):
    put(STAMP(0.95), OFF['sc10']+ct, pan=0.0, gain=0.7)
for i, ct in enumerate([1.94,2.22,2.50,2.78]):
    put(STAMP(1.05), OFF['sc10']+ct, pan=0.0, gain=0.95)
put(tone(110,2.6,a=0.02,d=2.4,harm=(1.0,0.5,0.22,0.1),gain=0.24), OFF['sc10']+3.26)
put(tone(164.8,2.2,a=0.05,d=2.1,harm=(1.0,0.3),gain=0.12), OFF['sc10']+3.40)

# tail: fade the last 400ms so the file does not click shut
tail = int(0.4*SR); L[-tail:] *= np.linspace(1,0,tail); R[-tail:] *= np.linspace(1,0,tail)

# normalise with headroom
peak = max(np.abs(L).max(), np.abs(R).max())
g = 0.89/peak
L *= g; R *= g
rms = np.sqrt(np.mean((L**2+R**2)/2))
print(f"peak before norm {peak:.3f} | applied gain {g:.3f} | final RMS {20*np.log10(rms):.1f} dBFS")

inter = np.empty(N*2); inter[0::2] = L; inter[1::2] = R
pcm = (np.clip(inter,-1,1)*32767).astype('<i2')
import os as _os
_PROJ = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
out = _os.path.join(_PROJ, "hyperframes", "assets", "score.wav")
with wave.open(out,'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("wrote", out, os.path.getsize(out), "bytes")
