import os

import pytest

try:
    from src.metadata_action import MetadataAction
    from .data_test import (data_for_get_value,
                            data_for_add_extra_fields, data_for_get_type,
                            data_for_write_parsed_data_to_file,
                            data_for_interface)
except ImportError as er:
    raise ImportError(f'Проблем импорта класса MetadataAction: {er}')


class TestMetadataAction:
    """Данный класс тестирует функциональность класса MetadataAction."""

    @pytest.mark.parametrize('interface', data_for_interface)
    def test_interface(self, interface):
        """Проверяет наличие свойств и методов класса."""

        attrs_and_methods = MetadataAction.__dict__
        assert (
                interface in attrs_and_methods
        ), f'Атрибута {interface} нет в классе MetadataAction'

    @pytest.mark.parametrize('metadata, expected_length, expected_result', data_for_add_extra_fields())
    def test_add_extra_fields(self, metadata, expected_length, expected_result):
        """Проверяет данные, которые находятся в REQUIRED_FIELDS
        после вызова функции _add_extra_fields."""

        metadata._add_extra_fields()
        result = metadata.required_fields
        result_length = len(result)

        assert (result_length == expected_length), 'Неверное количество полей в required_fields'
        assert (result == expected_result), f'В required_fields ожидаются такие данные: {expected_result}'

    @pytest.mark.parametrize('name, data, expected_result', data_for_get_value)
    def test_get_value(self, name, data, expected_result, metadata):
        """Проверяет функцию _get_value на корректную обработку данных."""

        result = metadata._get_value(name=name, data=data)

        assert result == expected_result, (
            'Функция _get_value вернула некорректное значение. '
            f'Результат работы: {result}, ожидалось: {expected_result}'
        )

    @pytest.mark.parametrize('value, expected_result', data_for_get_type)
    def test_get_type(self, value, expected_result, metadata):
        """Проверяет функцию _get_type на корректный вывод типа в удобочитаемом виде."""

        result = metadata._get_type(value=value)

        assert result == expected_result, (
            'Функция _get_type вернула некорректное значение. '
            f'Результат работы: {result}, ожидалось: {expected_result}'
        )

    def test_parse_metadata(self, tmpdir, data_for_parse, expected_data_for_parse):
        """Проверяет правильность обработки данных метода _parse_metadata и запись их в файл."""

        test_file = tmpdir.join('test.txt')
        metadata = MetadataAction(data_for_parse, filename=str(test_file), hint=True, rule=True)

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

    def test_parse_metadata_only_primitive(self, tmpdir, data_for_parse, expected_data_for_parse_only_primitive):
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
        data_for_write_parsed_data_to_file
    )
    def test_write_parsed_data_to_file(self,
                                       field: str,
                                       data: dict,
                                       expected_result: str,
                                       expected_file_size: int,
                                       tmpdir, ) -> None:
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
