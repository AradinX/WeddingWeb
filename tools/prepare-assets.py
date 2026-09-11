"""Wycina biale tlo z grafik w Inspiracje/ i zapisuje gotowe PNG do assets/.

Uruchom po podmianie ktoregokolwiek pliku zrodlowego:  python tools/prepare-assets.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

SRC = Path(__file__).resolve().parent.parent / "Inspiracje"
OUT = Path(__file__).resolve().parent.parent / "assets"

MAGENTA = (255, 0, 255)


def cut_white(im, thresh=60):
    """Zdejmuje tlo wypelnieniem od krawedzi - biel WEWNATRZ motywu (biale kwiaty) zostaje."""
    rgb = im.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    seeds = [(x, y) for x in (0, w // 2, w - 1) for y in (0, h // 2, h - 1)]
    seeds += [(x, 0) for x in range(0, w, 8)] + [(x, h - 1) for x in range(0, w, 8)]
    seeds += [(0, y) for y in range(0, h, 8)] + [(w - 1, y) for y in range(0, h, 8)]
    for s in seeds:
        if min(px[s]) > 235 and px[s] != MAGENTA:
            ImageDraw.floodfill(rgb, s, MAGENTA, thresh=thresh)

    bg = np.all(np.array(rgb) == MAGENTA, axis=2)
    alpha = Image.fromarray(np.where(bg, 0, 255).astype(np.uint8))
    # zmiekczenie + lekkie cofniecie krawedzi, zeby nie zostala biala obwodka
    alpha = alpha.filter(ImageFilter.GaussianBlur(1.1))
    a = np.array(alpha).astype(np.int16)
    a = np.clip((a - 120) * (255 / 110), 0, 255).astype(np.uint8)

    out = im.convert("RGBA")
    out.putalpha(Image.fromarray(a))
    return out.crop(out.getchannel("A").getbbox())


JOBS = {
    "koperta_zamknięta.png": "envelope-closed.png",
    "Front-koperta.png": "envelope-front.png",
    "pieczęć.png": "seal.png",
    "Kwiaty.png": "flowers.png",
}

OUT.mkdir(exist_ok=True)
for src, dst in JOBS.items():
    img = cut_white(Image.open(SRC / src))
    img.save(OUT / dst, optimize=True)
    print(f"{dst:24} {img.size}")

# karta to pelny prostokat - nic nie wycinamy
card = Image.open(SRC / "Karta weselna.png").convert("RGB")
card.save(OUT / "card.png", optimize=True)
print(f"{'card.png':24} {card.size}")
