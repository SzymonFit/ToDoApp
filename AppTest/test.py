import unittest
import sys
sys.path.append('C:/Users/Szymon/Desktop/ToDoApp')
from PyQt5.QtWidgets import QApplication
from App.main import App


class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls): # Wywoływana przed wszystkimi testami
        cls.app = QApplication([])  # Inicjalizacja aplikacji przed testami

    @classmethod
    def tearDownClass(cls): # Wywoływana po wszystkich testach
        cls.app.quit()  # Zamknięcie aplikacji po testach

    def setUp(self):
        self.window = App()
        self.window.show()
        self.app.processEvents()  # Pozwala na obsługę zdarzeń w oknie

    def tearDown(self):
        self.window.close()

    def test_add_note(self):
        note_count_before = self.window.list_of_notes.count()

        self.window.add_note()

        note_count_after = self.window.list_of_notes.count()
        self.assertEqual(note_count_after, note_count_before + 1)

    def test_add_important_note(self):
        note_count_before = self.window.list_of_notes.count()

        self.window.add_important_note()

        note_count_after = self.window.list_of_notes.count()
        self.assertEqual(note_count_after, note_count_before + 1)

    def test_delete_notes(self):
        note_count_before = self.window.list_of_notes.count()

        self.window.add_note()
        self.window.add_note()

        note_to_select = self.window.list_of_notes.item(0)
        self.window.list_of_notes.setCurrentItem(note_to_select)

        self.window.delete_notes()

        note_count_after = self.window.list_of_notes.count()
        self.assertEqual(note_count_after, note_count_before + 1)

    def test_delete_all_notes_from_file(self):
        self.window.add_note()
        self.window.add_note()

        self.window.delete_all_notes_from_file()

        self.assertEqual(self.window.list_of_notes.count(), 0)

if __name__ == '__main__':
    unittest.main()