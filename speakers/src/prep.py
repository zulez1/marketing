"""Speaker cut-outs (B/W, alpha), amber cut-paper backing shapes, and B/W event backgrounds."""
import numpy as np, cv2
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from rembg import remove, new_session

AMBER = (240, 185, 11)
sess = new_session('isnet-general-use')

def cutout(src, name):
    im = Image.open(src).convert('RGB')
    rgba = remove(im, session=sess, post_process_mask=True)
    a = np.array(rgba)[:, :, 3].copy()
    # fill small interior holes (e.g. dark patches on clothing the model dropped)
    inv = (a < 128).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(inv, 4)
    H, W = a.shape
    for i in range(1, n):
        x, y, w, h, area = stats[i]
        touches = x == 0 or y == 0 or x + w >= W or y + h >= H
        if not touches and area < 0.02 * H * W: a[lab == i] = 255
    # B/W with punch: luminance, contrast curve, slight sharpen
    g = ImageOps.grayscale(im)
    g = ImageOps.autocontrast(g, cutoff=1)
    g = ImageEnhance.Contrast(g).enhance(1.25).filter(ImageFilter.UnsharpMask(2, 80, 2))
    bw = Image.merge('RGBA', (g, g, g, Image.fromarray(a)))
    bw.save(f'assets/{name}_cutout.png')
    # amber backing: dilate, then simplify to a blocky polygon like hand-cut paper
    m = (a > 128).astype(np.uint8) * 255
    pad = 60
    m = cv2.copyMakeBorder(m, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (61, 61))
    d = cv2.dilate(m, k)
    cnts, _ = cv2.findContours(d, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cnts, key=cv2.contourArea)
    poly = cv2.approxPolyDP(c, 14, True)
    rng = np.random.default_rng(7)
    poly = poly + rng.integers(-6, 7, poly.shape)  # slightly irregular scissor cuts
    shape = np.zeros_like(d); cv2.fillPoly(shape, [poly.astype(np.int32)], 255)
    shape = shape[pad:-pad, pad:-pad]
    # the paper extends below the frame edge where the person is cropped
    h, w = shape.shape
    bottom_rows = np.where(a[-3:].max(0) > 128)[0]
    out = np.zeros((h, w, 4), np.uint8); out[..., :3] = AMBER; out[..., 3] = shape
    Image.fromarray(out).save(f'assets/{name}_paper.png')
    print(name, im.size, 'alpha cover', round((a > 128).mean(), 3))

def background(src, name, crop_h=None):
    im = Image.open(src).convert('RGB')
    w, h = im.size
    # 4:5 crop from the vertical 9:16 frame, slightly above centre
    ch = int(w * 5 / 4); top = int((h - ch) * 0.4)
    im = im.crop((0, top, w, top + ch)).resize((1080, 1350), Image.LANCZOS)
    g = ImageOps.grayscale(im); g = ImageEnhance.Contrast(g).enhance(1.15)
    g = ImageEnhance.Brightness(g).enhance(0.55).filter(ImageFilter.GaussianBlur(1.2))
    g.convert('RGB').save(f'assets/{name}.jpg', quality=90)
    # story version 1080x1920 from the full frame
    s = Image.open(src).convert('RGB').resize((1080, 1920), Image.LANCZOS)
    s = ImageEnhance.Brightness(ImageEnhance.Contrast(ImageOps.grayscale(s)).enhance(1.15)).enhance(0.55).filter(ImageFilter.GaussianBlur(1.2))
    s.convert('RGB').save(f'assets/{name}_story.jpg', quality=90)

if __name__ == '__main__':
  cutout('src/speaker1.jpg', 'speaker1')
  cutout('src/speaker2.jpg', 'speaker2')
  for b in ['IMG_2335', 'IMG_2345', 'IMG_2378', 'IMG_2416']:
      background(f'src/bg_{b}.jpg', f'bg_{b}')
  print('done')
