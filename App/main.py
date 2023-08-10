import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QListWidget, QVBoxLayout, QWidget, QLabel, QListWidgetItem, QHBoxLayout, QInputDialog
from PyQt5.QtCore import QFile, Qt
from datetime import datetime
import os

class App(QMainWindow):
    def __init__(self):
        super().__init__() 
        
        self.setWindowTitle("App")
        self.setGeometry(100, 100, 1000, 1000)

        
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
            self.save_to_file(note_with_date)

    def add_important_note():
        pass

    def save_to_file(self, element):
        with open(self.file_path, "a") as file:
            file.write(element)


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
        selected_items = self.list_of_notes.selectedItems()
        for item in selected_items:
            self.list_of_notes.takeItem(self.list_of_notes.row(item)) # Usuwamy element z listy
            self.delete_from_file(item.text() + "\n") #

    def delete_from_file(self, element):
        with open(self.file_path, "r+") as file:
            lines = file.readlines() 
            file.seek(0) # Ustawiamy kursor na początku pliku
            for line in lines:
                if line.strip() != element.strip(): # Jeśli linia nie jest taka sama jak element, to ją zapisujemy
                    file.write(line)
            file.truncate() # Usuwamy wszystkie linie po ostatniej zapisanej

    def delete_all_notes_from_file(self):
        self.list_of_notes.clear()
        with open(self.file_path, "w") as file:
            file.write("")

"""Do zrobienia:
- dodawanie ważnych notatek + sortowanie ich na poczatku
- usuwanie wszystkich notatek procz waznych
- wczytywanie z pliku notatek waznych i zwyklych tak zeby data byla do prawej tresc do lewej, split()  ~~~ done
- dodanie daty do notatki np lekarz za 4 dni  
- dodanie przypomnienia o notatce?
- usuwanie automatyczne notatek gdy data jest starsza 2 dni niz zapisano notatke
- css :)
- i moze testy jednostkowe jak sie uda :D
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())