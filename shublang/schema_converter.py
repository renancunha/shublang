from shublang import evaluate


class SchemaConverter:
    def __init__(self, schema):
        self.schema = schema

    def has_childrens(self, field) -> bool:
        return field["type"] == "object"

    def get_type_converter(self, field_type):
        converters = {
            "string": "str",
            "bool": "bool",
            "float": "float",
            "integer": "int",
        }
        if field_type in converters:
            return converters[field_type]

    def evaluate_field(self, field_name, field, data):
        src = field.get("src")

        # TODO: if src is not present, use the field_name as src
        if not src:
            raise ValueError(
                f"The field {field_name} does not have the source defined."
            )

        field_type = field.get("type")
        if not field_type:
            raise ValueError(f"The field {field_name} does not have the type defined.")

        expression = f'jmespath("{src}")'

        transformations = field.get("transformations")
        if transformations:
            expression += f"|{transformations}"

        type_converter = self.get_type_converter(field_type)
        if type_converter:
            expression += f"|{type_converter}"

        expression += "|first"

        try:
            value = evaluate(expression, [data])
        except TypeError:
            value = None
        except KeyError:
            value = None

        return value

    def _traverse_fields(self, root, data):
        item = {}

        for field_name, field in root["properties"].items():

            if self.has_childrens(field):
                item[field_name] = self._traverse_fields(field, data)
            else:
                item[field_name] = self.evaluate_field(field_name, field, data)

        return item

    def convert(self, data):
        if not isinstance(data, list):
            data = [data]

        result = list(map(lambda x: self._traverse_fields(self.schema, x), data))
        return result
