"""Splits picture_local/Map_of_Maui.jpg into a map without its survey lines and a transparent layer of just the lines.

  python scripts/data/unmark_maui.py

Writes picture_local/Map_of_Maui_clean.jpg (lines painted out) and picture_local/Map_of_Maui_lines.png (the lines alone).
The lines are the map's red, blue and thin yellow/orange boundary strokes; everything else (relief, green and yellow
fills, lettering, paper) is left alone. Needs numpy and opencv-python.
"""
import os
import cv2
import numpy as np

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'picture_local')
src = cv2.imread(os.path.join(root, 'Map_of_Maui.jpg'))
hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
h, s, v = hsv[..., 0].astype(int), hsv[..., 1].astype(int), hsv[..., 2].astype(int)

red = ((h < 9) | (h > 166)) & (s > 80) & (v > 90)
blue = (h > 80) & (h < 135) & (s > 70) & (v > 40)
amber = (h > 10) & (h < 34) & (s > 130) & (v > 150)

def thin(m, k):
    # keep strokes only: drop anything that survives an opening (broad fills)
    m = m.astype(np.uint8)
    wide = cv2.morphologyEx(m, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    return (m > 0) & (wide == 0)

mask = thin(red, 9) | thin(blue, 11) | thin(amber, 11)
mask = cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))

clean = cv2.inpaint(src, mask * 255, 5, cv2.INPAINT_TELEA)
cv2.imwrite(os.path.join(root, 'Map_of_Maui_clean.jpg'), clean, [cv2.IMWRITE_JPEG_QUALITY, 90])

# the lines alone, with the original's colour; alpha follows how far each pixel differs from the clean map
diff = np.abs(src.astype(int) - clean.astype(int)).max(axis=2)
alpha = np.clip(diff * 3, 0, 255).astype(np.uint8) * (mask > 0)
rgba = np.dstack([src * (alpha[..., None] > 0), alpha])
cv2.imwrite(os.path.join(root, 'Map_of_Maui_lines.png'), rgba, [cv2.IMWRITE_PNG_COMPRESSION, 9])
print('masked %.1f%% of pixels' % (100 * (mask > 0).mean()))
