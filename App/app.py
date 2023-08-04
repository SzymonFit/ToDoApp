import tkinter as tk
from datetime import datetime

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("App")
        self.geometry('1000x1000')
        
        self.add = tk.Entry(self, width=300)
        self.add.pack()

        self.add_button = tk.Button(self, text="Add note", command = self.add_note)
        self.add_button.pack()

        self.delete_button = tk.Button(self, text="Delete", command=self.delete_notes)
        self.delete_button.pack()


        self.list_of_notes = tk.Listbox(self)
        self.list_of_notes.pack(fill=tk.BOTH, expand=True)

        self.read_from_file()
        
        self.protocol("WM_DELETE_WINDOW", self.close_app)

    def add_note(self):
        new_note = self.add.get()
        if new_note:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            note_with_date = f"{current_time} - {new_note}"
            self.list_of_notes.insert(tk.END, note_with_date)
            self.save_to_file(note_with_date)
            self.add.delete(0, tk.END)


    def save_to_file(self, element):
        with open("notes.txt", "w") as file:
            file.write(element + "\n")
    
    def read_from_file(self):
        try:
            with open("notes.txt", "r") as file:
                for line in file:
                    element = line.strip()
                    self.list_of_notes.insert(tk.END, element)
        except FileNotFoundError:
            pass
        
    def delete_notes(self):
        index = self.list_of_notes.curselection()
        if index:
            index = int(index[0])
            element = self.list_of_notes.get(index)
            self.list_of_notes.delete(index)
            self.delete_from_file(element)

    def delete_from_file(self, element):

        with open("notes.txt", "w") as file:
            lines = file.readlines()
            for line in lines:
                if line.strip() != element:
                    file.write(line)

    def close_app(self):
        self.save_to_file("")
        self.destroy()

runApp = App()
runApp.mainloop()