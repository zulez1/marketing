"""Colour cut-outs: same alpha as the B/W ones, original colour with a light grade."""
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

for name in ('speaker1', 'speaker2'):
    im = Image.open(f'src/{name}.jpg').convert('RGB')
    a = Image.open(f'assets/{name}_cutout.png').getchannel('A')
    assert im.size == a.size, (im.size, a.size)
    im = ImageEnhance.Contrast(im).enhance(1.1)
    im = ImageEnhance.Color(im).enhance(1.08).filter(ImageFilter.UnsharpMask(2, 60, 2))
    im.putalpha(a)
    im.save(f'assets/{name}_cutout_color.png')
    print(name, im.size)
