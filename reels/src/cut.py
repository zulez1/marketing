"""Cut one shot from an iPhone HLG clip into a graded 1080x1920 / 30 fps SDR segment.

usage (as module): cut(src, start, out_dur, dst, speed=1.0, z0=1.0, z1=1.08, pan=0.0)
  speed  < 1 = slow motion (sources are ~60 fps, so 0.5 stays smooth)
  z0,z1  zoom at the first / last frame (1.0 = fills the frame); punch-ins and pull-outs
  pan    horizontal offset of the crop, -1 (left) .. 1 (right), useful for landscape sources
"""
import subprocess, sys

W, H = 1080, 1920
BASE_H = 2208               # 15% headroom over 1920 for zooming
BASE_W = round(BASE_H * 9 / 16 / 2) * 2   # 1242

GRADE = "eq=contrast=1.07:saturation=1.18:gamma=0.97,unsharp=5:5:0.35"
TONEMAP = ("zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
           "tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")


def is_hdr(src):
    tr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=color_transfer',
                         '-of', 'csv=p=0', src], capture_output=True, text=True).stdout.strip()
    return tr in ('arib-std-b67', 'smpte2084')


def cut(src, start, out_dur, dst, speed=1.0, z0=1.0, z1=1.08, pan=0.0, hdr=None):
    if hdr is None: hdr = is_hdr(src)
    src_dur = out_dur * speed + 0.1
    # zoom factor over output time t (seconds): z(t) = z0 + (z1-z0) * t/out_dur, never below 1
    z = f"max(1,({z0})+(({z1})-({z0}))*t/{out_dur})"
    chain = [
        f"scale=-2:{BASE_H}:flags=bicubic",
        # landscape sources: take a 9:16 window, optionally panned
        f"crop={BASE_W}:{BASE_H}:(iw-{BASE_W})/2*(1+{pan}):0",
        TONEMAP if hdr else "format=yuv420p",
        GRADE,
        f"setpts=(PTS-STARTPTS)/{speed}",
        "fps=30",
        # animated zoom, then a centred crop back to 1080x1920
        f"scale=w='trunc({W}*{z}/2)*2':h='trunc({H}*{z}/2)*2':eval=frame:flags=bicubic",
        f"crop={W}:{H}",
        "setsar=1",
        "setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv",
    ]
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.3f}", "-t", f"{src_dur:.3f}", "-i", src,
           "-an", "-vf", ",".join(chain), "-t", f"{out_dur:.4f}",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-pix_fmt", "yuv420p",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", dst]
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    a = sys.argv[1:]
    cut(a[0], float(a[1]), float(a[2]), a[3], *(float(x) for x in a[4:]))
