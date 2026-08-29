from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False
)

image_path = "test.jpg"

results = ocr.predict(image_path)

for result in results:
    result.print()