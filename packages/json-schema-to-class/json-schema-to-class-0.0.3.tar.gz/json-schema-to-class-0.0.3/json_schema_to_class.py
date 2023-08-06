import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def spaces(level: int):
    return '    ' * level


def indent_line(line: str, level: int):
    return spaces(level=level) + line if line else ''


def indent_class(code: str, level: int):
    return '\n'.join(indent_line(line, level) for line in code.splitlines())


class Item:
    def __init__(self, name: str):
        self.name = name

    def to_json(self):
        pairs = []
        for key in dir(self):
            if not key.startswith('_'):
                value = getattr(self, key)
                if not callable(value):
                    pairs.append((key, value))
        return dict(pairs)

    def class_name(self):
        return self.name.title().replace('_', '')

    def type_name(self):
        return self.class_name()

    def to_init_code(self) -> str:
        raise NotImplementedError  # pragma: no cover

    def to_class_code(self, level: int = 0) -> str:
        raise NotImplementedError  # pragma: no cover


class Basic(Item):
    TYPE_MAP = {
        'integer': int,
        'number': float,
        'string': str,
        'array': list,
        'boolean': bool
    }

    def __init__(self, name: str, type: str, default: Any = None):
        super().__init__(name=name)
        self.type = type
        self.default = default

    def type_name(self):
        return Basic.TYPE_MAP[self.type].__name__

    def to_init_code(self) -> str:
        return f'{spaces(2)}self.{self.name}: {self.type_name()} = values.get("{self.name}", {repr(self.default)})'

    def to_class_code(self, level: int = 0):
        raise ValueError(f'Cannot convert [{self.type_name()}] to class!')


class Definition(Item):
    def __init__(self, name: str, path: str):
        super().__init__(name=name)
        self.path = path

    def to_init_code(self) -> str:
        return f'{spaces(2)}self.{self.name} = {self.class_name()}(values=values.get("{self.name}"))'

    def to_class_code(self, level: int = 0) -> str:
        raise ValueError(f'Cannot convert [{self.type_name()}] to class!')


class Enum(Basic):
    def __init__(self, name: str, enum: list, default: Any = None):
        super().__init__(name=name, type='enum', default=default)
        self.enum = enum

    def to_class_code(self, level: int = 0) -> str:
        result = [
            f'class {self.class_name()}:',
            f'{spaces(1)}def __init__(self, values=None):',
            f'{spaces(2)}self.enum = {repr(self.enum)}',
            f'{spaces(2)}self.value = values if values is None else {repr(self.default)}'
        ]
        code = '\n'.join(result)
        return indent_class(code=code, level=level)


class Array(Basic):
    def __init__(self, name: str, items: Item = None, default: Any = None):
        super().__init__(name=name, type='array', default=default)
        self.items = items

    def to_json(self):
        return {
            **super().to_json(),
            'items': self.items.to_json()
        }

    def type_name(self):
        return f'List[{self.items.type_name()}]'

    def to_init_code(self) -> str:
        return '{spaces}self.{name}: {type_name} = values.get("{name}", {default})'.format(
            spaces=spaces(2),
            name=self.name,
            type_name=self.type_name(),
            default=repr(self.default or [])
        )

    def to_class_code(self, level: int = 0) -> str:
        result = [f'class {self.class_name()}:']
        if isinstance(self.items, Model):
            result.append(self.items.to_class_code(level=1))
        result.append(f'{spaces(1)}def __init__(self, values: list = None):')
        result.append(f'{spaces(2)}self.items: {self.type_name()} = [')
        result.append(f'{spaces(3)}{self.items.type_name()}(values=value) for value in (values or [])')
        result.append(f'{spaces(2)}]')
        code = '\n'.join(result)
        return indent_class(code=code, level=level)


class Model(Item):
    def __init__(self, name: str):
        super().__init__(name=name)
        self.properties: List[Item] = []
        self._in_definitions = False

    def set_in_definitions(self):
        self._in_definitions = True

    def inner_models(self) -> List['Model']:
        return [item for item in self.properties if isinstance(item, Model)]

    def to_json(self):
        return {
            **super().to_json(),
            'properties': dict((item.name, item.to_json()) for item in self.properties)
        }

    def to_init_code(self):
        prefix = '' if self._in_definitions else 'self.'
        return f'{spaces(2)}self.{self.name} = {prefix}{self.class_name()}(values=values.get("{self.name}", {{}}))'

    def to_class_code(self, level: int = 0) -> str:
        result = [f'class {self.class_name()}:']
        for item in self.inner_models():
            result.append(item.to_class_code(level=1))
            result.append('')
        result.append(f'{spaces(1)}def __init__(self, values: dict = None):')
        result.append('\n'.join(item.to_init_code() for item in self.properties))

        return indent_class(code='\n'.join(result), level=level)


class Parser:
    def __init__(self):
        self.definitions: Dict[str, Item] = {}
        self.root: Item = None

    def parse_object(self, name: str, schema: dict) -> Model:
        model = Model(name=name)
        for name, definition in schema.get('properties', {}).items():
            item = self.parse_definition(name=name, schema=definition)
            model.properties.append(item)
        return model

    def parse_array(self, name: str, schema: dict) -> Array:
        items = self.parse_definition('items', schema['items'])
        return Array(name=name, items=items, default=schema.get('default', None))

    def parse_definition(self, name: str, schema: dict) -> Item:
        default = schema.get('default', None)

        if 'type' in schema:
            item_type = schema['type']
            if item_type == 'object':
                return self.parse_object(name=name, schema=schema)
            elif item_type == 'array':
                return self.parse_array(name=name, schema=schema)
            else:
                return Basic(name=name, type=item_type, default=default)
        elif 'enum' in schema:
            return Enum(name=name, enum=schema['enum'], default=default)
        elif '$ref' in schema:
            path = schema['$ref']
            name = self.definitions[path].name
            return Definition(name=name, path=path)
        else:
            raise ValueError(f'Cannot parse schema {repr(schema)}')

    def parse(self, schema: dict):
        for name, definition in schema.get('definitions', {}).items():
            item = self.parse_definition(name=name, schema=definition)
            self.definitions[f'#/definitions/{name}'] = item
            if isinstance(item, Model):
                item.set_in_definitions()

        name = schema['title']
        self.root = self.parse_definition(name=name, schema=schema)

    def generate(self) -> str:
        result = [
            'from typing import List',
            '\n'
        ]
        for path, definition in self.definitions.items():
            result.append(definition.to_class_code(level=0))
            result.append('\n')
        result.append(self.root.to_class_code(level=0))
        return '\n'.join(result) + '\n'


def generate_file(schema_path: Path, output_path: Path, lazy: bool = True):
    with open(str(schema_path)) as f:
        schema = json.load(f)

    parser = Parser()
    parser.parse(schema=schema)
    result = parser.generate()

    if lazy and output_path.exists():
        if output_path.lstat().st_mtime > schema_path.lstat().st_mtime:
            return

    with open(str(output_path), 'w') as f:
        f.write(result)


def main():  # pragma: no cover
    arg_parser = argparse.ArgumentParser(description='JSON Schema to Python Class')
    arg_parser.add_argument('schema_path', type=str)
    arg_parser.add_argument('-o', '--output-path', type=str)

    arguments = arg_parser.parse_args()
    generate_file(Path(arguments.schema_path), Path(arguments.output_path), lazy=False)


if __name__ == '__main__':
    main()  # pragma: no cover
