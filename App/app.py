import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QListWidget, QVBoxLayout, QWidget
from PyQt5.QtCore import QFile
from datetime import datetime

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App")
        self.setGeometry(100, 100, 1000, 1000)
        
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.add = QLineEdit(self)
        self.add.setFixedWidth(300)
        self.layout.addWidget(self.add)

        self.add_button = QPushButton("Add note", self)
        self.add_button.setObjectName("add_button")
        self.add_button.clicked.connect(self.add_note)
        self.add_button.setProperty("class", "add_button")
        self.layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Delete", self)
        self.delete_button.setObjectName("delete_button")
        self.delete_button.clicked.connect(self.delete_notes)
        self.delete_button.setProperty("class", "delete_button")    
        self.layout.addWidget(self.delete_button)

        self.list_of_notes = QListWidget(self)
        self.layout.addWidget(self.list_of_notes)

        self.central_widget.setLayout(self.layout)

        self.read_from_file()

        style_file = QFile("styles.css")
        style_file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = style_file.readAll().data().decode("utf-8")
        self.setStyleSheet(stylesheet)

    def add_note(self):
        new_note = self.add.text()
        if new_note:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            note_with_date = f"{new_note} - {current_time}"
            self.list_of_notes.addItem(note_with_date)  # Dodajemy notatkę jako nowy element do listy
            self.save_to_file(note_with_date + "\n")  # Zapisujemy notatkę z nową linią

    def save_to_file(self, element):
        with open("notes.txt", "a") as file:
            file.write(element)
    
    def read_from_file(self):
        try:
            with open("notes.txt", "r") as file:
                for line in file:
                    element = line.strip()
                    self.list_of_notes.addItem(element)
        except FileNotFoundError:
            pass
        
    def delete_notes(self):
        selected_items = self.list_of_notes.selectedItems()
        for item in selected_items:
            self.list_of_notes.takeItem(self.list_of_notes.row(item))
            self.delete_from_file(item.text() + "\n")

    def delete_from_file(self, element):
        with open("notes.txt", "r+") as file:
            lines = file.readlines() 
            file.seek(0) # Ustawiamy kursor na początku pliku
            for line in lines:
                if line.strip() != element.strip(): # Jeśli linia nie jest taka sama jak element, to ją zapisujemy
                    file.write(line)
            file.truncate() # Usuwamy wszystkie linie po ostatniej zapisanej

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())