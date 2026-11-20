#!/usr/bin/env python3
"""SH27/SH28 v003 — authentic portrait photographs (local compositing, NO AI, 0 credit).
Uses ONLY the archived historical JPG (Nationaal Archief / Anefo 905-8914, CC0 1.0): references/p3/historical_sources/Mohammed_V_1953_Anefo_905-8914_original.jpg
The face is NEVER drawn, generated, reconstructed or retouched: the photograph undergoes geometric transforms only (resize, small rotation, slight perspective).
Paper border, bamboo stick and shadow are drawn around it. v001/v002 and the master are untouched; outputs are never overwritten."""
import sys, hashlib, numpy as np, cv2
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
R = Path(__file__).resolve().parent.parent; HS = R/"references/p3/historical_sources"; POST = R/"references/p3/post"
SRC_JPG = HS/"Mohammed_V_1953_Anefo_905-8914_original.jpg"
assert hashlib.sha256(SRC_JPG.read_bytes()).hexdigest() == "3f2c5ece88094ca64ab94aa9e523060286b9d107b50c1f5777bbb0c221d48d31", "archived photo hash mismatch"
PHOTO = Image.open(SRC_JPG).convert("RGB")                         # 886x1182
def make_card(pw, rot, persp=0.018):
    """printed photo: white paper border around the untouched photograph, resized to pw wide (geometric only)."""
    ph = int(round(pw*PHOTO.height/PHOTO.width)); b = max(8, int(pw*0.055))
    photo = PHOTO.resize((pw, ph), Image.LANCZOS)
    card = Image.new("RGBA", (pw+2*b, ph+2*b+int(b*0.8)), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
    d.rectangle([0, 0, card.width-1, card.height-1], fill=(236, 228, 208, 255))                # warm paper border (not the photo)
    card.paste(photo.convert("RGBA"), (b, b))                                                  # the photograph itself, untouched pixels
    d.rectangle([0, 0, card.width-1, card.height-1], outline=(150, 138, 118, 255), width=1)
    arr = np.asarray(card); h, w = arr.shape[:2]; s = persp*w
    src = np.float32([[0, 0], [w, 0], [w, h], [0, h]]); dst = np.float32([[s, 0], [w-s*0.2, s*0.4], [w, h], [0, h-s*0.3]])   # slight perspective (right side nearer)
    M = cv2.getPerspectiveTransform(src, dst); arr = cv2.warpPerspective(arr, M, (w, h), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_TRANSPARENT)
    return Image.fromarray(arr, "RGBA").rotate(rot, expand=True, resample=Image.BICUBIC)
def place(img, card, cx, bottom_y, hand):
    d = ImageDraw.Draw(img, "RGBA"); x0 = int(cx-card.width/2); y0 = int(bottom_y-card.height)
    # bamboo stick from the card bottom to the raised hand, behind the card
    d.line([(cx, bottom_y-6), hand], fill=(150, 112, 60, 255), width=max(5, card.width//28)); d.line([(cx+2, bottom_y-6), (hand[0]+2, hand[1])], fill=(196, 160, 96, 255), width=max(2, card.width//70))
    sh = Image.new("RGBA", card.size, (0, 0, 0, 0)); sh.paste((40, 30, 20, 95), mask=card.split()[3]); sh = sh.filter(ImageFilter.GaussianBlur(max(3, card.width//40)))
    img.paste(sh, (x0+card.width//30, y0+card.width//26), sh); img.paste(card, (x0, y0), card)
def run(src, dst, items):
    if dst.exists(): sys.exit(f"{dst.name} exists")
    img = Image.open(src).convert("RGB")
    for pw, rot, cx, by, hand in items: place(img, make_card(pw, rot), cx, by, hand)
    img.save(dst); print("ok", dst.name)
if __name__ == "__main__":
    run(POST/"SH27_flags_v002.png", POST/"SH27_flags_portraits_v003.png", [(215, -3, 1050, 872, (1072, 878)), (215, 3, 2610, 742, (2632, 752))])
    run(POST/"SH28_flags_v002.png", POST/"SH28_flags_portraits_v003.png", [(105, 3, 2470, 780, (2470, 792))])
