from config import config


class ParseMetadata:
    """Класс предназначен для обработки метаданных 'Parametrica' и
    записи обработанных данных в файл в читаемом для пользователя виде.
    Для создания экземпляра класса нужно передать такие аргументы как:
     metadata - обрабатываемые метаданные и
     required_field - поля, данные которых вы желаете получить.
     По умолчанию получаемые поля: label, type, default"""

    def __init__(self, metadata: dict, required_field: dict):
        self.metadata = metadata
        self.__fields = required_field
        self.data = {}

    @property
    def fields(self) -> dict:
        """Добавляет к полям по умолчанию поля, которые
        нужны пользователю."""

        fields = {'Описание поля': 'label',
                  'Тип поля': 'type',
                  'Значение по умолчанию': 'default'}
        fields.update(self.__fields)
        return fields

    def _parse_metadata(self, data: dict) -> dict:
        """Преобразует метаданные. Оставляет только вложенные поля.
        Где metadata - данные, которые нужно обработать."""

        for field, value in data.items():
            data_type = value.get('type')
            if isinstance(data_type, dict):
                self._parse_metadata(data_type)
            else:
                self.data[field] = value

        return self.data

    def write_data_to_file(self, parsed_metadata: dict, filename: str = 'test.txt') -> None:
        """Запись данных в файл в читаемом для пользователя виде.
        Где parsed_metadata - обработанные данные,
        filename - название файла в который буду записаны данные."""

        with open(f'../{filename}', 'w') as file:
            for field, value in parsed_metadata.items():
                file.write(f'Поле: {field}\n')

                for name, info in self.fields.items():
                    file.write(f'    {name}: {value.get(info, None)}\n')

    def run(self):
        """Головная функция."""

        self._parse_metadata(self.metadata)
        self.write_data_to_file(self.data)


if __name__ == '__main__':
    meta_data = config.__metadata__()

    req_field = {'Подсказка': 'hint', 'Секретное ли поле': 'secret', 'Ограничение': 'rule'}
    parse_metadata = ParseMetadata(meta_data, req_field)

    parse_metadata.run()
