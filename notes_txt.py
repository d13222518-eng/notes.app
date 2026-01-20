#для начала скопируй сюда интерфейс "Умных заметок" и проверь его работу

#затем запрограммируй демо-версию функционала
# імпортуємо потрібні класи з PyQt5
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QListWidget, QLineEdit, QTextEdit,
    QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout
)

# імпортуємо бібліотеку для роботи з JSON
import json


# --------- ДАНІ ЗАМІТОК ---------

# словник, у якому зберігаються всі замітки
# ключ — назва замітки
# значення — словник з текстом і тегами
notes = {

    "Ласкаво просимо!": {
        "текст": "Це найкращий додаток для заміток у світі!",
        "теги": ["добро", "інструкція"]
    }

}

# записуємо початкові замітки у файл JSON
with open("notes_data.json", "w", encoding="utf-8") as file:
    json.dump(notes, file)


# --------- СТВОРЕННЯ ПРОГРАМИ ---------

# створюємо об'єкт QApplication (обов'язково для PyQt)
app = QApplication([])


# --------- ВІКНО ПРОГРАМИ ---------

# створюємо головне вікно
notes_win = QWidget()
notes_win.setWindowTitle('Розумні замітки')  # заголовок вікна
notes_win.resize(900, 600)                   # розмір вікна


# --------- ВІДЖЕТИ ---------

# список заміток
list_notes = QListWidget()
list_notes_label = QLabel('Список заміток')

# кнопки для роботи із замітками
button_note_create = QPushButton('Створити замітку')
button_note_del = QPushButton('Видалити замітку')
button_note_save = QPushButton('Зберегти замітку')

# поле введення тегу
field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введіть тег...')

# поле для тексту замітки
field_text = QTextEdit()

# кнопки для роботи з тегами
button_tag_add = QPushButton('Додати до замітки')
button_tag_del = QPushButton('Відкріпити від замітки')
button_tag_search = QPushButton('Шукати замітки по тегу')

# список тегів
list_tags = QListWidget()
list_tags_label = QLabel('Список тегів')


# --------- РОЗМІЩЕННЯ ЕЛЕМЕНТІВ (LAYOUT-и) ---------

# головний горизонтальний layout
layout_notes = QHBoxLayout()

# ліва колонка (текст замітки)
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

# права колонка (списки та кнопки)
col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

# ряд кнопок створення та видалення
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)

# ряд кнопки збереження
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)

# додаємо ряди в праву колонку
col_2.addLayout(row_1)
col_2.addLayout(row_2)

# додаємо список тегів і поле введення
col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

# ряд кнопок для тегів
row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)

# ряд кнопки пошуку
row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)


# додаємо layout-и до головного layout
layout_notes.addLayout(col_1, stretch=2)  # ліва частина ширша
layout_notes.addLayout(col_2, stretch=1)  # права частина вужча

# встановлюємо layout для вікна
notes_win.setLayout(layout_notes)


# --------- ФУНКЦІЇ ---------
def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Додати замітку", "Назва замітки: ")
    if ok and note_name != "":

        notes[note_name] = {"текст" : "", "теги" : []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]["теги"])

       


def show_note():
    # отримуємо текст із замітки з виділеною назвою та відображаємо її в полі редагування
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[key]["теги"])


def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = field_text.toPlainText()

        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False, indent=2)
        print(notes)

    else:
        print("Замітка для збереження не вибрана!")

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()

        del notes[key]

        list_notes.clear()
        list_tags.clear()
        field_text.clear()

        list_notes.addItems(notes)

        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file)
       

    else:
        print("Замітка для видалення не вибрана!")


def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()

        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
       
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file)
       
    else:
        print("Замітка для додавання не вибрана!")
       
def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.selectedItems()[0].text()

        notes[key]["теги"].remove(tag)

        list_tags.clear()

        list_tags.addItems(notes[key]["теги"])

        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file)
       
    else:
        print("Тег не вибраний для видалення!")

def search_tag():
    print(button_tag_search.text())
    tag = field_tag.text()
    if button_tag_search.text() == "Шукати замітки за тегом" and tag:
        print(tag)
        notes_filtered = {} # тут будуть замітки з виділеним тегом
        for note in notes:
            if tag in notes[note]["теги"]: 
                notes_filtered[note]=notes[note]
        button_tag_search.setText("Скинути пошук")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
        
    elif button_tag_search.text() == "Скинути пошук":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Шукати замітки за тегом")
        
    else:
        pass
# --------- ПОДІЇ ---------

# при кліку на замітку викликається функція show_note
# підключення обробки подій
button_note_create.clicked.connect(add_note)
list_notes.itemClicked.connect(show_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)
# --------- ЗАВАНТАЖЕННЯ ДАНИХ З JSON ---------

# читаємо замітки з файлу
with open("notes_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# додаємо назви заміток у список
list_notes.addItems(data)


# --------- ЗАПУСК ПРОГРАМИ ---------

# показуємо вікно
notes_win.show()

# запускаємо головний цикл програми
app.exec_()