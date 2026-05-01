from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "images" / "events" / "annual_meeting_flyer.png"
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 800, 600
BACKGROUND = (247, 248, 251)
HEADER_COLOR = (14, 74, 135)
ACCENT_COLOR = (224, 71, 52)
CARD_BG = (255, 255, 255)
TEXT_COLOR = (32, 33, 36)

FONT_PATHS = [
    "/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/SFNSDisplay.ttf",
]

def load_font(size):
    for path in FONT_PATHS:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()

TITLE_FONT = load_font(60)
HEADING_FONT = load_font(40)
BODY_FONT = load_font(30)

img = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
draw = ImageDraw.Draw(img)

# Header bar
bar_height = 200
draw.rectangle([(0, 0), (WIDTH, bar_height)], fill=HEADER_COLOR)
draw.text((20, 40), "Bay Club Annual Meeting", font=TITLE_FONT, fill="white")

# Card
card_top = 250
card_margin = 50
card_right = WIDTH - card_margin
card_left = card_margin
card_height = 300
draw.rounded_rectangle([(card_left, card_top), (card_right, card_top + card_height)], radius=20, fill=CARD_BG)

# Text
body_text = "Join us in person or online — your ballot matters."
current_y = card_top + 40
text_box_width = card_right - card_left - 60
lines = []
for word in body_text.split():
    test_line = word if not lines else lines[-1] + " " + word
    bbox = draw.textbbox((0, 0), test_line, font=HEADING_FONT)
    line_width = bbox[2] - bbox[0]
    if not lines or line_width > text_box_width:
        lines.append(word)
    else:
        lines[-1] = test_line
for line in lines:
    draw.text((card_left + 30, current_y), line, font=HEADING_FONT, fill=TEXT_COLOR)
    current_y += 55

# Save PNG
img.save(OUTPUT_PATH)
print(f"Created thumbnail PNG at: {OUTPUT_PATH}")