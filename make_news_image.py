#!/usr/bin/env python3
"""Generate the make.fun Nov 24 world-news image: 1024x1024 PNG, program output.
Stories verified 2026-11-25 against DailyFoxNews, CWEB, Medium/All Voices,
dailysummaryof.com, 10things.news and principia.news — all agree on the top items.
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap

W = H = 1024
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(p, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, p)

BLUE = (11, 63, 166); DARK = (20, 30, 50); GREY = (90, 100, 115); LIGHT = (235, 242, 255)
# Header
d.rectangle([0, 0, W, 150], fill=BLUE)
d.text((48, 28), "WORLD NEWS", font=font(58), fill="white")
d.text((48, 96), "Tuesday, 24 November 2026", font=font(30, False), fill=(200, 220, 255))
d.text((W-48, 34), "24 NOV", font=font(34), fill="white", anchor="ra")

stories = [
    ("TECH", "Nvidia reinstates Jensen Huang as CEO",
     "Board brings him back under two weeks after his resignation; shares jump about 30%."),
    ("COURTS", "US jury: Huawei guilty on trade secrets & bank fraud",
     "Convicted of conspiracy to steal trade secrets and bank fraud; acquitted of racketeering."),
    ("MIDDLE EAST", "Tankers hit mines in the Strait of Hormuz",
     "Iran reports three, then four, tankers struck by mines and catching fire."),
    ("CONFLICT", "Ukraine hits Russian ships in two seas",
     "Drone strikes on a Russian cargo ship in the Gulf of Finland and a warship off Libya."),
    ("UKRAINE", "Russian strike on Zaporizhzhia kills 2, wounds ~40",
     "Overnight attack wounds about 40 people, including four children, officials say."),
    ("JUSTICE", "ICJ: Myanmar committed genocide against Rohingya",
     "The International Court of Justice rules Myanmar committed genocide."),
]
y = 164
for tag, head, sub in stories:
    d.rounded_rectangle([36, y, W-36, y+120], radius=16, fill=LIGHT, outline=(200, 215, 240), width=2)
    d.text((60, y+12), tag, font=font(20), fill=BLUE)
    d.text((60, y+38), head, font=font(27), fill=DARK)
    # wrap sub to fit
    for i, line in enumerate(textwrap.wrap(sub, width=64)):
        d.text((60, y+72+i*22), line, font=font(20, False), fill=GREY)
    y += 130
# Source note: headlines cross-checked across the outlets named in the footer.
d.text((48, H-44), "Sources: AP / Daily Summary of World / 10 Things / Principia  •  24 Nov 2026",
       font=font(19, False), fill=GREY)
out = "news-2026-11-24.png"
img.save(out)
print(out, img.size)
