"""Beat-locked music for a reel, one of four styles, plus in-key hits on accent cuts and an outro
(impact + ringing chord + whoosh under the slab wipe).

styles:
  house     four-on-the-floor, clap, 16th hats, pumping 8th bass, chord stabs        (A minor)
  trap      half-time: 808 with glides, snare on 3, hat rolls and triplets, bell lead (F# minor)
  epic      trailer: taiko/toms, 16th string ostinato, braams on accents, no kick grid (D minor)
  tension   minimal: ticking clock, heartbeat kick, off-beat sub pulse, dark stabs     (C minor)
"""
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

# (root midi, chord tones) per bar
PROGS = {
    'house':   [(45, [57, 60, 64]), (41, [57, 60, 65]), (48, [55, 60, 64]), (43, [55, 59, 62])],          # Am F C G
    'trap':    [(42, [54, 57, 61]), (38, [54, 57, 62]), (45, [52, 57, 61]), (40, [52, 56, 59])],          # F#m D A E
    'epic':    [(38, [50, 53, 57]), (34, [50, 53, 58]), (36, [48, 52, 55]), (33, [49, 52, 57])],          # Dm Bb C A
    'tension': [(36, [48, 51, 55]), (36, [48, 51, 55]), (32, [48, 51, 56]), (35, [47, 50, 55])],          # Cm Cm Ab G
}


