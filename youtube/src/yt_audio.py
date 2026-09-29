"""Sound for the YouTube intro, stinger and outro: whooshes on every slab wave,
an impact + A-minor stab on the logo, shimmer on the glint, calm bed for the end screen."""
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

SR = 48000
rng = np.random.default_rng(3)
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def ta(n): return np.arange(n) / SR
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b, o=2): return sosfilt(butter(o, [a, b], 'band', fs=SR, output='sos'), x)
def add(buf, x, t, g=1.0):
    i = int(t * SR)
    if i >= buf.shape[-1]: return
    x = x[..., : buf.shape[-1] - i]; buf[..., i:i + x.shape[-1]] += x * g
def norm(x): return x / (np.max(np.abs(x)) + 1e-9)

def whoosh(length=0.55, pan=1.0):
    """noise swept through a moving band-pass, panned left→right with the slabs"""
    n = int(length * SR); t = ta(n); x = rng.standard_normal(n)
    out = np.zeros(n); seg = 512
    for s in range(0, n, seg):
        p = s / n; fc = 400 + 5200 * np.sin(np.pi * p) ** 1.5
        out[s:s + seg] = bp(x[max(0, s - 2048):s + seg], fc * 0.6, min(fc * 1.6, 20000))[-len(out[s:s + seg]):]
    env = np.sin(np.pi * t / length) ** 2
    y = lp(out * env, 9000)
    pos = np.clip(t / length, 0, 1) * 2 - 1  # -1 → 1
    L = y * np.sqrt(0.5 * (1 - pos * pan)); R = y * np.sqrt(0.5 * (1 + pos * pan))
    return np.stack([L, R])

def impact():
    n = int(1.6 * SR); t = ta(n)
    sub = np.sin(2 * np.pi * (38 + 60 * np.exp(-t * 20)) * t) * np.exp(-t * 3.0)
    crack = hp(rng.standard_normal(n), 2000) * np.exp(-t * 40) * 0.25
    y = lp(sub, 200) + crack
    return np.stack([y, y])

def stab(notes=(57, 60, 64, 71), length=2.4, bright=5000):
    n = int(length * SR); t = ta(n); x = np.zeros(n)
    for m in notes:
        for det in (-0.06, 0.06):
            for k in range(1, 10):
                x += np.sin(2 * np.pi * hz(m + 12 + det) * k * t) / k
    y = lp(x, bright) * np.minimum(1, t / 0.004) * (0.35 * np.exp(-t * 7) + 0.65 * np.exp(-t * 1.3))
    return np.stack([y, np.roll(y, int(0.008 * SR))])

def shimmer(start_note=81, count=6, gap=0.06):
    n = int(2.2 * SR); out = np.zeros((2, n))
    for i, m in enumerate([start_note, start_note + 3, start_note + 7, start_note + 12, start_note + 15, start_note + 19][:count]):
        k = int(1.6 * SR); t = ta(k); f = hz(m)
        y = (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-t * 8)) * np.minimum(1, t / 0.003) * np.exp(-t * 3.5)
        pan = -0.6 + 1.2 * i / max(1, count - 1)
        add(out, np.stack([y * np.sqrt(0.5 * (1 - pan)), y * np.sqrt(0.5 * (1 + pan))]), i * gap, 0.8 - i * 0.08)
    return out

def reverb(x, secs=1.8, decay=3.0, wet=0.25):
    irn = int(secs * SR); it = ta(irn)
    ir = [lp(rng.standard_normal(irn), 6000) * np.exp(-it * decay) for _ in range(2)]
    w = np.stack([fftconvolve(x[i], ir[i])[: x.shape[1]] for i in range(2)])
    return x + w / (np.max(np.abs(w)) + 1e-9) * np.max(np.abs(x)) * wet

def master(x, fade_out=0.0, peak=0.89):
    x = hp(x, 28)
    if fade_out:
        k = int(fade_out * SR); x[:, -k:] *= np.linspace(1, 0, k) ** 1.5
    x = np.tanh(x * 1.2) / np.tanh(1.2)
    return x / np.max(np.abs(x)) * peak

