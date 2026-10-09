"""Mascot poses: white background -> transparent PNG (rembg), optional badge fix.
python3 mascot/cut.py <image> <name> [--badge]   → mascot/png/<name>.png + content/_kit/img/<name>.png
--badge: redraw the badge (diamond + РЕШЕНО) when the generator left it blank."""
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage
from rembg import remove, new_session

def fix_badge(im, dy=0.40, ty=0.66, tw_max=0.84):
    a = np.array(im); ai = a.astype(int)
    y = (ai[..., 0] > 200) & (ai[..., 1] > 170) & (ai[..., 2] < 90) & (ai[..., 3] > 200)
    lab, n = ndimage.label(y); k = np.argmax(ndimage.sum(y, lab, range(1, n + 1))) + 1
    badge = ndimage.binary_fill_holes(lab == k)
    ys, xs = np.where(badge); x0, x1 = xs.min(), xs.max(); w = x1 - x0 + 1
    rows = [r for r in range(ys.min(), ys.max() + 1) if badge[r].sum() > 0.7 * w]; y0, y1 = rows[0], rows[-1]; h = y1 - y0 + 1
    col = tuple(np.median(ai[lab == k][:, :3], axis=0).astype(int)) + (255,)
    S = 4; reg = Image.fromarray(a[y0:y1 + 1, x0:x1 + 1]).resize((w * S, h * S), Image.LANCZOS); d = ImageDraw.Draw(reg)
    m = Image.fromarray((badge[y0:y1 + 1, x0:x1 + 1] * 255).astype('uint8'))
    reg.paste(col, (0, 0), m.resize((w * S, h * S)).filter(ImageFilter.MinFilter(9)))
    cx, cy, r = w * S / 2, h * S * dy, w * S * 0.15
    d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=(13, 15, 19, 255))
    F = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'; fs = int(w * S * 0.19)
    while True:
        font = ImageFont.truetype(F, fs); tw = d.textlength('РЕШЕНО', font=font)
        if tw <= w * S * tw_max: break
        fs -= 1
    d.text((cx - tw / 2, h * S * ty), 'РЕШЕНО', font=font, fill=(13, 15, 19, 255))
    im.paste(reg.resize((w, h), Image.LANCZOS), (x0, y0), m)
    return im

if __name__ == '__main__':
    src, name = sys.argv[1], sys.argv[2]
    o = remove(Image.open(src).convert('RGB'), session=new_session('isnet-general-use'), post_process_mask=True)
    al = np.array(o)[..., 3]; al[al < 12] = 0; o.putalpha(Image.fromarray(al))
    o = o.crop(o.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox())
    if '--badge' in sys.argv: o = fix_badge(o)
    if '--badge-high' in sys.argv: o = fix_badge(o, dy=0.30, ty=0.50, tw_max=0.72)  # lower part hidden by hands
    o.save(f'mascot/png/{name}.png', optimize=True); o.save(f'content/_kit/img/{name}.png'); print(name, o.size)
