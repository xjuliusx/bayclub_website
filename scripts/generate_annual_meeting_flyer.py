from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "events" / "annual_meeting_flyer.pdf"
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 2550, 3300
BACKGROUND = (247, 248, 251)
HEADER_COLOR = (14, 74, 135)
ACCENT_COLOR = (224, 71, 52)
CARD_BG = (255, 255, 255)
TEXT_COLOR = (32, 33, 36)
SUBTEXT_COLOR = (84, 97, 112)

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

TITLE_FONT = load_font(110)
HEADING_FONT = load_font(70)
BODY_FONT = load_font(50)
BUTTON_FONT = load_font(60)
SMALL_FONT = load_font(40)

img = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
draw = ImageDraw.Draw(img)

# Header bar
bar_height = 520
draw.rectangle([(0, 0), (WIDTH, bar_height)], fill=HEADER_COLOR)
draw.text((120, 80), "Bay Club Annual Meeting Reminder", font=TITLE_FONT, fill="white")

# Accent circle image
circle_center = (WIDTH - 440, 280)
circle_radius = 200
draw.ellipse([
    (circle_center[0] - circle_radius, circle_center[1] - circle_radius),
    (circle_center[0] + circle_radius, circle_center[1] + circle_radius)
], fill=(255, 255, 255, 255), outline=(255, 255, 255), width=0)

draw.ellipse([
    (circle_center[0] - 150, circle_center[1] - 150),
    (circle_center[0] + 150, circle_center[1] + 150)
], fill=(224, 71, 52))

# Simple calendar icon
calendar_x, calendar_y = circle_center[0] - 70, circle_center[1] - 90
calendar_w, calendar_h = 140, 140
draw.rectangle([(calendar_x, calendar_y), (calendar_x + calendar_w, calendar_y + calendar_h)], fill="white")
draw.rectangle([(calendar_x, calendar_y), (calendar_x + calendar_w, calendar_y + 40)], fill=(14, 74, 135))
draw.line([(calendar_x + 10, calendar_y + 60), (calendar_x + 10, calendar_y + calendar_h - 10)], fill=(224, 71, 52), width=12)
draw.line([(calendar_x + 70, calendar_y + 60), (calendar_x + 70, calendar_y + calendar_h - 10)], fill=(224, 71, 52), width=12)

draw.rectangle([(calendar_x + 20, calendar_y + 80), (calendar_x + 40, calendar_y + 100)], fill=(14, 74, 135))
draw.rectangle([(calendar_x + 80, calendar_y + 80), (calendar_x + 100, calendar_y + 100)], fill=(14, 74, 135))

# Card for details
card_top = 600
card_margin = 140
card_right = WIDTH - card_margin
card_left = card_margin
card_height = 1890
draw.rounded_rectangle([(card_left, card_top), (card_right, card_top + card_height)], radius=40, fill=CARD_BG)

# Section header
section_x = card_left + 100
current_y = card_top + 100
draw.text((section_x, current_y), "Annual Meeting Details", font=HEADING_FONT, fill=TEXT_COLOR)
current_y += 120

# Body text
body_lines = [
    "Dear Owners,",
    "",
    "Please be reminded that the Bay Club's Annual Meeting will be held on",
    "May 5th, 2026 at 8:00 PM in the Community Room and via Zoom.",
    "",
    "If you do not intend to vote for any specific candidate, please submit a signed ballot.",
    "Ballots may be submitted online or dropped into the ballot boxes",
    "located in each Bay Club lobby.",
    "",
    "Each ballot submitted by a Unit Owner helps toward reaching quorum for",
    "the Annual Meeting."
]
for line in body_lines:
    draw.text((section_x, current_y), line, font=BODY_FONT, fill=TEXT_COLOR)
    current_y += 80

# Visual accent row
box_x = section_x
box_y = current_y + 60
box_w = WIDTH - card_margin - section_x
box_h = 360
draw.rounded_rectangle([(box_x, box_y), (box_x + box_w, box_y + box_h)], radius=30, fill=(236, 244, 255))

accent_text = "Join us in person or online — your ballot matters."
draw.text((box_x + 40, box_y + 40), accent_text, font=HEADING_FONT, fill=HEADER_COLOR)

# Ballot icon inside accent box
icon_center = (box_x + box_w - 220, box_y + box_h // 2)
icon_w = 200
icon_h = 180
draw.rectangle([(icon_center[0] - icon_w // 2, icon_center[1] - icon_h // 2), (icon_center[0] + icon_w // 2, icon_center[1] + icon_h // 2)], fill="white", outline=HEADER_COLOR, width=10)
draw.line([(icon_center[0] - 70, icon_center[1] - 20), (icon_center[0] + 70, icon_center[1] - 20)], fill=HEADER_COLOR, width=12)
draw.rectangle([(icon_center[0] - 80, icon_center[1] + 30), (icon_center[0] + 80, icon_center[1] + 70)], fill=(224, 71, 52))
draw.polygon([(icon_center[0] - 25, icon_center[1] + 15), (icon_center[0], icon_center[1] - 15), (icon_center[0] + 40, icon_center[1] + 20), (icon_center[0] + 10, icon_center[1] + 55), (icon_center[0] - 25, icon_center[1] + 25)], fill="white")

# Footer text
footer_y = card_top + card_height - 180
draw.text((section_x, footer_y), "Thank you for helping keep our community engaged and informed.", font=SMALL_FONT, fill=SUBTEXT_COLOR)

# Save PDF
img.save(OUTPUT_PATH, "PDF", resolution=300)
print(f"Created flyer PDF at: {OUTPUT_PATH}")
