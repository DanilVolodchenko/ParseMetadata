from enum import Enum
from typing import List, Tuple, Dict

from src.metadata_action import MetadataAction


class EnumTestClass(Enum):
    value1: str = 'TestValue1'
    value2: str = 'TestValue2'
    value3: str = 'TestValue3'


data_for_interface: List[str] = [
    '_add_extra_fields',
    '_parse_metadata',
    '_write_parsed_data_to_file',
    '_get_value',
    '_get_type',
    'run',
]

data_for_get_value: List[Tuple[str, Dict[str, str], str]] = [
    ('rule', {'rule': 'Test value'}, 'Test value'),
    ('rule', {'rule': 'Match([A-Za-z1-9].#$)'}, 'Регулярное выражение'),
    ('test', {'test': EnumTestClass.value3}, 'TestValue3'),
    ('type', {'type': 'int', 'is_iterable': False}, 'целочисленное'),
    ('type', {'type': 'int', 'is_iterable': True}, 'кортеж'),
    ('hint', {'hint': 'Test hint'}, 'Test hint'),
    ('default', {'default': 'Test default'}, 'Test default'),
]

data_for_get_type: List[Tuple[str, str]] = [
    ('int', 'целочисленное'),
    ('str', 'строка'),
    ('bool', 'логическое'),
    ('float', 'вещественное'),
    ('tuple', 'кортеж'),
    ('none', 'none'),
]

data_for_write_parsed_data_to_file: List[Tuple[str, dict, str, int]] = [
    (
        'common',
        {'hint': 'Test hint', 'label': 'Test label', 'secret': False},
        'Поле common\n    Описание поля: Test label\n    Подсказка: Test hint\n',
        92,
    ),
    ('string', {'label': 'Test label', 'secret': True}, '', 0),
    (
        'tuple',
        {'type': 'str', 'secret': False},
        'Поле tuple\n    Тип поля: строка\n',
        49,
    ),
]


def data_for_add_extra_fields() -> List[Tuple[MetadataAction, int, Dict[str, str]]]:
    """Данные для функции тестирования test_add_extra_fields."""

    metadata_default = MetadataAction({}, filename='test')
    metadata_only_primitive = MetadataAction({}, filename='test', only_primitive=True)
    metadata_full = MetadataAction({}, filename='test', hint=True, rule=True)

    expected_fields_default = {
        'label': 'Описание поля',
        'type': 'Тип поля',
        'default': 'Значение по умолчанию',
    }

    expected_fields_extra = {
        'label': 'Описание поля',
        'type': 'Тип поля',
        'default': 'Значение по умолчанию',
        'hint': 'Подсказка',
        'rule': 'Ограничение',
    }

    data = [
        (metadata_default, 3, expected_fields_default),
        (metadata_only_primitive, 3, expected_fields_default),
        (metadata_full, 5, expected_fields_extra),
    ]

    return data
