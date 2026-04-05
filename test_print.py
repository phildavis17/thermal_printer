import os
from pathlib import Path
from PIL import Image

from src.characters import SepChar

PRINTER_IP = "192.168.1.87"  # Replace with your printer's IP address
PRINTER_PORT = 9100            # Replace with your printer's port if different
LOCAL_CAPABILITIES_FILE = Path(__file__).parent / "capabilities.json"
PRINTER_PIXEL_WIDTH = 576


DASH = 0x2D

os.environ["ESCPOS_CAPABILITIES_FILE"] = str(LOCAL_CAPABILITIES_FILE)
from escpos.printer import Network


def _scale_image_to_width(img: Image.Image, target_width_pixels: int) -> Image.Image:
    scale_factor = target_width_pixels / img.width
    target_height_pixels = int(img.height * scale_factor)
    return img.resize((target_width_pixels, target_height_pixels), Image.Resampling.LANCZOS)


def get_image(image_path: Path) -> Image.Image:
    img = Image.open(image_path)
    return _scale_image_to_width(img, PRINTER_PIXEL_WIDTH)





def main():
    p = Network(PRINTER_IP, PRINTER_PORT, profile="RP850P")
    p.hw("INIT")
    # p.charcode("CP437")
    # p.text("\xB0")
    # p.set(align="left")
    # p.textln("This is a test")
    # p.set(align="right")
    # p.textln("This is a test")
    # p.set(align="center")
    # p.textln("This is a test")
    # for r in "234567890ABCDEF":
    #     for c in "012234567890ABCDEF":
    # for r in "23":
    #     for c in "01":
    #         code = f"\\x{r}{c}"
    #         p.text(f"{r} {c} -> ")
    #         p.text("\xB0")
    #         p.ln()
    p.textln(SepChar.BLOCK_0.value * 48)
    p.ln()
    p.textln(SepChar.BLOCK_1.value * 48)
    p.ln()
    p.textln(SepChar.BLOCK_2.value * 48)
    p.ln()
    p.textln(SepChar.BLOCK_3.value * 48)
    p.ln()
    p.textln(SepChar.LINE.value * 48)
    p.ln()
    p.textln(SepChar.DOUBLE_LINE.value * 48)
    p.ln()
    p.textln(SepChar.BLOCK_UPPER.value * 48)
    p.ln()
    p.textln(SepChar.BLOCK_LOWER.value * 48)
    p.ln()
    # p.textln(SepChar.BLOCK_UPPER * 48)
    # p.textln("_"*48)
    # p.textln("="*48)
    # p.set(font=0)
    # p.textln("This is a test")
    # p.set(font=1)
    # p.textln("This is a test")
    # p.set(font=2, custom_size=True, width=4, height=4)
    # p.textln("[] This is a test")
    # pic = get_image(Path(__file__).parent / "mcld_drawing.jpeg")
    # pic = get_image(Path(__file__).parent / "mcld.jpg")
    # p.image(pic, impl="bitImageColumn", center=True)
    p.ln(2)
    p.cut()


if __name__ == "__main__":
    main()
