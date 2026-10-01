"""Beat-locked music + in-key hits for a reel. Drive (kick/clap/hats/bass/stabs) until the outro,
then an impact, a ringing chord and a whoosh under the slab wipe."""
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

SR = 48000
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def ta(n): return np.arange(n) / SR
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b, o=2): return sosfilt(butter(o, [a, b], 'band', fs=SR, output='sos'), x)
def norm(x): return x / (np.max(np.abs(x)) + 1e-9)

PROGS = {  # roots and triads, A minor family
    1: [(45, [57, 60, 64]), (41, [57, 60, 65]), (48, [55, 60, 64]), (43, [55, 59, 62])],
    2: [(45, [57, 60, 64]), (43, [55, 59, 62]), (41, [57, 60, 65]), (40, [56, 59, 64])],
    3: [(38, [57, 62, 65]), (45, [57, 60, 64]), (41, [57, 60, 65]), (43, [55, 59, 62])],
    4: [(45, [57, 60, 64]), (45, [57, 60, 64]), (41, [57, 60, 65]), (43, [55, 59, 62])],
}

def make_track(path, bpm, dur, cuts=(), outro=None, seed=1, flashes=()):
    rng = np.random.default_rng(seed)
    beat = 60 / bpm; bar = 4 * beat; N = int(dur * SR) + SR
    prog = PROGS[(seed - 1) % 4 + 1]
    end = outro if outro else dur
    chord = lambda t: prog[int(t // bar) % len(prog)]
    def add(buf, x, t, g=1.0):
        i = int(round(t * SR))
        if 0 <= i < len(buf):
            x = x[: len(buf) - i]; buf[i:i + len(x)] += x * g

    drums = np.zeros(N); bass = np.zeros(N); pad = np.zeros(N); stab = np.zeros(N); sfx = np.zeros(N); duck = np.ones(N)
    def kick(g=1.0):
        n = int(0.4 * SR); t = ta(n)
        ph = 2 * np.pi * np.cumsum(46 + 75 * np.exp(-t * 32)) / SR
        env = np.minimum(1, t / 0.002) * np.exp(-t * 8) * np.minimum(1, (0.4 - t) / 0.04)
        return lp(np.sin(ph) * env, 2500, 4) * g
    def clap():
        n = int(0.25 * SR); t = ta(n); x = bp(rng.standard_normal(n), 900, 4200); env = np.zeros(n)
        for d in (0, 0.011, 0.023): env += np.where(t >= d, np.exp(-(t - d) * 55), 0)
        return x * (env + np.exp(-t * 14) * 0.35) * 0.5
    def hat(o=False):
        n = int((0.16 if o else 0.045) * SR); t = ta(n)
        return lp(hp(rng.standard_normal(n), 7500), 13000) * np.exp(-t * (18 if o else 85))

    nb = int(end // beat)
    for k in range(nb):
        tb = k * beat; b = k // 4; q = k % 4
        add(drums, kick(), tb)
        i = int(tb * SR); m = int(0.28 * SR); duck[i:i + m] = np.minimum(duck[i:i + m], 0.35 + 0.65 * (ta(m) / 0.28) ** 0.8)
        if q in (1, 3): add(drums, clap(), tb, 0.55)
        for s in range(4):
            add(drums, hat(s == 2), tb + s * beat / 4, 0.1 if s == 2 else (0.06 if s % 2 else 0.035))
        # 8th-note bass
        root, _ = chord(tb)
        for e in range(2):
            n = int(beat / 2 * SR); t = ta(n); f = hz(root + (12 if e else 0))
            x = lp(np.sign(np.sin(2 * np.pi * f * t)) * 0.4 + np.sin(2 * np.pi * f * t), 650) * np.minimum(1, t / 0.004) * np.exp(-t * 7)
            add(bass, x, tb + e * beat / 2)
    # fill: snare roll into every 4th bar
    for b in range(3, int(end // bar), 4):
        for s in range(8):
            add(drums, clap(), b * bar + 2 * beat + s * beat / 4, 0.18 + 0.05 * s)

    for b in range(int(np.ceil(dur / bar)) + 1):
        root, notes = prog[b % len(prog)]; st = b * bar
        ln = bar + 0.4; n = int(ln * SR); t = ta(n); x = np.zeros(n)
        for m in notes + [notes[0] + 12]:
            for det in (-0.08, 0.08):
                for kk in range(1, 8): x += np.sin(2 * np.pi * hz(m + det) * kk * t + rng.uniform(0, 6)) / kk
        add(pad, lp(x, 1500) * np.minimum(1, t / 0.1) * np.minimum(1, (ln - t) / 0.3), st)

    def stab_hit(t0, bright=3800, length=0.5):
        _, notes = chord(t0 + 0.01); n = int(length * SR); t = ta(n); x = np.zeros(n)
        for m in notes + [notes[0] + 12]:
            for kk in range(1, 10): x += np.sin(2 * np.pi * hz(m + 12) * kk * t) / kk * (0.7 if kk % 2 else 1)
        return lp(x, bright) * np.minimum(1, t / 0.003) * np.exp(-t * (9 if length < 1 else 1.6))
    def boom():
        n = int(1.4 * SR); t = ta(n)
        return lp(np.sin(2 * np.pi * (38 + 45 * np.exp(-t * 14)) * t) * np.exp(-t * 3.0), 220)
    def riser(L=0.5):
        n = int(L * SR); t = ta(n); return lp(bp(rng.standard_normal(n), 400, 4000), 3800, 4) * (t / L) ** 3
    def whoosh(L=0.6):
        n = int(L * SR); t = ta(n); return lp(bp(rng.standard_normal(n), 300, 6000), 8000) * np.sin(np.pi * t / L) ** 2

    add(sfx, boom(), 0.0, 0.7); add(stab, stab_hit(0.0), 0.0)
    for c in cuts:
        if c >= end: continue
        if c in flashes:
            add(stab, stab_hit(c), c, 1.0); add(sfx, riser(0.45), c - 0.45, 0.14); add(sfx, boom(), c, 0.35)
    if outro:
        add(sfx, whoosh(0.7), outro - 0.15, 0.4); add(sfx, boom(), outro + 0.4, 0.8)
        add(stab, stab_hit(outro + 0.4, 5200, 3.0), outro + 0.4, 1.2)
        tail = int((dur - outro) * SR); i0 = int(outro * SR)
        duck[i0:] = 1

    mix = (np.stack([norm(drums) * 0.55] * 2)
           + np.stack([norm(bass) * 0.33 * duck] * 2)
           + np.stack([norm(pad) * 0.15 * duck, np.roll(norm(pad), 500) * 0.15 * duck])
           + np.stack([norm(stab) * 0.2, np.roll(norm(stab), 380) * 0.2])
           + np.stack([sfx * 0.8] * 2))
    if outro:  # groove stops for the lockup; only the hit and the chord ring out
        i0 = int((outro + 0.4) * SR); g = np.ones(N); g[i0:] = 0
        mix -= np.stack([norm(drums) * 0.55 * (1 - g), norm(drums) * 0.55 * (1 - g)])
        mix -= np.stack([norm(bass) * 0.33 * duck * (1 - g)] * 2)
    irn = int(1.5 * SR); it = ta(irn)
    ir = [lp(rng.standard_normal(irn), 5000) * np.exp(-it * 3.6) for _ in range(2)]
    send = np.stack([norm(stab) * 0.2 + sfx * 0.5] * 2)
    wet = np.stack([fftconvolve(send[c], ir[c])[:N] for c in range(2)])
    mix = mix + wet / (np.max(np.abs(wet)) + 1e-9) * 0.14
    mix = hp(mix, 30)[:, : int(dur * SR)]
    fl = int(0.6 * SR); mix[:, -fl:] *= np.linspace(1, 0, fl) ** 1.5
    mix = np.tanh(mix * 1.4) / np.tanh(1.4); mix = mix / np.max(np.abs(mix)) * 0.89
    wavfile.write(path, SR, (mix.T * 32767).astype(np.int16))
