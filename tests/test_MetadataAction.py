import os
from enum import Enum

import pytest

try:
    from src.metadata_action import MetadataAction
except ImportError as er:
    raise ImportError(f'Проблем импорта класса MetadataAction: {er}')


class EnumTestClass(Enum):
    value1 = 'TestValue1'
    value2 = 'TestValue2'
    value3 = 'TestValue3'


class TestMetadataAction:
    """Данный класс тестирует функциональность класса MetadataAction."""

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

    @pytest.mark.parametrize(
        'interface',
        [
            '_add_extra_fields',
            '_parse_metadata',
            '_write_parsed_data_to_file',
            '_get_value',
            '_get_type',
            'run',
        ],
    )
    def test_interface(self, interface):
        """Проверяет наличие свойств и методов класса."""

        attrs_and_methods = MetadataAction.__dict__
        assert (
            interface in attrs_and_methods
        ), f'Атрибута {interface} нет в классе MetadataAction'

    @pytest.mark.parametrize(
        'metadata, expected_length, expected_result',
        [
            (metadata_default, 3, expected_fields_default),
            (metadata_only_primitive, 3, expected_fields_default),
            (metadata_full, 5, expected_fields_extra),
        ],
    )
    def test_add_extra_fields(self, metadata, expected_length, expected_result):
        """Проверяет данные, которые находятся в REQUIRED_FIELDS
        после вызова функции _add_extra_fields."""

        metadata._add_extra_fields()
        result = metadata.required_fields
        result_length = len(result)

        assert (
            result_length == expected_length
        ), 'Неверное количество полей REQUIRED_FIELDS'
        assert (
            result == expected_result
        ), f'В REQUIRED_FIELDS ожидаются такие данные: {expected_result}'

    @pytest.mark.parametrize(
        'name, data, expected_result',
        [
            ('rule', {'rule': 'Test value'}, 'Test value'),
            ('rule', {'rule': 'Match([A-Za-z1-9].#$)'}, 'Регулярное выражение'),
            ('test', {'test': EnumTestClass.value3}, 'TestValue3'),
            ('type', {'type': 'int', 'is_iterable': False}, 'целочисленное'),
            ('type', {'type': 'int', 'is_iterable': True}, 'кортеж'),
            ('hint', {'hint': 'Test hint'}, 'Test hint'),
            ('default', {'default': 'Test default'}, 'Test default'),
        ],
    )
    def test_get_value(self, name, data, expected_result):
        """Проверяет функцию _get_value на корректную обработку данных."""

        result = self.metadata_full._get_value(name=name, data=data)

        assert result == expected_result, (
            'Функция _get_value вернула некорректное значение. '
            f'Результат работы: {result}, ожидалось: {expected_result}'
        )

    @pytest.mark.parametrize(
        'value, expected_result',
        [
            ('int', 'целочисленное'),
            ('str', 'строка'),
            ('bool', 'логическое'),
            ('float', 'вещественное'),
            ('tuple', 'кортеж'),
            ('none', 'none'),
        ],
    )
    def test_get_type(self, value, expected_result):
        """Проверяет функцию _get_type на корректный вывод типа в удобочитаемом виде."""

        result = self.metadata_full._get_type(value=value)

        assert result == expected_result, (
            'Функция _get_type вернула некорректное значение. '
            f'Результат работы: {result}, ожидалось: {expected_result}'
        )

    def test_parse_metadata(self, tmpdir, data_for_parse, expected_data_for_parse):
        """Проверяет правильность обработки данных метода _parse_metadata и запись их в файл."""

        test_file = tmpdir.join('test.txt')
        metadata = MetadataAction(
            data_for_parse, filename=str(test_file), hint=True, rule=True
        )

        metadata._add_extra_fields()
        metadata._parse_metadata()
        file_size = os.path.getsize(test_file)

        assert file_size == 1238, (
            'Размер txt файла некорректный '
            f'Ожидалось: 1238, а получилось: {file_size}'
        )
        assert test_file.read() == expected_data_for_parse, (
            'Данные в txt файле не совпадают с ожидаемым значением\n'
            f'Результат работы:\n {test_file.read()},\n '
            f'Ожидалось: \n{expected_data_for_parse}'
        )

    def test_parse_metadata_only_primitive(
        self, tmpdir, data_for_parse, expected_data_for_parse_only_primitive
    ):
        """Проверяет правильность обработки данных метода _parse_metadata и запись их в файл."""

        test_file = tmpdir.join('test.txt')
        metadata = MetadataAction(
            data_for_parse,
            filename=str(test_file),
            only_primitive=True,
            hint=True,
            rule=True,
        )

        metadata._add_extra_fields()
        metadata._parse_metadata()
        file_size = os.path.getsize(test_file)

        assert file_size == 900, (
            'Размер txt файла некорректный '
            f'Ожидалось: 900, а получилось: {file_size}'
        )
        assert test_file.read() == expected_data_for_parse_only_primitive, (
            'Данные в txt файле не совпадают с ожидаемым значением\n'
            f'Результат работы:\n {test_file.read()},\n '
            f'Ожидалось: \n{expected_data_for_parse_only_primitive}'
        )

    @pytest.mark.parametrize(
        'field, data, expected_result, expected_file_size',
        [
            (
                'common',
                {'hint': 'Test hint', 'label': 'Test label', 'secret': False},
                (
                    'Поле common\n    Описание поля: Test label\n    Подсказка: Test hint\n'
                ),
                92,
            ),
            ('string', {'label': 'Test label', 'secret': True}, '', 0),
            (
                'tuple',
                {'type': 'str', 'secret': False},
                'Поле tuple\n    Тип поля: строка\n',
                49,
            ),
        ],
    )
    def test_write_parsed_data_to_file(
        self,
        field: str,
        data: dict,
        expected_result: str,
        expected_file_size: int,
        tmpdir,
    ) -> None:
        """Проверяет правильность метода _write_parsed_data_to_file."""

        test_file = tmpdir.join('test.txt')
        metadata = MetadataAction({}, filename=str(test_file), hint=True, rule=True)

        metadata._add_extra_fields()
        metadata._write_parsed_data_to_file(field=field, data=data)
        file_size = os.path.getsize(test_file)

        assert file_size == expected_file_size, (
            'Размер txt файла некорректный '
            f'Ожидалось: {expected_file_size}, а получилось: {file_size}'
        )
        assert test_file.read() == expected_result, (
            'Данные в txt файле не совпадают с ожидаемым значением\n'
            f'Результат работы:\n {test_file.read()},\n '
            f'Ожидалось: \n{expected_result}'
        )
