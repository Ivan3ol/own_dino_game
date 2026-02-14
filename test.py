from pathlib import Path
from PIL import Image

IN_DIR = Path("input_png")
OUT_DIR = Path("output_16")
OUT_DIR.mkdir(parents=True, exist_ok=True)

TARGET = (16, 16)

def crop_alpha(img: Image.Image) -> Image.Image:
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    bbox = img.split()[-1].getbbox()
    return img if bbox is None else img.crop(bbox)

def pad_to(img: Image.Image, size=(16,16)) -> Image.Image:
    canvas = Image.new("RGBA", size, (0,0,0,0))
    x = (size[0] - img.size[0]) // 2
    y = (size[1] - img.size[1]) // 2
    canvas.paste(img, (x, y), img)
    return canvas

for p in IN_DIR.glob("*.png"):
    img = Image.open(p)
    tight = crop_alpha(img)

    # Optional: if tight is bigger than 16x16, shrink to fit
    if tight.size[0] > 16 or tight.size[1] > 16:
        tight.thumbnail(TARGET, Image.Resampling.LANCZOS)

    out = pad_to(tight, TARGET)
    out.save(OUT_DIR / p.name)
    print(p.name, "->", out.size)