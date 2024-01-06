import pytest


@pytest.fixture()
def data_for_parse():
    """Выводит сгенерированные метаданные."""

    data = {'common': {'hint': 'Сюда вписывать примитивы',
                       'is_iterable': False,
                       'is_primitive': False,
                       'label': 'Общие поля для примера',
                       'name': 'common',
                       'password': False,
                       'secret': False,
                       'type': {'int_field': {'default': 220,
                                              'hint': 'Записывается сюда какое-то '
                                                      'значение целочисленное',
                                              'is_iterable': False,
                                              'is_primitive': True,
                                              'label': 'Интовое поле',
                                              'name': 'int_field',
                                              'password': False,
                                              'rule': None,
                                              'secret': False,
                                              'type': 'int'},
                                'string': {'default': 'STR',
                                           'hint': 'Используется для хранения строки',
                                           'is_iterable': False,
                                           'is_primitive': True,
                                           'label': 'Строчный тип типа',
                                           'name': 'string',
                                           'password': False,
                                           'rule': None,
                                           'secret': False,
                                           'type': 'str'},
                                'tuple_field': {'default': (False, True, True),
                                                'hint': '',
                                                'is_iterable': True,
                                                'is_primitive': True,
                                                'label': 'Кортеж',
                                                'name': 'tuple_field',
                                                'password': False,
                                                'rule': None,
                                                'secret': False,
                                                'type': 'bool'}
                                }
                       },
            'custom_default': {'hint': '',
                               'is_iterable': False,
                               'is_primitive': False,
                               'label': 'Кастомное дефолт значение 1',
                               'name': 'custom_default',
                               'password': False,
                               'secret': False,
                               'type': {'default_1234': {'default': 1111,
                                                         'hint': '',
                                                         'is_iterable': False,
                                                         'is_primitive': True,
                                                         'label': 'Тут должно было быть '
                                                                  '1234',
                                                         'name': 'default_1234',
                                                         'password': False,
                                                         'rule': None,
                                                         'secret': False,
                                                         'type': 'int'}
                                        }
                               }
            }

    return data


@pytest.fixture()
def expected_data_for_parse():
    """Выводит ожидаемые данные записанные в txt файл."""

    expected_data = (
        'Поле common\n'
        '    Описание поля: Общие поля для примера\n'
        '    Подсказка: Сюда вписывать примитивы\n'
        '    Поле int_field\n'
        '        Описание поля: Интовое поле\n'
        '        Тип поля: целочисленное\n'
        '        Значение по умолчанию: 220\n'
        '        Подсказка: Записывается сюда какое-то значение целочисленное\n'
        '    Поле string\n'
        '        Описание поля: Строчный тип типа\n'
        '        Тип поля: строка\n'
        '        Значение по умолчанию: STR\n'
        '        Подсказка: Используется для хранения строки\n'
        '    Поле tuple_field\n'
        '        Описание поля: Кортеж\n'
        '        Тип поля: кортеж\n'
        '        Значение по умолчанию: (False, True, True)\n'
        'Поле custom_default\n'
        '    Описание поля: Кастомное дефолт значение 1\n'
        '    Поле default_1234\n'
        '        Описание поля: Тут должно было быть 1234\n'
        '        Тип поля: целочисленное\n'
        '        Значение по умолчанию: 1111\n')

    return expected_data


@pytest.fixture()
def expected_data_for_parse_only_primitive():
    """Выводит ожидаемые данные записанные в txt файл."""

    expected_data = (
        'Поле int_field\n'
        '    Описание поля: Интовое поле\n'
        '    Тип поля: целочисленное\n'
        '    Значение по умолчанию: 220\n'
        '    Подсказка: Записывается сюда какое-то значение целочисленное\n'
        'Поле string\n'
        '    Описание поля: Строчный тип типа\n'
        '    Тип поля: строка\n'
        '    Значение по умолчанию: STR\n'
        '    Подсказка: Используется для хранения строки\n'
        'Поле tuple_field\n'
        '    Описание поля: Кортеж\n'
        '    Тип поля: кортеж\n'
        '    Значение по умолчанию: (False, True, True)\n'
        'Поле default_1234\n'
        '    Описание поля: Тут должно было быть 1234\n'
        '    Тип поля: целочисленное\n'
        '    Значение по умолчанию: 1111\n')

    return expected_data