class Track:
    def __init__(self, dur, seed):
        self.N = int(dur * SR) + SR
        self.rng = np.random.default_rng(seed)
        self.st = {}           # stem name -> mono buffer
        self.duck = np.ones(self.N)

    def buf(self, name):
        if name not in self.st: self.st[name] = np.zeros(self.N)
        return self.st[name]

    def add(self, name, x, t, g=1.0):
        b = self.buf(name); i = int(round(t * SR))
        if 0 <= i < self.N:
            x = x[: self.N - i]; b[i:i + len(x)] += x * g

    def sidechain(self, t, depth=0.65, ln=0.28):
        i = int(t * SR); m = int(ln * SR)
        if i >= self.N: return
        seg = (1 - depth) + depth * (ta(m) / ln) ** 0.8
        m = min(m, self.N - i); self.duck[i:i + m] = np.minimum(self.duck[i:i + m], seg[:m])

    # ---------- instruments ----------
    def noise(self, n): return self.rng.standard_normal(n)

    def kick(self, f0=46, f1=75, dec=8, L=0.4, click=0.0):
        n = int(L * SR); t = ta(n)
        ph = 2 * np.pi * np.cumsum(f0 + f1 * np.exp(-t * 32)) / SR
        env = np.minimum(1, t / 0.002) * np.exp(-t * dec) * np.minimum(1, (L - t) / 0.04)
        x = np.sin(ph) * env
        if click: x += hp(self.noise(n), 3000) * np.exp(-t * 300) * click
        return lp(x, 2500, 4)

    def clap(self, tight=1.0):
        n = int(0.28 * SR); t = ta(n); x = bp(self.noise(n), 900, 4200); env = np.zeros(n)
        for d in (0, 0.011 * tight, 0.023 * tight): env += np.where(t >= d, np.exp(-(t - d) * 55), 0)
        return x * (env + np.exp(-t * 14) * 0.35) * 0.5

    def snare(self, body=190):
        n = int(0.35 * SR); t = ta(n)
        tone = np.sin(2 * np.pi * body * t) * np.exp(-t * 25)
        nz = bp(self.noise(n), 1500, 9000) * np.exp(-t * 16)
        return (tone * 0.6 + nz) * 0.6

    def hat(self, open_=False, bright=7500):
        n = int((0.16 if open_ else 0.045) * SR); t = ta(n)
        return lp(hp(self.noise(n), bright), 13000) * np.exp(-t * (18 if open_ else 85))

    def tom(self, f=90, L=0.9):
        n = int(L * SR); t = ta(n)
        ph = 2 * np.pi * np.cumsum(f * (1 + 0.6 * np.exp(-t * 18))) / SR
        skin = np.sin(ph) * np.exp(-t * 4.5)
        slap = bp(self.noise(n), 200, 2500) * np.exp(-t * 30) * 0.35
        return lp(skin + slap, 3000)

    def b808(self, f, L, glide_to=None):
        n = int(L * SR); t = ta(n)
        fr = np.full(n, f)
        if glide_to: fr = f + (glide_to - f) * np.clip((t - (L - 0.12)) / 0.1, 0, 1)
        ph = 2 * np.pi * np.cumsum(fr) / SR
        x = np.tanh(np.sin(ph) * 1.8) * np.minimum(1, t / 0.005) * np.exp(-t * 0.9) * np.minimum(1, (L - t) / 0.03)
        return lp(x, 400)

    def pluck(self, m, L=0.5, bright=1.0, dec=6):
        n = int(L * SR); t = ta(n); f = hz(m)
        x = np.sin(2 * np.pi * f * t) + 0.35 * bright * np.sin(4 * np.pi * f * t) * np.exp(-t * 9)
        return x * np.minimum(1, t / 0.003) * np.exp(-t * dec)

    def bell(self, m, L=1.2):
        n = int(L * SR); t = ta(n); f = hz(m)
        x = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-t * 6) + 0.25 * np.sin(2 * np.pi * 5.4 * f * t) * np.exp(-t * 12)
        return x * np.minimum(1, t / 0.002) * np.exp(-t * 3)

    def saw_chord(self, notes, L, cutoff=1500, att=0.08, rel=0.3, detune=0.08, harm=8):
        n = int(L * SR); t = ta(n); x = np.zeros(n)
        for m in notes:
            for det in (-detune, detune):
                for k in range(1, harm): x += np.sin(2 * np.pi * hz(m + det) * k * t + self.rng.uniform(0, 6)) / k
        return lp(x, cutoff) * np.minimum(1, t / att) * np.minimum(1, (L - t) / rel)

    def string_note(self, m, L):
        n = int(L * SR); t = ta(n); x = np.zeros(n)
        for det in (-0.06, 0.0, 0.06):
            for k in range(1, 9): x += np.sin(2 * np.pi * hz(m + det) * k * t + self.rng.uniform(0, 6)) / k
        return lp(x, 2600) * np.minimum(1, t / 0.008) * np.exp(-t * 6)

    def braam(self, notes, L=2.2):
        n = int(L * SR); t = ta(n); x = np.zeros(n)
        for m in notes:
            for det in (-0.1, 0.0, 0.1):
                ph = 2 * np.pi * hz(m - 12 + det) * t
                x += np.sign(np.sin(ph)) * 0.5 + np.sin(ph)
        cut = 300 + 2400 * np.exp(-t * 2.5)
        y = np.zeros(n); seg = 2048
        for s in range(0, n, seg):
            y[s:s + seg] = lp(x[max(0, s - 4096):s + seg], cut[s])[-len(y[s:s + seg]):]
        return np.tanh(y * 0.6) * np.minimum(1, t / 0.01) * np.exp(-t * 1.2)

    def tick(self):
        n = int(0.03 * SR); t = ta(n)
        return (np.sin(2 * np.pi * 3200 * t) + 0.5 * bp(self.noise(n), 2000, 6000)) * np.exp(-t * 260)

    def boom(self):
        n = int(1.4 * SR); t = ta(n)
        return lp(np.sin(2 * np.pi * (38 + 45 * np.exp(-t * 14)) * t) * np.exp(-t * 3.0), 220)

    def riser(self, L=0.5):
        n = int(L * SR); t = ta(n); return lp(bp(self.noise(n), 400, 4000), 3800, 4) * (t / L) ** 3

    def whoosh(self, L=0.6):
        n = int(L * SR); t = ta(n); return lp(bp(self.noise(n), 300, 6000), 8000) * np.sin(np.pi * t / L) ** 2