def write(name, x): wavfile.write(name, SR, (x.T * 32767).astype(np.int16))

# ---------------- intro (6 s) ----------------
N = int(6.0 * SR); a = np.zeros((2, N))
add(a, whoosh(0.7), 0.0, 0.55)                    # wave 1 sweeps in
add(a, impact(), 0.62, 0.9)                       # logo lands
add(a, stab(), 0.62, 0.35)
add(a, shimmer(), 1.85, 0.18)                     # glint across the word
pad_n = int(4.2 * SR); t = ta(pad_n); pad = np.zeros(pad_n)
for m in (45, 57, 60, 64, 67):
    for det in (-0.08, 0.08):
        pad += np.sin(2 * np.pi * hz(m + det) * t) + 0.3 * np.sin(4 * np.pi * hz(m + det) * t)
pad = lp(pad, 1400) * np.minimum(1, t / 0.6) * np.minimum(1, (4.2 - t) / 0.5)
add(a, np.stack([pad, np.roll(pad, 300)]), 0.8, 0.05)
add(a, whoosh(0.6), 4.35, 0.6)                    # wave 2 covers
add(a, whoosh(0.6, pan=-1), 5.05, 0.5)            # and clears
add(a, stab((57, 60, 64, 69), 1.0, 7000), 4.8, 0.18)
write('../intro.wav', master(reverb(a), fade_out=0.15))

# ---------------- stinger (1.6 s) ----------------
N = int(1.6 * SR); s = np.zeros((2, N))
add(s, whoosh(0.5), 0.0, 0.6)
add(s, impact(), 0.45, 0.6)
add(s, stab((57, 60, 64, 71), 1.2, 6000), 0.45, 0.28)
add(s, whoosh(0.5, pan=-1), 0.95, 0.5)
write('../stinger.wav', master(reverb(s, 1.2, 4.0, 0.2), fade_out=0.1))

# ---------------- outro (20 s) ----------------
N = int(20.0 * SR); o = np.zeros((2, N))
add(o, whoosh(0.7), 0.0, 0.5)
add(o, impact(), 0.6, 0.6)
add(o, stab(), 0.6, 0.25)
add(o, shimmer(76), 1.8, 0.12)
BAR = 2.75
prog = [(45, [57, 60, 64, 67]), (41, [57, 60, 65, 69]), (48, [55, 60, 64, 67]), (43, [55, 59, 62, 67])] * 2
bed = np.zeros(N); pl = np.zeros(N)
for b, (root, notes) in enumerate(prog):
    st = 0.6 + b * BAR; ln = BAR + 0.6; n = int(ln * SR); t = ta(n); x = np.zeros(n)
    for m in notes + [root + 12]:
        for det in (-0.07, 0.07):
            for k in range(1, 6): x += np.sin(2 * np.pi * hz(m + det) * k * t + rng.uniform(0, 6)) / k
    add(bed, lp(x, 900) * np.minimum(1, t / 0.8) * np.minimum(1, (ln - t) / 0.6), st)
    for e in range(8):   # soft plucks on eighths
        k = int(0.9 * SR); tt = ta(k); f = hz(notes[[0, 2, 1, 3, 2, 1, 3, 2][e]] + 12)
        y = np.sin(2 * np.pi * f * tt) * np.minimum(1, tt / 0.004) * np.exp(-tt * 5.5)
        add(pl, y, st + e * BAR / 8, 0.8 if e % 2 == 0 else 0.55)
o += np.stack([norm(bed) * 0.22, np.roll(norm(bed), 500) * 0.22])
o += np.stack([norm(pl) * 0.12, np.roll(norm(pl), 250) * 0.12])
write('../outro.wav', master(reverb(o, 2.2, 2.6, 0.3), fade_out=0.8))
print('ok')
