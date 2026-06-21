#!/usr/bin/env python3
"""Facebook хуудасны cover болон профайл зураг үүсгэгч.
Нил ягаан дэвсгэр + зурсан лотос + 'Өөрийгөө хайрлахуй' уран бичмэл."""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

TEXT = "Өөрийгөө хайрлахуй"
SCRIPT_FONT = ".fonts/Pacifico.ttf"


def vgradient(w, h, top, bottom):
    """Босоо градиент."""
    base = Image.new("RGB", (w, h))
    px = base.load()
    for y in range(h):
        t = y / max(1, h - 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        for x in range(w):
            px[x, y] = (r, g, b)
    return base


def radial_glow(w, h, cx, cy, radius, color, max_alpha):
    """Зөөлөн алтан туяа."""
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    steps = 60
    for i in range(steps, 0, -1):
        r = radius * i / steps
        a = int(max_alpha * (1 - i / steps))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (a,))
    return layer.filter(ImageFilter.GaussianBlur(8))


def petal(width, height, fill, outline):
    """Үзүүртэй навч хэлбэрийн дэлбээ (доод төв = суурь)."""
    pad = 6
    tile = Image.new("RGBA", (width + pad * 2, height + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    cx = width / 2 + pad
    pts = []
    N = 40
    for i in range(N + 1):
        t = i / N
        x = cx + math.sin(t * math.pi) * (width / 2)
        y = pad + t * height
        pts.append((x, y))
    for i in range(N, -1, -1):
        t = i / N
        x = cx - math.sin(t * math.pi) * (width / 2)
        y = pad + t * height
        pts.append((x, y))
    d.polygon(pts, fill=fill, outline=outline)
    return tile


def draw_lotus(canvas, cx, cy, scale=1.0, alpha=235):
    """Лотос цэцэг зурах. cy = цэцгийн суурь."""
    w, h = canvas.size
    fill = (255, 255, 255, alpha)
    edge = (245, 222, 160, min(255, alpha))
    front_fill = (255, 250, 240, alpha)

    rows = [
        # (дэлбээний өргөн, өндөр, өнцгүүд, fill)
        (int(70 * scale), int(210 * scale), [-78, -52, -26, 0, 26, 52, 78], fill),
        (int(64 * scale), int(165 * scale), [-40, -20, 0, 20, 40], front_fill),
    ]
    for pw, ph, angles, fcol in rows:
        for a in angles:
            layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            p = petal(pw, ph, fcol, edge)
            # дэлбээний суурь (доод төв) -> лотосын төвд
            bx = cx - p.size[0] // 2
            by = cy - p.size[1] + 6
            layer.alpha_composite(p, (int(bx), int(by)))
            layer = layer.rotate(a, center=(cx, cy), resample=Image.BICUBIC)
            canvas.alpha_composite(layer)
    # төв
    d = ImageDraw.Draw(canvas)
    r = int(22 * scale)
    d.ellipse([cx - r, cy - r * 2, cx + r, cy], fill=(245, 205, 120, alpha))


def fit_font(text, path, target_w, start=200):
    size = start
    while size > 10:
        f = ImageFont.truetype(path, size)
        bbox = f.getbbox(text)
        if bbox[2] - bbox[0] <= target_w:
            return f
        size -= 4
    return ImageFont.truetype(path, 12)


def draw_text_center(canvas, text, font, cx, cy, fill, shadow=True):
    d = ImageDraw.Draw(canvas)
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = cx - tw / 2 - bbox[0]
    y = cy - th / 2 - bbox[1]
    if shadow:
        d.text((x + 3, y + 3), text, font=font, fill=(60, 30, 90, 130))
    d.text((x, y), text, font=font, fill=fill)


# ---------- COVER (1640 x 624) ----------
def make_cover():
    w, h = 1640, 624
    img = vgradient(w, h, (88, 44, 160), (44, 20, 92)).convert("RGBA")
    img.alpha_composite(radial_glow(w, h, w // 2, int(h * 0.42), 360, (255, 220, 150), 90))
    draw_lotus(img, w // 2, int(h * 0.50), scale=0.95, alpha=210)
    font = fit_font(TEXT, SCRIPT_FONT, int(w * 0.7), start=150)
    draw_text_center(img, TEXT, font, w // 2, int(h * 0.78), (255, 248, 235, 255))
    img.convert("RGB").save("content/fb-cover.jpg", quality=92)
    print("cover saved")


# ---------- PROFILE (1080 x 1080) ----------
def make_profile():
    w, h = 1080, 1080
    img = vgradient(w, h, (108, 58, 180), (54, 26, 110)).convert("RGBA")
    img.alpha_composite(radial_glow(w, h, w // 2, int(h * 0.40), 420, (255, 220, 150), 100))
    draw_lotus(img, w // 2, int(h * 0.46), scale=1.25, alpha=230)
    font = fit_font(TEXT, SCRIPT_FONT, int(w * 0.82), start=180)
    draw_text_center(img, TEXT, font, w // 2, int(h * 0.80), (255, 248, 235, 255))
    img.convert("RGB").save("content/fb-profile.jpg", quality=92)
    print("profile saved")


if __name__ == "__main__":
    make_cover()
    make_profile()
