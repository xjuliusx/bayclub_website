from PIL import Image
import os

# Source image paths (from project images/ folder)
src_images = [
    os.path.join('images', 'Club 1.jpeg'),
    os.path.join('images', 'Gym 1.jpeg'),
    os.path.join('images', 'indoor Basketball.jpeg'),
]

out_path = os.path.join('images', 'combined_vertical.jpg')

# target size per panel
panel_w = 1200
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

# create final canvas (stack vertically)
final_w = panel_w
final_h = panel_h * len(src_images)
canvas = Image.new('RGB', (final_w, final_h), (255,255,255))

y = 0
for path in src_images:
    if not os.path.exists(path):
        raise SystemExit(f"Source image not found: {path}")
    fitted = fit_image(path, (panel_w, panel_h))
    canvas.paste(fitted, (0, y))
    y += panel_h

canvas.save(out_path, quality=90)
print('Wrote', out_path)
