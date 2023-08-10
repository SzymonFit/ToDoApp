from PyQt5.QtWidgets import QApplication, QInputDialog
import sys
from app import App

class CustomInputDialog(QInputDialog):
    def __init__(self, parent=App):
        super().__init__(parent)
        
        self.setInputMode(QInputDialog.TextInput)
        self.setWindowTitle('Custom Input Dialog')
        self.setLabelText('Enter your text:')
        self.setTextValue('Initial text')  # Domyślna treść pola tekstowego
        self.resize(400, 200)  # Ustawienie rozmiaru pop-upa

def main():
    app = QApplication(sys.argv)

    custom_input_dialog = CustomInputDialog()

    text, ok = custom_input_dialog.getText()

    if ok:
        print('Text entered:', text)
    else:
        print('Cancelled')

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()