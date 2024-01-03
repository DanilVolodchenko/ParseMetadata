from enum import Enum

import pytest

try:
    from metadata_action import MetadataAction
except ImportError:
    raise ImportError('Проблем импорта класса MetadataAction')


class EnumTestClass(Enum):
    value1 = 'TestValue1'
    value2 = 'TestValue2'
    value3 = 'TestValue3'


class TestMetadataAction:
    """Данный класс тестирует функциональность класса MetadataAction."""

    metadata_default = MetadataAction({}, filename='test')
    metadata_only_primitive = MetadataAction({}, filename='test', only_primitive=True)
    metadata_full = MetadataAction({}, filename='test', hint=True, rule=True)

    expected_fields_default = {'label': 'Описание поля',
                               'type': 'Тип поля',
                               'default': 'Значение по умолчанию'}

    expected_fields_extra = {'label': 'Описание поля',
                             'type': 'Тип поля',
                             'default': 'Значение по умолчанию',
                             'hint': 'Подсказка',
                             'rule': 'Ограничение'
                             }

    @pytest.mark.parametrize('interface', [
        'REQUIRED_FIELDS',
        '_add_extra_fields',
        '_parse_metadata',
        '_write_parsed_data_to_file',
        '_get_value',
        '_get_type',
        'run'
    ])
    def test_interface(self, interface):
        """Проверяет наличие атрибутов и методов класса."""

        attrs_and_methods = MetadataAction.__dict__
        assert interface in attrs_and_methods, 'Атрибута REQUIRED_FIELDS нет в классе MetadataAction'

    @pytest.mark.parametrize('metadata, expected_length, expected_result', [
        (metadata_default, 3, expected_fields_default),
        (metadata_only_primitive, 3, expected_fields_default),
        (metadata_full, 5, expected_fields_extra)
    ])
    def test_add_extra_fields(self, metadata, expected_length, expected_result):
        """Проверяет данные, которые находятся в REQUIRED_FIELDS
        после вызова функции _add_extra_fields."""

        metadata._add_extra_fields()
        result = metadata.REQUIRED_FIELDS
        result_length = len(result)

        assert result_length == expected_length, 'Неверное количество полей REQUIRED_FIELDS'
        assert result == expected_result, f'В REQUIRED_FIELDS ожидаются такие данные: {expected_result}'

    @pytest.mark.parametrize('name, data, expected_result', [
        ('rule', {'rule': 'Test value'}, 'Test value'),
        ('rule', {'rule': 'Match([A-Za-z1-9].#$)'}, 'Регулярное выражение'),
        ('test', {'test': EnumTestClass.value3}, 'TestValue3'),
        ('type', {'type': 'int', 'is_iterable': False}, 'целочисленное'),
        ('type', {'type': 'int', 'is_iterable': True}, 'кортеж'),
        ('hint', {'hint': 'Test hint'}, 'Test hint'),
        ('default', {'default': 'Test default'}, 'Test default')
    ])
    def test_get_value(self, name, data, expected_result):
        """Проверяет функцию _get_value на корректную обработку данных."""

        result = self.metadata_full._get_value(name=name, data=data)

        assert result == expected_result, ('Функция _get_value вернула некорректное значение. '
                                           f'Результат работы: {result}, ожидалось: {expected_result}')

    @pytest.mark.parametrize('value, expected_result', [
        ('int', 'целочисленное'),
        ('str', 'строка'),
        ('bool', 'логическое'),
        ('float', 'вещественное'),
        ('tuple', 'кортеж'),
        ('none', 'none'),
    ])
    def test_get_type(self, value, expected_result):
        """Проверяет функцию _get_type на корректый вывод типа в удобочитаемом виде."""

        result = self.metadata_full._get_type(value=value)

        assert result == expected_result, ('Функция _get_type вернула некорректное значение. '
                                           f'Результат работы: {result}, ожидалось: {expected_result}')
