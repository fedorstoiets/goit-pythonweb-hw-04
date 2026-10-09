# goit-pythonweb-hw-04

Домашнє завдання №4 з курсу **FullStack Web Development with Python**.

Проєкт реалізує асинхронне сортування файлів із вихідної директорії у цільову директорію за розширеннями файлів.

## Автор

**Fedor Stoietskyi**

---

## Мета завдання

Скрипт:

- приймає вихідну та цільову директорії через аргументи командного рядка;
- рекурсивно читає всі файли у вихідній директорії;
- асинхронно копіює файли;
- сортує файли по підпапках за їх розширенням;
- обробляє файли без розширення;
- логуванням повідомляє про процес роботи та помилки.

---

## Використані технології

- Python 3
- asyncio
- argparse
- pathlib
- shutil
- logging

---

## Структура проєкту

```text
goit-pythonweb-hw-04/
│
├── main.py
├── README.md
└── .gitignore
```

Тестові директорії та результати сортування не додаються до репозиторію.
Запуск програми
Загальний формат:
python main.py <source_folder> <output_folder>

Наприклад:
python main.py test_source sorted_files

Аргументи командного рядка
Скрипт використовує argparse.
Переглянути довідку:
python main.py --help

Приклад:
usage: main.py [-h] source output

Asynchronously sort files from a source folder into subfolders by file extension.

positional arguments:
source Path to the source folder
output Path to the output folder

Принцип роботи
Вихідна структура:
test_source/
├── notes.txt
├── report.pdf
├── photo.jpg
├── README
│
└── nested/
├── data.csv
└── second.jpg

Після запуску:
python main.py test_source sorted_files

отримуємо:
sorted_files/
├── csv/
│ └── data.csv
│
├── jpg/
│ ├── photo.jpg
│ └── second.jpg
│
├── no_extension/
│ └── README
│
├── pdf/
│ └── report.pdf
│
└── txt/
└── notes.txt

Сортування за розширенням
Для кожного файлу визначається його розширення.
Наприклад:
.txt -> txt/
.jpg -> jpg/
.pdf -> pdf/
.csv -> csv/

Файли без розширення потрапляють у:
no_extension/

Асинхронна обробка
Файлові операції є блокуючими, тому вони запускаються через:
asyncio.to_thread(...)

Копіювання кількох файлів виконується конкурентно за допомогою:
await asyncio.gather(\*tasks)

Це дозволяє ефективніше обробляти велику кількість файлів.
Рекурсивне читання
Для пошуку файлів у вкладених директоріях використовується:
source_folder.rglob("\*")

Тому програма обробляє не тільки файли у кореневій папці, а й файли у всіх підпапках.
Логування
Програма використовує стандартний модуль:
logging

Приклад успішного виконання:
INFO - Source folder: C:\...\test_source
INFO - Output folder: C:\...\sorted_files
INFO - Found 6 file(s). Starting asynchronous copy.
INFO - Copied: ...
INFO - Sorting completed successfully.

Обробка помилок
Якщо вихідної директорії не існує, програма не завершується аварійно, а записує помилку в лог:
ERROR - Source folder does not exist: ...

Також логуються помилки, які можуть виникнути під час копіювання файлів.
Форматування коду
Код відформатовано за допомогою Black.
Форматування:
python -m black main.py

Перевірка:
python -m black --check main.py

Очікуваний результат:
All done! ✨ 🍰 ✨
1 file would be left unchanged.
