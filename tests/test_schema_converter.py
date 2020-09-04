import json
from shublang import SchemaConverter


def test_convert_walmart_to_melvin():

    # file containing the custom schema
    with open("./tests/resources/walmart_to_melvin_schema.json", "r") as f:
        schema = json.loads(f.read())

    # product data in the unified-schema format
    with open("./tests/resources/base_walmart_data.json", "r") as f:
        base_data = json.loads(f.read())

    # product data in the custom schema format
    with open("./tests/resources/melvin_walmart_data.json", "r") as f:
        expected_data = json.loads(f.read())

    converter = SchemaConverter(schema)
    assert converter.convert(base_data) == expected_data


def test_convert_amazon_to_books():

    # file containing the custom schema
    with open("./tests/resources/amazon_to_books.json", "r") as f:
        schema = json.loads(f.read())

    with open("./tests/resources/base_amazon_data.json", "r") as f:
        base_data = json.loads(f.read())

    with open("./tests/resources/books_amazon_data.json", "r") as f:
        expected_data = json.loads(f.read())

    converter = SchemaConverter(schema)
    assert converter.convert(base_data) == expected_data
