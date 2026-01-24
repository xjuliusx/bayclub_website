from PIL import Image
import os

# Source image paths (from project images/ folder)
src_images = [
    os.path.join('images', 'Gym 1.jpeg'),
    os.path.join('images', 'indoor Basketball.jpeg'),
    os.path.join('images', 'gym 2.jpeg'),
]

out_path = os.path.join('images', 'combined_gym.jpg')

# target size per panel (you can adjust these values)
panel_w = 700
panel_h = 420

# helper: open image, center-crop to target aspect ratio, then resize
def fit_image(path, size):
    target_w, target_h = size
    im = Image.open(path).convert('RGB')
    iw, ih = im.size
    target_ratio = target_w / target_h
    current_ratio = iw / ih
    if current_ratio > target_ratio:
        # crop left/right
        new_w = int(ih * target_ratio)
        left = (iw - new_w) // 2
        im = im.crop((left, 0, left + new_w, ih))
    else:
        # crop top/bottom
        new_h = int(iw / target_ratio)
        top = (ih - new_h) // 2
        im = im.crop((0, top, iw, top + new_h))
    im = im.resize((target_w, target_h), Image.LANCZOS)
    return im

# create final canvas
final_w = panel_w * len(src_images)
final_h = panel_h
canvas = Image.new('RGB', (final_w, final_h), (255,255,255))

x = 0
for path in src_images:
    if not os.path.exists(path):
        raise SystemExit(f"Source image not found: {path}")
    fitted = fit_image(path, (panel_w, panel_h))
    canvas.paste(fitted, (x, 0))
    x += panel_w

canvas.save(out_path, quality=90)
print('Wrote', out_path)
