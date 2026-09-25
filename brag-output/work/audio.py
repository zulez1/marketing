"""Soundtrack for the brag video: restrained A-minor ambient cue + in-key SFX, one mix."""
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

SR = 48000
DUR = 23.0
N = int(SR * DUR)
BAR = 2.75
BEAT = BAR / 4
EIGHTH = BEAT / 2
rng = np.random.default_rng(7)

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def t_arr(n): return np.arange(n) / SR
def lp(x, fc, order=2): return sosfilt(butter(order, fc, 'low', fs=SR, output='sos'), x)
def hp(x, fc, order=2): return sosfilt(butter(order, fc, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi, order=2): return sosfilt(butter(order, [lo, hi], 'band', fs=SR, output='sos'), x)

def add(buf, x, start, gain=1.0):
    i = int(start * SR)
    if i >= len(buf): return
    x = x[: len(buf) - i]
    buf[i:i + len(x)] += x * gain

# chords (MIDI): Am F C G | Am F G C(add9)
A2, F2, C3, G2 = 45, 41, 48, 43
CHORDS = [
    (A2, [57, 60, 64, 67]),  # Am7
    (F2, [57, 60, 65, 69]),  # Fmaj7
    (C3, [55, 60, 64, 67]),  # C
    (G2, [55, 59, 62, 67]),  # G
    (A2, [57, 60, 64, 67]),
    (F2, [57, 60, 65, 69]),
    (G2, [55, 59, 62, 67]),
    (C3, [55, 60, 62, 64]),  # Cadd9 — lands on the lockup
]
def chord_at(t): return CHORDS[min(int(t // BAR), len(CHORDS) - 1)]

pad = np.zeros(N); bass = np.zeros(N); pluck = np.zeros(N)
kick = np.zeros(N); shaker = np.zeros(N); sfx = np.zeros(N)

# ---------- pad: detuned soft saws, low-passed, overlapping bars ----------
for b, (root, notes) in enumerate(CHORDS):
    start = b * BAR
    length = BAR + (DUR - start - BAR if b == len(CHORDS) - 1 else 0.6)
    n = int(length * SR); t = t_arr(n)
    x = np.zeros(n)
    for m in notes:
        for det in (-0.07, 0.0, 0.07):
            f = hz(m + det)
            for k in range(1, 7):
                x += np.sin(2 * np.pi * f * k * t + rng.uniform(0, 6.28)) / k
    env = np.minimum(1, t / 0.7) * np.minimum(1, (length - t) / 0.6)
    x = lp(x, 900 if b < 7 else 1300) * env
    add(pad, x, start, 1.0)
pad *= np.minimum(1, t_arr(N) / 1.2)  # hook swells in
pad[:int(5.2*SR)] *= 1.35

# ---------- sub bass from bar 2 ----------
for b, (root, _) in enumerate(CHORDS):
    if b < 2: continue
    start = b * BAR
    length = BAR if b < 7 else DUR - start
    n = int(length * SR); t = t_arr(n)
    env = np.minimum(1, t / 0.05) * np.exp(-t * 0.5) * np.minimum(1, (length - t) / 0.3)
    x = np.sin(2 * np.pi * hz(root) * t) + 0.25 * np.sin(2 * np.pi * hz(root + 12) * t)
    add(bass, x * env, start)

# ---------- plucked arpeggio ----------
def pluck_note(m, length=0.9, bright=1.0):
    n = int(length * SR); t = t_arr(n); f = hz(m)
    x = (np.sin(2 * np.pi * f * t) + 0.35 * bright * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 9)
         + 0.12 * bright * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t * 14))
    env = np.minimum(1, t / 0.004) * np.exp(-t * 5.5)
    return x * env

pattern = [0, 2, 1, 3, 2, 1, 3, 2]
t = 0.0; step = 0
while t < 7 * BAR:  # arp through bar 7, bar 8 rings out
    bar = int(t // BAR)
    root, notes = chord_at(t)
    if bar == 0 and step % 2 == 1:  # sparse quarters under the hook
        t += EIGHTH; step += 1; continue
    m = notes[pattern[step % 8]] + 12
    vel = 0.55 if step % 2 else 0.8
    add(pluck, pluck_note(m), t, vel)
    t += EIGHTH; step += 1
# final arpeggio flourish on the lockup chord
for i, m in enumerate([72, 74, 76, 79, 84]):
    add(pluck, pluck_note(m, 2.2), 7 * BAR + i * EIGHTH * 0.5, 0.55 - i * 0.05)

# ---------- soft kick + shaker (scenes 2–4) ----------
def kick_hit(gain=1.0):
    n = int(0.45 * SR); t = t_arr(n)
    f = 45 + 45 * np.exp(-t * 30)
    ph = 2 * np.pi * np.cumsum(f) / SR
    env = np.minimum(1, t / 0.002) * np.exp(-t * 9) * np.minimum(1, (0.45 - t) / 0.05)
    return lp(np.sin(ph) * env, 1800, 4) * gain

for b in range(2, 7):
    for beat in (0, 2):
        add(kick, kick_hit(), b * BAR + beat * BEAT)
add(kick, kick_hit(1.2), 7 * BAR)

sh = hp(rng.standard_normal(int(0.08 * SR)), 6000) * np.exp(-t_arr(int(0.08 * SR)) * 60)
for b in range(2, 7):
    for e in range(8):
        if e % 2 == 1:
            add(shaker, sh, b * BAR + e * EIGHTH, 0.9 if e % 4 == 3 else 0.55)

# ---------- SFX, in key and in the same room ----------
def swell(length=0.55):
    n = int(length * SR); t = t_arr(n)
    x = lp(bp(rng.standard_normal(n), 300, 3200), 2500, 4)
    return x * (t / length) ** 2.5 * np.minimum(1, (length - t) / 0.03)

def bell(m, length=2.0):
    n = int(length * SR); t = t_arr(n); f = hz(m)
    x = (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-t * 6)
         + 0.2 * np.sin(2 * np.pi * 5.4 * f * t) * np.exp(-t * 12))
    return x * np.minimum(1, t / 0.003) * np.exp(-t * 2.4)

def thud():
    n = int(0.9 * SR); t = t_arr(n)
    return np.sin(2 * np.pi * (55 + 25 * np.exp(-t * 18)) * t) * np.exp(-t * 5)

def click():
    n = int(0.12 * SR); t = t_arr(n)
    x = bp(rng.standard_normal(n), 1500, 5000) * np.exp(-t * 90)
    return x * 0.6 + np.sin(2 * np.pi * hz(88) * t) * np.exp(-t * 40) * 0.5

CUTS = [5.2, 10.6, 16.2, 19.4]
for c in CUTS:
    add(sfx, swell(), c - 0.55, 0.22)
# hook: title lands
add(sfx, thud(), 0.25, 0.55); add(sfx, bell(69), 1.3, 0.16)
# logo reveals (scene 2, scene 5)
add(sfx, thud(), 5.45, 0.5); add(sfx, bell(76), 5.5, 0.18)
add(sfx, thud(), 19.7, 0.6); add(sfx, bell(79), 19.7, 0.2)
# three Business Live cards — Am tones rising
for i, m in enumerate([81, 84, 88]):
    add(sfx, bell(m, 1.6), 10.6 + 1.65 + i * 0.55, 0.12)
# spotlight on #03
add(sfx, bell(93, 1.4), 10.6 + 3.9, 0.07)
# claim lines (scene 4) — low, soft
add(sfx, thud(), 16.5, 0.35)
# button click
add(sfx, click(), 19.4 + 2.45, 0.35)

# ---------- mix ----------
def stereo(x, pan=0.0, width=0.0):
    l = x * np.sqrt(0.5 * (1 - pan)); r = x * np.sqrt(0.5 * (1 + pan))
    if width:
        d = int(width * SR); r = np.concatenate([np.zeros(d), r[:-d]])
    return np.stack([l, r])

def norm(x): return x / (np.max(np.abs(x)) + 1e-9)

dry = (stereo(norm(pad) * 0.30, 0, 0.012)
       + stereo(norm(bass) * 0.30)
       + stereo(norm(pluck) * 0.22, 0.15, 0.006)
       + stereo(norm(kick) * 0.40)
       + stereo(norm(shaker) * 0.045, -0.3)
       + stereo(sfx * 0.9, 0, 0.004))
send = (stereo(norm(pluck) * 0.22, 0.15) + stereo(sfx * 0.9) + stereo(norm(pad) * 0.12))

# shared room: decorrelated exponential-noise IR
irn = int(2.4 * SR); it = t_arr(irn)
ir = [lp(rng.standard_normal(irn), 5000) * np.exp(-it * 2.6) for _ in range(2)]
wet = np.stack([fftconvolve(send[i], ir[i])[:N] for i in range(2)])
wet = wet / np.max(np.abs(wet)) * 0.22

mix = dry + wet
mix = hp(mix, 28)
fade = np.ones(N); fl = int(0.6 * SR); fade[-fl:] = np.linspace(1, 0, fl) ** 1.5
mix *= fade
mix = np.tanh(mix * 1.1) / np.tanh(1.1)
mix = mix / np.max(np.abs(mix)) * 0.89
wavfile.write('soundtrack.wav', SR, (mix.T * 32767).astype(np.int16))
print('ok', mix.shape)
