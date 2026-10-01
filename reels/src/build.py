"""Build one reel from a JSON spec: beat-timed shots + overlay graphics + music.

python3 build.py specs/reel1.json

spec: {name, bpm, seed, shots:[{f, in, beats, speed?, z0?, z1?, pan?, flash?}],
       texts:[{b0, b1, lines:[...], kicker?, pos?, style?, max?, uniform?}],
       outro_beats}
Times in the spec are in beats; everything snaps to the music grid.
"""
import json, os, subprocess, sys, shutil
from concurrent.futures import ThreadPoolExecutor
from cut import cut
from music import make_track

SMM = '/home/user/media/smm'
WORK = '/home/user/media/work'
OUT = '/home/user/marketing/reels'

spec = json.load(open(sys.argv[1]))
name = spec['name']; beat = 60.0 / spec['bpm']
NOMUSIC = os.environ.get('NOMUSIC') == '1'
style = 'none' if NOMUSIC else spec.get('style', 'house')
wd = f'{WORK}/{name}'; os.makedirs(wd, exist_ok=True)

# ---- timeline ----
t = 0.0; jobs = []; flashes = []; cuts = []
for i, s in enumerate(spec['shots']):
    d = s['beats'] * beat
    jobs.append((f"{SMM}/{s['f']}", s['in'], d, f'{wd}/s{i:02d}.mp4', s.get('speed', 1.0), s.get('z0', 1.0), s.get('z1', 1.08), s.get('pan', 0.0)))
    if i and s.get('flash'): flashes.append(round(t, 4))
    cuts.append(round(t, 4)); t += d
outro = t
dur = t + spec.get('outro_beats', 8) * beat
# the outro needs footage underneath until the slabs cover it: hold the last shot a little longer
last = list(jobs[-1]); last[2] += 1.2; jobs[-1] = tuple(last)

def run(j):
    if not os.path.exists(j[3]) or os.environ.get('FORCE'):
        cut(*j)
    return j[3]

with ThreadPoolExecutor(3) as ex:
    segs = list(ex.map(run, jobs))
with open(f'{wd}/list.txt', 'w') as fh:
    for s in segs: fh.write(f"file '{s}'\n")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{wd}/list.txt', '-c', 'copy', f'{wd}/footage.mp4'], check=True)

# ---- overlay frames ----
ov = {'dur': dur, 'outro': outro, 'flashes': flashes, 'outroTag': spec.get('outro_tag'),
      'texts': [{**x, 't0': x['b0'] * beat, 't1': x['b1'] * beat} for x in spec['texts']]}
json.dump(ov, open(f'{wd}/overlay.json', 'w'), ensure_ascii=False)
fr = f'{wd}/ov'; shutil.rmtree(fr, ignore_errors=True)
subprocess.run(['node', 'cap_overlay.mjs', f'{wd}/overlay.json', fr], check=True)

# ---- music ----
make_track(f'{wd}/music.wav', spec['bpm'], dur, cuts=cuts[1:], outro=outro, seed=spec.get('seed', 1), flashes=flashes, style=style)

# ---- final ----
os.makedirs(OUT, exist_ok=True)
dst = f'{OUT}/bez-muzyki/{name}-bez-muzyki.mp4' if NOMUSIC else f'{OUT}/{name}.mp4'
os.makedirs(os.path.dirname(dst), exist_ok=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{wd}/footage.mp4', '-framerate', '30', '-i', f'{fr}/f%04d.png', '-i', f'{wd}/music.wav',
                '-filter_complex', '[0:v]tpad=stop_mode=clone:stop_duration=10,scale=in_color_matrix=bt709:in_range=tv,format=gbrp[v];'
                '[1:v]format=rgba[g];[v][g]overlay=format=rgb,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,'
                'setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv[o]',
                '-map', '[o]', '-map', '2:a', '-t', f'{dur:.3f}', '-r', '30',
                '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
                '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
                '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', dst], check=True)
print(dst, round(dur, 2), 's')
