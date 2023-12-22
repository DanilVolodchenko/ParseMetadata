# ParseMetadata

---

## Описание
Данный проект создан для обработки метаданных библиотеки Parametrica, которые прописываются в
файле config.py. Он обрабатывает полученные данные и записывает в txt файл данные в удобочитаемом формате.

---

## Принцип взаимодействия

Находясь в файле с расширением .py импортирует класс MetadataAction. Создаем его экземпляр
и передаем параметры: сами данные и названия файла, в который нужно сохранить данные.

---

### Пример кода

```python
from metadata_action import MetadataAction
from config import config

metadata = config.__metadata__()
filename = 'test'

meta_action = MetadataAction(metadata, filename, rule=True)
meta_action.run()
```

---

`В данном примере будут обработаны данные которые находятся в переменной metadata,
а сохранены будут в файл test.txt`

Класс MetadataAction принимает такие параметры как:
* `data` - данные которые нужно обработать
* `filename` - название файла в который нужно записать данные
* `only_primitive` - отвечает за добавление только примитивных полей. По умолчанию `False`
* `label` - добавляет описание поля. По умолчанию `True`
* `type` - добавляет тип поля. По умолчанию `True`
* `default` - добавляет значение по умолчанию. По умолчанию `True`
* `hint` - добавляет подсказку. По умолчанию `False`
* `secret` - добавляет секретное поле. По умолчанию `False`
* `rule` - добавляет ограничение. По умолчанию `False`

---

По итогу должен получиться примерно следующий .txt файл:
```text
Поле common
    Описание поля: Общие поля для примера
    Тип поля: Не установлено
    Значение по умолчанию: Не установлено
    Ограничение: Не установлено
    Поле int_field
        Описание поля: Интовое поле
        Тип поля: int
        Значение по умолчанию: 220
    Поле flag
        Описание поля: Флаг значение
        Тип поля: bool
        Значение по умолчанию: Пусто
    Поле string
        Описание поля: Строчный тип типа
        Тип поля: str
        Значение по умолчанию: STR
    Поле enum_field
        Описание поля: Тут хранится enum
        Тип поля: MyEnum
        Значение по умолчанию: value2
```