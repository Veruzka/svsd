"""Builds img/kue-petition-1897-women-44.jpg from picture_local/sign3.jpg (and img/kue-petition-1897-women.jpg, the original, web-sized): the same page with the clerk's total, 43, rewritten as 44.

  python scripts/data/petition_count.py

The two handwritten 43s (a small one in the number column, a large one under the last name) are painted out, then the
clerk's own 4 is copied into the place of each 3, so the new total is in the same hand. The story fades this image in over
the original when a visitor signs. Needs numpy and opencv-python. Positions were measured on this scan (1527 x 2500).
"""
import os
import cv2
import numpy as np

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
im = cv2.imread(os.path.join(root, 'picture_local', 'sign3.jpg'))

# for each total: the box around its 3 (painted out), the box around its 4, and where a copy of the 4 goes
JOBS = [
    dict(three=(790, 2070, 836, 2160), four=(750, 2074, 794, 2162), dx=42, dy=-4),
    dict(three=(1098, 2202, 1190, 2305), four=(928, 2214, 1066, 2372), dx=165, dy=-10),
]

def ink(region):
    # the clerk's pencil is dark grey in every channel; the red column rules and paper are not
    return (region.max(axis=2) < 190).astype(np.uint8)

mask = np.zeros(im.shape[:2], np.uint8)
for j in JOBS:
    x0, y0, x1, y1 = j['three']
    mask[y0:y1, x0:x1] = ink(im[y0:y1, x0:x1])
clean = cv2.inpaint(im, cv2.dilate(mask, np.ones((5, 5), np.uint8)) * 255, 3, cv2.INPAINT_TELEA)

out = clean.copy()
for j in JOBS:
    x0, y0, x1, y1 = j['four']
    glyph = im[y0:y1, x0:x1]
    m = cv2.dilate(ink(glyph), np.ones((3, 3), np.uint8)).astype(bool)
    ty, tx = y0 + j['dy'], x0 + j['dx']
    region = out[ty:ty + (y1 - y0), tx:tx + (x1 - x0)]
    region[m] = np.minimum(region[m], glyph[m])

q = [cv2.IMWRITE_JPEG_QUALITY, 80]
cv2.imwrite(os.path.join(root, 'img', 'kue-petition-1897-women-44.jpg'), out, q)
cv2.imwrite(os.path.join(root, 'img', 'kue-petition-1897-women.jpg'), im, q)
print('ok')
