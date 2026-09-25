"""Soundtrack for the vertical, bolder cut: 120 BPM A-minor drive, cuts hit on the beat."""
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

SR = 48000
DUR = 21.5
N = int(SR * DUR)
BEAT = 0.5
BAR = 2.0
rng = np.random.default_rng(11)

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def ta(n): return np.arange(n) / SR
def lp(x, fc, o=2): return sosfilt(butter(o, fc, 'low', fs=SR, output='sos'), x)
def hp(x, fc, o=2): return sosfilt(butter(o, fc, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def add(buf, x, start, g=1.0):
    i = int(round(start * SR))
    if i >= len(buf): return
    x = x[: len(buf) - i]; buf[i:i + len(x)] += x * g
def norm(x): return x / (np.max(np.abs(x)) + 1e-9)

# Am F C G | Am F C G | Am | C (lockup)
PROG = [(45, [57, 60, 64]), (41, [57, 60, 65]), (48, [55, 60, 64]), (43, [55, 59, 62])] * 2 + [(45, [57, 60, 64]), (48, [55, 60, 64, 67])]
def chord(t): return PROG[min(int(t // BAR), len(PROG) - 1)]
CUTS = [2, 4, 6, 8.5, 11, 13, 16, 18]
END = 18.0  # lockup: groove stops, chord rings

drums = np.zeros(N); bass = np.zeros(N); stab = np.zeros(N); pad = np.zeros(N); arp = np.zeros(N); sfx = np.zeros(N)
duck = np.ones(N)

def kick(g=1.0):
    n = int(0.4 * SR); t = ta(n)
    ph = 2 * np.pi * np.cumsum(48 + 70 * np.exp(-t * 35)) / SR
    env = np.minimum(1, t / 0.002) * np.exp(-t * 8) * np.minimum(1, (0.4 - t) / 0.04)
    return lp(np.sin(ph) * env, 2500, 4) * g
def clap():
    n = int(0.25 * SR); t = ta(n)
    x = bp(rng.standard_normal(n), 900, 4000)
    env = np.zeros(n)
    for d in (0, 0.011, 0.022):
        env += np.where(t >= d, np.exp(-(t - d) * 55), 0)
    env += np.exp(-t * 14) * 0.35
    return x * env * 0.5
def hat(open_=False):
    n = int((0.18 if open_ else 0.05) * SR); t = ta(n)
    return hp(rng.standard_normal(n), 7500) * np.exp(-t * (18 if open_ else 80))

for b in range(9):  # bars 0..8 (0–18s)
    for k in range(4):
        tb = b * BAR + k * BEAT
        add(drums, kick(), tb, 1.0)
        # sidechain duck
        i = int(tb * SR); m = int(0.3 * SR)
        duck[i:i + m] = np.minimum(duck[i:i + m], 0.35 + 0.65 * (ta(m) / 0.3) ** 0.8)
        if b >= 1 and k in (1, 3): add(drums, clap(), tb, 0.55)
        if b >= 2:
            for s in range(4):
                add(drums, hat(s == 2), tb + s * BEAT / 4, 0.10 if s == 2 else (0.07 if s % 2 else 0.04))
add(drums, kick(1.2), END)

# bass: 8th-note pulse, root + octave
for b in range(9):
    root, _ = PROG[b]
    for e in range(8):
        n = int(0.24 * SR); t = ta(n); f = hz(root + (12 if e % 2 else 0))
        x = np.sign(np.sin(2 * np.pi * f * t)) * 0.4 + np.sin(2 * np.pi * f * t)
        x = lp(x, 600) * np.minimum(1, t / 0.004) * np.exp(-t * 7)
        add(bass, x, b * BAR + e * BEAT / 2)
n = int((DUR - END) * SR); t = ta(n)
add(bass, np.sin(2 * np.pi * hz(36) * t) * np.exp(-t * 0.9) * np.minimum(1, (DUR - END - t) / 0.4), END, 0.9)

# pad under everything, ducked
for b, (root, notes) in enumerate(PROG):
    start = b * BAR; length = (BAR + 0.3) if b < len(PROG) - 1 else DUR - start
    n = int(length * SR); t = ta(n); x = np.zeros(n)
    for m in notes + [notes[0] + 12]:
        for det in (-0.08, 0.08):
            for k in range(1, 8):
                x += np.sin(2 * np.pi * hz(m + det) * k * t + rng.uniform(0, 6.28)) / k
    env = np.minimum(1, t / 0.08) * np.minimum(1, (length - t) / 0.3)
    add(pad, lp(x, 1600 if b < len(PROG) - 1 else 2200) * env, start)

# stabs: short bright chord on every cut and on the hook downbeat
def stab_hit(t0):
    _, notes = chord(t0 + 0.01)
    n = int(0.5 * SR); t = ta(n); x = np.zeros(n)
    for m in notes + [notes[0] + 12]:
        f = hz(m + 12)
        for k in range(1, 10):
            x += np.sin(2 * np.pi * f * k * t) / k * (0.7 if k % 2 else 1)
    return lp(x, 3500) * np.minimum(1, t / 0.003) * np.exp(-t * 9)
for c in [0.05] + CUTS:
    add(stab, stab_hit(c), c)

# arp on the lockup
for i, m in enumerate([72, 76, 79, 84, 79, 76, 79, 84]):
    n = int(1.2 * SR); t = ta(n); f = hz(m)
    x = (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t) * np.exp(-t * 10)) * np.minimum(1, t / 0.003) * np.exp(-t * 4)
    add(arp, x, END + 0.25 + i * 0.25, 0.8 - i * 0.06)

# ---------- SFX ----------
def swish(length=0.3):
    n = int(length * SR); t = ta(n)
    x = bp(rng.standard_normal(n), 800, 5000)
    return lp(x, 4500, 4) * np.sin(np.pi * t / length) ** 2
def riser(length=0.5):
    n = int(length * SR); t = ta(n)
    return lp(bp(rng.standard_normal(n), 400, 4000), 3500, 4) * (t / length) ** 3
def boom():
    n = int(1.2 * SR); t = ta(n)
    return np.sin(2 * np.pi * (40 + 40 * np.exp(-t * 12)) * t) * np.exp(-t * 3.2)
def tap():
    n = int(0.1 * SR); t = ta(n)
    return bp(rng.standard_normal(n), 1500, 5000) * np.exp(-t * 90) * 0.6 + np.sin(2 * np.pi * hz(88) * t) * np.exp(-t * 45) * 0.5

for c in CUTS: add(sfx, riser(), c - 0.5, 0.12)
add(sfx, swish(0.28), 2.95, 0.35)            # strike-through "послушать"
add(sfx, swish(0.28), 15.0, 0.35)            # strike-through "3 000 случайных"
for i in range(3): add(sfx, swish(0.3), 11.3 + i * 0.5, 0.28)  # photos fly in
add(sfx, boom(), 0.05, 0.55); add(sfx, boom(), END, 0.7)
add(sfx, tap(), END + 1.9, 0.4)

# ---------- mix ----------
def st(x, pan=0.0, d=0.0):
    l = x * np.sqrt(0.5 * (1 - pan)); r = x * np.sqrt(0.5 * (1 + pan))
    if d:
        k = int(d * SR); r = np.concatenate([np.zeros(k), r[:-k]])
    return np.stack([l, r])

groove_duck = duck.copy(); groove_duck[int(END * SR):] = 1
dry = (st(norm(drums) * 0.55)
       + st(norm(bass) * 0.34 * groove_duck)
       + st(norm(pad) * 0.16 * groove_duck, 0, 0.012)
       + st(norm(stab) * 0.20, 0, 0.008)
       + st(norm(arp) * 0.16, 0.2, 0.006)
       + st(sfx * 0.8, 0, 0.004))
send = st(norm(stab) * 0.2) + st(norm(arp) * 0.16) + st(sfx * 0.6) + st(norm(drums) * 0.05)
irn = int(1.6 * SR); it = ta(irn)
ir = [lp(rng.standard_normal(irn), 5000) * np.exp(-it * 3.5) for _ in range(2)]
wet = np.stack([fftconvolve(send[i], ir[i])[:N] for i in range(2)])
wet = wet / np.max(np.abs(wet)) * 0.16

mix = hp(dry + wet, 30)
fl = int(0.5 * SR); mix[:, -fl:] *= np.linspace(1, 0, fl) ** 1.5
mix = np.tanh(mix * 1.4) / np.tanh(1.4)
mix = mix / np.max(np.abs(mix)) * 0.89
wavfile.write('soundtrack-v.wav', SR, (mix.T * 32767).astype(np.int16))
print('ok')
