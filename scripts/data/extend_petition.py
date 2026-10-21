"""Adds two blank ruled rows to the bottom of picture_local/sign2.jpg, so there is room for a new signature after the last name.

  python scripts/data/extend_petition.py

Writes picture_local/sign2_ext.jpg. The new rows are built from the page itself: every ruled row of the table is
resampled to one height and a high percentile taken, which erases the handwriting and keeps the paper, the rules and the red
column lines. Needs numpy and opencv-python. Line positions below were measured on this scan (1506 x 2500).
"""
import os
import cv2
import numpy as np

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'picture_local')
im = cv2.imread(os.path.join(root, 'sign2.jpg'))
H, W = im.shape[:2]

# ruled lines under each row (header line first); the ones missing from the detection are interpolated
LINES = [778, 839, 906, 976, 1039, 1110, 1178, 1246, 1314, 1382, 1447, 1520, 1590, 1657, 1727, 1793, 1862, 1930, 2000, 2074, 2141, 2213, 2278, 2350, 2413, 2482]
PITCH = 68
NEW_ROWS = 2

strips = []
for a, b in zip(LINES[2:-1], LINES[3:]):  # rows 3..25: leave out the header and the first two rows
    strip = im[a + 3:b + 3]
    strips.append(cv2.resize(strip, (W, PITCH), interpolation=cv2.INTER_AREA))
stack = np.stack(strips).astype(np.float32)
# a high percentile instead of the median, so no ghost of the handwriting is left; then match the tone of the paper above
template = np.percentile(stack, 78, axis=0)
ref = np.median(stack, axis=(0, 1, 2))
template = np.clip(template - (np.median(template, axis=(0, 1)) - ref), 0, 255).astype(np.uint8)

cut = LINES[-1] + 3
out = np.vstack([im[:cut]] + [template] * NEW_ROWS + [im[cut:]])
cv2.imwrite(os.path.join(root, 'sign2_ext.jpg'), out, [cv2.IMWRITE_JPEG_QUALITY, 90])

h = out.shape[0]
print('size', out.shape[1], h)
print('row 51: y %.4f-%.4f of height, number col x 742-830, name col x 830-1422 of 1506' % (cut / h, (cut + PITCH) / h))
