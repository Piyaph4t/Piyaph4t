from PIL import Image, ImageDraw, ImageFont
import os

WIDTH, HEIGHT = 480, 320
BG = (13, 17, 23)
GREEN = (0, 255, 128)
CYAN = (0, 200, 255)
GRAY = (140, 148, 160)
WHITE = (230, 237, 243)
YELLOW = (255, 215, 0)

FONT_SIZE = 14
LINE_H = 20
PAD = 14

try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", FONT_SIZE)
    font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", FONT_SIZE)
except Exception:
    font = ImageFont.load_default()
    font_bold = font

SCRIPT = [
    (GREEN,  "fiw@arch:~$ "),
    (WHITE,  "gcc -O2 -o kernel kernel.c && echo done"),
    (GRAY,   ""),
    (CYAN,   "[✓] Compiled kernel.c  →  ./kernel"),
    (GRAY,   ""),
    (GREEN,  "fiw@arch:~$ "),
    (WHITE,  "./kernel"),
    (GRAY,   ""),
    (YELLOW, "  Performance matters."),
    (YELLOW, "  Curiosity beats memorization."),
    (YELLOW, "  Learn fundamentals first."),
    (YELLOW, "  Engineering = trade-offs."),
    (GRAY,   ""),
    (GREEN,  "fiw@arch:~$ "),
    (WHITE,  "uname -r"),
    (GRAY,   ""),
    (WHITE,  "6.17.0-22-generic"),
    (GRAY,   ""),
    (GREEN,  "fiw@arch:~$ "),
    (WHITE,  "echo 'Still learning. Still building.'"),
    (GRAY,   ""),
    (WHITE,  "Still learning. Still building."),
    (GRAY,   ""),
    (GREEN,  "fiw@arch:~$ _"),
]

VISIBLE_LINES = (HEIGHT - 2 * PAD) // LINE_H


def draw_frame(lines_so_far):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(img)
    visible = lines_so_far[-VISIBLE_LINES:]
    for i, (color, text) in enumerate(visible):
        y = PAD + i * LINE_H
        d.text((PAD, y), text, font=font, fill=color)
    return img


frames = []
durations = []

accumulated = []

for idx, (color, text) in enumerate(SCRIPT):
    if text == "":
        accumulated.append((color, text))
        frames.append(draw_frame(accumulated))
        durations.append(60)
        continue

    is_prompt_prefix = color == GREEN and text.endswith("$ ") or text.endswith("$ _")

    if is_prompt_prefix:
        accumulated.append((color, text))
        frames.append(draw_frame(accumulated))
        durations.append(120)
        continue

    for ch_count in range(1, len(text) + 1):
        accumulated_with_partial = accumulated + [(color, text[:ch_count])]
        frames.append(draw_frame(accumulated_with_partial))
        durations.append(40)

    accumulated.append((color, text))
    frames.append(draw_frame(accumulated))
    durations.append(200)

for _ in range(8):
    frames.append(draw_frame(accumulated))
    durations.append(120)

out = os.path.join(os.path.dirname(__file__), "terminal.gif")
frames[0].save(
    out,
    save_all=True,
    append_images=frames[1:],
    loop=0,
    duration=durations,
    optimize=False,
)
print(f"Saved {len(frames)} frames → {out}")
