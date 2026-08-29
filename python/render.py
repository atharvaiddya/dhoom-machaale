from PIL import Image, ImageDraw, ImageFont
from ocr import extract_text
import sys


def render_clean_document(image_path, output_path):
    results = extract_text(image_path)

    original = Image.open(image_path)
    width, height = original.size


    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)

    font = ImageFont.load_default(size=24)

    
    for item in results:
        text = item["text"]
        box = item["box"]

        x1, y1, x2, y2 = box

        draw.text(
            (x1, y1),
            text,
            fill="black",
            font=font
        )

    canvas.save(output_path)

    print(f"\nClean document created:")
    print(output_path)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage:")
        print("python render.py <image>")
        sys.exit(1)

    image_path = sys.argv[1]

    render_clean_document(
        image_path,
        "clean_output.png"
    )