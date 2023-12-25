import os
from enum import Enum
from typing import Optional
from dataclasses import dataclass

from config import config


@dataclass(frozen=True)
class Fields:
    label: str = 'Описание поля'
    type: str = 'Тип поля'
    default: str = 'Значение по умолчанию'
    hint: str = 'Подсказка'
    secret: str = 'Секретное ли поле'
    rule: str = 'Ограничение'


class MetadataAction:
    """
    Класс предназначен для обработки метаданных 'Parametrica' и
    записи обработанных данных в файл в читаемом для пользователя виде.
    Для создания экземпляра класса нужно передать такие аргументы как:
     data - обрабатываемые метаданные и
     filename - название файла, в который будут сохранены данные,
     args - дополнительные поля
     По дефолту получаемые поля находятся в REQUIRED_FIELDS.
    """

    REQUIRED_FIELDS = {}

    def __init__(
            self, data: dict, *, filename: str,
            only_primitive: bool = False,
            label: bool = True, type: bool = True,
            default: bool = True, hint: bool = False,
            secret: bool = False, rule: bool = False
    ) -> None:
        self.metadata = data
        self.filename = filename
        self.only_primitive = only_primitive
        self.fields = (label, type, default, hint, secret, rule)
        self.space = 0

    def _add_extra_fields(self) -> None:
        """Добавляет дополнительные требуемые поля в REQUIRED_FIELDS,
        которые будут выведены в файл txt."""

        fields = ['label', 'type', 'default',
                  'hint', 'secret', 'rule']

        for num, is_field in enumerate(self.fields):
            if is_field:
                field = fields[num]
                self.REQUIRED_FIELDS[field] = Fields.__getattribute__(Fields, field)

    def _parse_metadata(self) -> None:
        """Разбирает данные и передает их функции write_parsed_data_to_file,
        которая в свою очередь их записывает."""

        for field, data_field in self.metadata.items():
            if data_field.get('is_primitive'):
                self._write_parsed_data_to_file(field, data_field, self.space)

            else:
                self.metadata = data_field.get('type')

                if not self.only_primitive:
                    data_field.pop('type')
                    self._write_parsed_data_to_file(field, data_field, self.space)
                    self.space += 4

                self._parse_metadata()
                self.space = 0

    def _write_parsed_data_to_file(self, field: str, data: dict, space: int) -> None:
        """Записывает полученные данные в файл. Где
        field - общее поле, data - данные этого поля,
        space - количество пробелов."""

        with open(f'{self.filename}.txt', 'a') as file:
            if not data.get('secret'):
                file.write(' ' * space + f'Поле {field}\n')
                for name, info in self.REQUIRED_FIELDS.items():
                    value = self._get_value(name, data)

                    if value:
                        file.write(' ' * (space + 4) + f'{info}: {value}\n')

    def _get_value(self, name: str, data: dict) -> Optional[str]:
        """Возвращает значение поля."""

        data_value = data.get(name)

        if isinstance(data_value, Enum):
            data_value = data.get(name).value

        if name == 'rule':
            if data_value:
                if 'Match' in f'{data_value}':
                    return 'Регулярное выражение'
                else:
                    return data_value

        else:
            if name == 'type':
                if data.get('is_iterable'):
                    data_value = 'tuple'
                data_value = self._get_type(data_value)

            if name == 'secret':
                if data.get(name):
                    data_value = 'Да'
                else:
                    data_value = 'Нет'

            if not data_value:
                data_value = 'Значение не установлено'

            return data_value

    @staticmethod
    def _get_type(value: str) -> str:
        """Возвращает тип поля в понятном человеке виде."""

        types = {'int': 'целочисленное',
                 'str': 'строка',
                 'bool': 'логическое',
                 'float': 'вещественное',
                 'tuple': 'кортеж'}

        return types.get(value)

    def run(self) -> None:
        """Осуществляет взаимодействие с функциями:
        _add_extra_fields и _parse_metadata."""

        if os.path.exists(f'{self.filename}.txt'):
            os.remove(f'{self.filename}.txt')
        self._add_extra_fields()
        self._parse_metadata()


if __name__ == '__main__':
    metadata: dict = config.__metadata__()
    wm = MetadataAction(metadata, filename='test',
                        only_primitive=False, hint=True,
                        secret=True, rule=True)
    wm.run()
