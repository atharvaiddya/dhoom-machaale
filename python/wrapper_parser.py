import re


def extract_fields(ocr_results):

    fields = {}

    for item in ocr_results:

        text = item["text"].strip()

        # Net quantity
        if re.search(
            r"\b(net\s*qty|net\s*quantity)\b",
            text,
            re.IGNORECASE
        ):
            fields["net_quantity_label"] = item

        # MRP
        if re.search(
            r"\b(mrp|maximum\s*retail\s*price)\b",
            text,
            re.IGNORECASE
        ):
            fields["mrp_label"] = item

        # Manufacturer
        if re.search(
            r"\b(manufactured\s*by|manufactured\s*&)\b",
            text,
            re.IGNORECASE
        ):
            fields["manufacturer_label"] = item

    return fields