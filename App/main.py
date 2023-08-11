import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QListWidget, QVBoxLayout, QWidget, QLabel, QListWidgetItem, QHBoxLayout, QInputDialog, QMessageBox
from PyQt5.QtCore import QFile, Qt
from datetime import datetime
import os

class App(QMainWindow):
    def __init__(self):
        super().__init__() 
        
        self.setWindowTitle("App")
        self.setGeometry(100, 100, 500, 500)

        
        self.central_widget = QWidget(self) # Tworzymy widget, który będzie centralnym elementem okna
        self.setCentralWidget(self.central_widget)  

        self.layout = QVBoxLayout()

        add_buttons_layout = QHBoxLayout()
        self.add_button = QPushButton("Add note", self)
        self.add_button.setObjectName("add_button")
        self.add_button.clicked.connect(self.add_note)
        self.add_button.setProperty("class", "add_button")
        add_buttons_layout.addWidget(self.add_button)   

        self.add_important_button = QPushButton("Add important note", self)
        self.add_important_button.setObjectName("add_important_button")
        self.add_important_button.clicked.connect(self.add_important_note) 
        self.add_important_button.setProperty("class", "add_important_button")
        add_buttons_layout.addWidget(self.add_important_button)             


        delete_buttons_layout = QHBoxLayout()
        self.delete_button = QPushButton("Delete", self)
        self.delete_button.setObjectName("delete_button")
        self.delete_button.clicked.connect(self.delete_notes)
        self.delete_button.setProperty("class", "delete_button")    
        delete_buttons_layout.addWidget(self.delete_button)

        self.delete_all_button = QPushButton("Delete all", self)
        self.delete_all_button.setObjectName("delete_all_button")
        self.delete_all_button.clicked.connect(self.delete_all_notes_from_file)
        self.delete_all_button.setProperty("class", "delete_all_button")
        delete_buttons_layout.addWidget(self.delete_all_button)

        self.layout.addLayout(add_buttons_layout) # Dodajemy układ przycisków do głównego układu
        self.layout.addLayout(delete_buttons_layout) # Dodajemy układ przycisków do głównego układu
        
        self.list_of_notes = QListWidget(self)
        self.layout.addWidget(self.list_of_notes)

        self.central_widget.setLayout(self.layout)
        file_path = os.path.join(os.path.dirname(__file__), "notes.txt") # Tworzymy ścieżkę do pliku z notatkami
        self.file_path = file_path
        
        self.read_from_file()

        style_file_path = os.path.join(os.path.dirname(__file__), "styles.css") # Tworzymy ścieżkę do pliku ze stylami
        style_file = QFile(style_file_path)
        style_file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = style_file.readAll().data().decode("utf-8")
        self.setStyleSheet(stylesheet)

    def add_note(self):
        new_note, is_clicked = QInputDialog.getText(self, 'Note Input', 'Enter your note:')
        if new_note and is_clicked:
            current_time = datetime.now().strftime("%d.%m.%Y")

            note_item = QListWidgetItem()  # Tworzymy nowy element listy
            note_widget = QWidget()  # Tworzymy widget dla elementu listy
            layout = QHBoxLayout()  # Tworzymy układ poziomy
            

            text_label = QLabel(new_note)  # Tworzymy etykietę z tekstem notatki
            text_label.setObjectName("text")
            layout.addWidget(text_label)  # Dodajemy etykietę do układu

            date_label = QLabel(current_time)  # Tworzymy etykietę  z datą
            date_label.setObjectName("date")
            layout.addWidget(date_label)  # Dodajemy etykietę do układu

            date_label.setAlignment(Qt.AlignRight)  # Wyrównujemy etykietę do prawej

            note_widget.setLayout(layout)  # Ustawiamy układ widgetu
            note_item.setSizeHint(note_widget.sizeHint())  # Ustawiamy wysokość elementu listy na podstawie widgetu (wysokość widgetu) 
            self.list_of_notes.addItem(note_item)  # Dodajemy element do listy
            self.list_of_notes.setItemWidget(note_item, note_widget)  # Przypisujemy widget do elementu

            note_with_date = f"{new_note}---{current_time}\n"
            self.save_to_file(note_with_date, important=False)

    def add_important_note(self):
        new_note, is_clicked = QInputDialog.getText(self, 'Note Input', 'Enter your note:')
        if new_note and is_clicked:
            current_time = datetime.now().strftime("%d.%m.%Y")

            note_item = QListWidgetItem()  # Tworzymy nowy element listy
            note_widget = QWidget()  # Tworzymy widget dla elementu listy
            layout = QHBoxLayout()  # Tworzymy układ poziomy
            

            text_label = QLabel(f"IMPORTANT --> {new_note}")  # Tworzymy etykietę z tekstem notatki
            text_label.setObjectName("text")
            layout.addWidget(text_label)  # Dodajemy etykietę do układu

            date_label = QLabel(current_time)  # Tworzymy etykietę  z datą
            date_label.setObjectName("date")
            layout.addWidget(date_label)  # Dodajemy etykietę do układu

            date_label.setAlignment(Qt.AlignRight)  # Wyrównujemy etykietę do prawej

            note_widget.setLayout(layout)  # Ustawiamy układ widgetu
            note_item.setSizeHint(note_widget.sizeHint())  # Ustawiamy wysokość elementu listy na podstawie widgetu (wysokość widgetu 
            self.list_of_notes.insertItem(0, note_item) # Dodajemy element do listy
            self.list_of_notes.setItemWidget(note_item, note_widget)  # Przypisujemy widget do elementu

            note_with_date = f"IMPORTANT --> {new_note}---{current_time}\n" 
            self.save_to_file(note_with_date, important=True)
            note_widget.setProperty("class", "important_note_widget")

    def save_to_file(self, element, important=False):
        with open(self.file_path, "r+") as file:
            old_content = file.read()
            if important:
                new_content = element + old_content
            else:
                new_content = old_content + element
            file.seek(0)
            file.write(new_content)
            file.truncate()

    def read_from_file(self):
        try:
            with open(self.file_path, "r") as file:
                for line in file:

                    element = line.split("---")
                    text = element[0]
                    date = element[-1]

                    note_item = QListWidgetItem()  # Tworzymy nowy element listy
                    note_widget = QWidget()  # Tworzymy widget dla elementu listy
                    layout = QHBoxLayout()  # Tworzymy układ poziomy
                    

                    text_label = QLabel(text)  # Tworzymy etykietę z tekstem notatki
                    text_label.setObjectName("text")
                    layout.addWidget(text_label)  # Dodajemy etykietę do układu

                    date_label = QLabel(date)  # Tworzymy etykietę  z datą
                    date_label.setObjectName("date")
                    layout.addWidget(date_label)  # Dodajemy etykietę do układu

                    date_label.setAlignment(Qt.AlignRight)  # Wyrównujemy etykietę do prawej

                    note_widget.setLayout(layout)  # Ustawiamy układ widgetu
                    note_item.setSizeHint(note_widget.sizeHint())  # Ustawiamy wysokość elementu listy na podstawie widgetu (wysokość widgetu) 
                    self.list_of_notes.addItem(note_item)  # Dodajemy element do listy
                    self.list_of_notes.setItemWidget(note_item, note_widget)  # Przypisujemy widget do elementu

        except FileNotFoundError:
            pass

    def delete_notes(self):
        delete_confirmation = QMessageBox.question(
        self,
        'Delete note',
        'Are you sure you want to delete this note?'
        )
        if delete_confirmation == QMessageBox.Yes:
            selected_items = self.list_of_notes.selectedItems()    

            for item in selected_items:
                note_widget = self.list_of_notes.itemWidget(item)
                text_label = note_widget.findChild(QLabel, "text")
                date_label = note_widget.findChild(QLabel, "date")
                
                if text_label and date_label:
                    note_text = text_label.text() 
                    note_date = date_label.text()
                    
                    note_with_date = f"{note_text}---{note_date}\n"
                    self.list_of_notes.takeItem(self.list_of_notes.row(item))  # Usuwamy element z listy
                    self.delete_from_file(note_with_date)

    def delete_from_file(self, element):
        with open(self.file_path, "r+") as file:
            lines = file.readlines() 
            file.seek(0) # Ustawiamy kursor na początku pliku
            for line in lines:
                if line.strip() != element.strip(): # Jeśli linia nie jest taka sama jak element, to ją zapisujemy
                    file.write(line)
            file.truncate() # Usuwamy wszystkie linie po ostatniej zapisanej

    def delete_all_notes_from_file(self):
        delete_confirmation = QMessageBox.question(
            self,
            'Delete all notes',
            'Are you sure you want to delete all notes?',
        )
        if delete_confirmation == QMessageBox.Yes:
            self.list_of_notes.clear()
            with open(self.file_path, "w") as file:
                file.write("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())