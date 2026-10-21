"""Writes the web-sized copies of the story's source scans into img/ (the originals stay in picture_local, which is not committed).

  python scripts/data/web_images.py

Also run scripts/data/unmark_maui.py and scripts/data/petition_count.py, which write the map and petition variants into img/.
Needs Pillow.
"""
import os
from PIL import Image

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
Image.MAX_IMAGE_PIXELS = None
JOBS = [  # source, output, max width, quality
    ('newspaper1.jpg', 'ka-hoku-o-hawaii-1924.jpg', 1500, 78),
    ('sign1.jpg', 'kue-petition-1897-men.jpg', 1100, 80),
]
for src, out, width, q in JOBS:
    im = Image.open(os.path.join(root, 'picture_local', src)).convert('RGB')
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    p = os.path.join(root, 'img', out)
    im.save(p, quality=q, optimize=True, progressive=True)
    print(out, im.size, os.path.getsize(p) // 1024, 'KB')
