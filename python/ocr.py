import json
import sys

from paddleocr import PaddleOCR

ocr = PaddleOCR(
    enable_mkldnn=False,
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False
)


def extract_text(image_path):
    results = ocr.predict(image_path)

    output = []

    for result in results:
        data = result.json

        if isinstance(data, str):
            data = json.loads(data)

        data = data["res"]

        for text, score, box in zip(
            data["rec_texts"],
            data["rec_scores"],
            data["rec_boxes"]
        ):
            output.append({
                "text": text,
                "score": float(score),
                "box": box
            })

    return output


if __name__ == "__main__":
    image_path = sys.argv[1]

    result = extract_text(image_path)

    print(json.dumps(result, ensure_ascii=False))