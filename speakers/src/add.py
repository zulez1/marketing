"""New speaker from any photo: fit the person into the 853x1280 card frame, then the usual
B/W cut-out + amber paper (prep.cutout) and a colour cut-out.
python3 src/add.py speaker3 [zoom]   (run from speakers/; photo: src/speaker3.jpg)
zoom > 1 lets the person be wider than the frame (sides cropped) — for tight head-and-shoulders shots.
"""
import sys, numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from rembg import remove
from prep import cutout, sess

W, H = 853, 1280
name = sys.argv[1]; zoom = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
im = Image.open(f'src/{name}.jpg').convert('RGB')
a = np.array(remove(im, session=sess))[:, :, 3]
ys, xs = np.where(a > 128); x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
bw, bh = x1 - x0, y1 - y0
s = min(zoom * W * 0.96 / bw, H * 0.92 / bh)
big = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
arr = np.array(big); cx = (x0 + x1) / 2 * s
# place: person centred horizontally, bottom of the photo on the bottom of the frame if the person touches it
left = round(W / 2 - cx); top = H - arr.shape[0] if y1 >= im.height - 3 else round(H - 20 - y1 * s)
pad = [(max(0, top), max(0, H - top - arr.shape[0])), (max(0, left), max(0, W - left - arr.shape[1])), (0, 0)]
arr = np.pad(arr, pad, mode='edge')
oy, ox = max(0, -top), max(0, -left)
Image.fromarray(arr[oy:oy + H, ox:ox + W]).save(f'src/{name}_fit.jpg', quality=95)
cutout(f'src/{name}_fit.jpg', name)
# colour version, same mask
c = Image.open(f'src/{name}_fit.jpg').convert('RGB')
c = ImageEnhance.Color(ImageEnhance.Contrast(c).enhance(1.1)).enhance(1.08).filter(ImageFilter.UnsharpMask(2, 60, 2))
c.putalpha(Image.open(f'assets/{name}_cutout.png').getchannel('A'))
c.save(f'assets/{name}_cutout_color.png'); print(name, 'ok')