# ---------------- styles: fill stems up to `end` ----------------
def style_house(T, beat, end, prog):
    bar = 4 * beat; chord = lambda t: prog[int(t // bar) % 4]
    for k in range(int(end // beat)):
        tb = k * beat; q = k % 4
        T.add('drums', T.kick(), tb); T.sidechain(tb)
        if q in (1, 3): T.add('drums', T.clap(), tb, 0.55)
        for s in range(4): T.add('drums', T.hat(s == 2), tb + s * beat / 4, 0.1 if s == 2 else (0.06 if s % 2 else 0.035))
        root, _ = chord(tb)
        for e in range(2):
            n = int(beat / 2 * SR); t = ta(n); f = hz(root + (12 if e else 0))
            T.add('bass', lp(np.sign(np.sin(2 * np.pi * f * t)) * 0.4 + np.sin(2 * np.pi * f * t), 650) * np.minimum(1, t / 0.004) * np.exp(-t * 7), tb + e * beat / 2)
    for b in range(int(np.ceil(end / bar)) + 1):
        T.add('pad', T.saw_chord(prog[b % 4][1] + [prog[b % 4][1][0] + 12], bar + 0.4), b * bar)
    return {'drums': 0.55, 'bass': 0.33, 'pad': 0.15}


def style_trap(T, beat, end, prog):
    bar = 4 * beat; chord = lambda t: prog[int(t // bar) % 4]
    for b in range(int(np.ceil(end / bar))):
        st = b * bar; root, notes = chord(st + 0.01); nroot = chord(st + bar + 0.01)[0]
        # half-time: kick on 1 and the "and" of 2, snare on 3
        for kb in (0, 1.5, 2.75):
            if st + kb * beat < end: T.add('drums', T.kick(42, 60, 6, 0.5, click=0.3), st + kb * beat, 0.8)
        if st + 2 * beat < end: T.add('drums', T.snare(), st + 2 * beat, 0.9); T.add('drums', T.clap(0.7), st + 2 * beat, 0.4)
        # hats: 8ths with a triplet roll at the end of every other bar
        for e in range(8):
            t = st + e * beat / 2
            if t >= end: break
            if b % 2 == 1 and e >= 6:
                for r in range(3): T.add('drums', T.hat(bright=8500), t + r * beat / 6, 0.08)
            else:
                T.add('drums', T.hat(bright=8500), t, 0.09 if e % 2 == 0 else 0.06)
        # 808 sustained, gliding into the next root
        L = min(bar, end - st) - 0.02
        if L > 0.1: T.add('bass', T.b808(hz(root - 12), L, glide_to=hz(nroot - 12)), st, 1.0)
        # bell lead: sparse minor riff
        riff = [notes[2] + 12, notes[0] + 12, notes[1] + 12, notes[0] + 12]
        for i, off in enumerate((0, 0.75, 1.5, 3.0)):
            if st + off * beat < end: T.add('lead', T.bell(riff[i], 0.9), st + off * beat, 0.6)
        T.add('pad', T.saw_chord(notes, bar + 0.3, cutoff=900, detune=0.12, harm=5), st, 1.0)
    return {'drums': 0.62, 'bass': 0.42, 'lead': 0.14, 'pad': 0.07}


def style_epic(T, beat, end, prog):
    bar = 4 * beat; chord = lambda t: prog[int(t // bar) % 4]
    for b in range(int(np.ceil(end / bar))):
        st = b * bar; root, notes = chord(st + 0.01)
        # taiko pattern: 1, 2.5, 3, 4 + low tom
        for tb, f, g in ((0, 70, 1.0), (1.5, 95, 0.6), (2, 70, 0.9), (3, 120, 0.55), (3.5, 120, 0.45)):
            if st + tb * beat < end: T.add('drums', T.tom(f), st + tb * beat, g)
        if b % 2 == 1:
            for r in range(4):
                if st + (3 + r * 0.25) * beat < end: T.add('drums', T.tom(140, 0.4), st + (3 + r * 0.25) * beat, 0.25 + 0.08 * r)
        # 16th string ostinato on root / fifth / octave
        pat = [0, 0, 7, 0, 12, 0, 7, 0]
        for s in range(16):
            t = st + s * beat / 4
            if t >= end: break
            T.add('strings', T.string_note(root + 12 + pat[s % 8], beat / 4 + 0.05), t, 0.9 if s % 4 == 0 else 0.6)
        T.add('pad', T.saw_chord([n - 12 for n in notes] + notes, bar + 0.5, cutoff=1200, att=0.4, rel=0.5), st, 1.0)
        tb_ = ta(int(bar * SR)); T.add('bass', lp(np.sin(2 * np.pi * hz(root) * tb_) * np.exp(-tb_ * 0.8), 200), st, 1.0)
    return {'drums': 0.62, 'strings': 0.22, 'pad': 0.16, 'bass': 0.3}


def style_tension(T, beat, end, prog):
    bar = 4 * beat; chord = lambda t: prog[int(t // bar) % 4]
    for k in range(int(end // beat)):
        tb = k * beat
        # heartbeat kick: lub-dub on 1 and 3
        if k % 2 == 0:
            T.add('drums', T.kick(40, 50, 9, 0.35), tb, 0.85); T.add('drums', T.kick(42, 40, 10, 0.3), tb + beat * 0.28, 0.5)
            T.sidechain(tb, 0.7, 0.35)
        # ticking clock on 8ths, accent on beats
        for e in range(2): T.add('ticks', T.tick(), tb + e * beat / 2, 1.0 if e == 0 else 0.55)
        # off-beat sub pulse
        root, _ = chord(tb)
        n = int(beat / 2 * SR); t = ta(n)
        T.add('bass', lp(np.sin(2 * np.pi * hz(root) * t) + 0.3 * np.sin(4 * np.pi * hz(root) * t), 300) * np.minimum(1, t / 0.01) * np.exp(-t * 6), tb + beat / 2)
        if k >= 8 and k % 4 == 3: T.add('drums', T.clap(1.4), tb, 0.35)
    for b in range(int(np.ceil(end / bar)) + 1):
        root, notes = prog[b % 4]
        # dark drone + a stab on beat 1 and the "and" of 3
        T.add('pad', T.saw_chord([root + 12, root + 19], bar + 0.4, cutoff=500, att=0.6, detune=0.15, harm=6), b * bar)
        for off in (0, 2.5):
            if b * bar + off * beat < end: T.add('lead', T.pluck(notes[0] + 12, 0.35, 1.2, 9) + T.pluck(notes[1] + 12, 0.35, 1.2, 9), b * bar + off * beat, 0.7)
    return {'drums': 0.6, 'ticks': 0.12, 'bass': 0.36, 'pad': 0.16, 'lead': 0.16}


STYLES = {'house': style_house, 'trap': style_trap, 'epic': style_epic, 'tension': style_tension}


def make_track(path, bpm, dur, cuts=(), outro=None, seed=1, flashes=(), style='house'):
    T = Track(dur, seed); beat = 60 / bpm; bar = 4 * beat
    prog = PROGS[style]; end = outro if outro else dur
    chord = lambda t: prog[int(t // bar) % 4]
    gains = STYLES[style](T, beat, end, prog)

    # accents: opening hit, flashed cuts, outro
    def stab(t0, length=0.5, bright=3800):
        _, notes = chord(t0 + 0.01); n = int(length * SR); t = ta(n); x = np.zeros(n)
        for m in notes + [notes[0] + 12]:
            for k in range(1, 10): x += np.sin(2 * np.pi * hz(m + 12) * k * t) / k * (0.7 if k % 2 else 1)
        return lp(x, bright) * np.minimum(1, t / 0.003) * np.exp(-t * (9 if length < 1 else 1.6))
    hit = (lambda t0: T.braam(chord(t0 + 0.01)[1], 1.6)) if style == 'epic' else (lambda t0: stab(t0))
    T.add('sfx', T.boom(), 0.0, 0.7); T.add('stab', hit(0.0), 0.0, 1.0)
    for c in cuts:
        if c in flashes and c < end:
            T.add('stab', hit(c), c, 1.0); T.add('sfx', T.riser(0.45), c - 0.45, 0.14); T.add('sfx', T.boom(), c, 0.35)
    if outro:
        T.add('sfx', T.whoosh(0.7), outro - 0.15, 0.4); T.add('sfx', T.boom(), outro + 0.4, 0.8)
        T.add('stab', stab(outro + 0.4, 3.0, 5200), outro + 0.4, 1.2)
        if style == 'epic': T.add('stab', T.braam(chord(outro + 0.41)[1], 3.0), outro + 0.4, 0.8)

    N = T.N; groove_stop = np.ones(N)
    if outro: groove_stop[int((outro + 0.4) * SR):] = 0; T.duck[int(outro * SR):] = 1
    mix = np.zeros((2, N))
    for name, g in gains.items():
        x = norm(T.buf(name)) * g
        x = x * (T.duck if name in ('bass', 'pad', 'strings', 'lead') else 1)
        if name in ('drums', 'bass', 'ticks', 'strings', 'lead'): x = x * groove_stop
        w = 0 if name in ('drums', 'bass') else 420
        mix += np.stack([x, np.roll(x, w)])
    stab_m = norm(T.buf('stab')) * 0.22; sfx = T.buf('sfx') * 0.8
    mix += np.stack([stab_m, np.roll(stab_m, 380)]) + np.stack([sfx, sfx])
    irn = int(1.6 * SR); it = ta(irn)
    ir = [lp(T.noise(irn), 5000) * np.exp(-it * 3.4) for _ in range(2)]
    send = stab_m + sfx * 0.5 + (norm(T.buf('lead')) * 0.15 if 'lead' in T.st else 0) + (norm(T.buf('strings')) * 0.1 if 'strings' in T.st else 0)
    wet = np.stack([fftconvolve(send, ir[c])[:N] for c in range(2)])
    mix = mix + wet / (np.max(np.abs(wet)) + 1e-9) * 0.15
    mix = hp(mix, 30)[:, : int(dur * SR)]
    fl = int(0.6 * SR); mix[:, -fl:] *= np.linspace(1, 0, fl) ** 1.5
    mix = np.tanh(mix * 1.4) / np.tanh(1.4); mix = mix / np.max(np.abs(mix)) * 0.89
    wavfile.write(path, SR, (mix.T * 32767).astype(np.int16))
