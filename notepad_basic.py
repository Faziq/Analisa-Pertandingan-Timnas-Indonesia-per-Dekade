import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

class Notepad:
    def __init__(self, master):
        self.master = master
        self.master.title("Untitled - Notepad")
        self.master.geometry("800x600")
        
        # Setup Text Area
        self.text_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, undo=True)
        self.text_area.pack(expand=True, fill='both')
        
        # Setup Menu
        self.menu_bar = tk.Menu(self.master)
        self.setup_menu()
        
        # File Handling
        self.current_file = None

    def setup_menu(self):
        # File Menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)
        
        # Edit Menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut_text)
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy_text)
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=self.undo_action)
        edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=self.redo_action)
        
        # Help Menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        self.master.config(menu=self.menu_bar)
        
        # Keyboard Shortcuts
        self.text_area.bind('<Control-n>', lambda event: self.new_file())
        self.text_area.bind('<Control-o>', lambda event: self.open_file())
        self.text_area.bind('<Control-s>', lambda event: self.save_file())
        self.text_area.bind('<Control-z>', lambda event: self.undo_action())
        self.text_area.bind('<Control-y>', lambda event: self.redo_action())

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.master.title("Untitled - Notepad")

    def open_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r") as file:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, file.read())
                self.current_file = file_path
                self.master.title(f"{file_path} - Notepad")
            except Exception as e:
                messagebox.showerror("Error", f"Cannot open file: {str(e)}")

    def save_file(self):
        if self.current_file:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(self.current_file, "w") as file:
                    file.write(content)
            except Exception as e:
                messagebox.showerror("Error", f"Cannot save file: {str(e)}")
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(file_path, "w") as file:
                    file.write(content)
                self.current_file = file_path
                self.master.title(f"{file_path} - Notepad")
            except Exception as e:
                messagebox.showerror("Error", f"Cannot save file: {str(e)}")

    def exit_app(self):
        self.master.destroy()

    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")

    def undo_action(self):
        self.text_area.edit_undo()

    def redo_action(self):
        self.text_area.edit_redo()

    def show_about(self):
        messagebox.showinfo("About", "Simple Notepad\nCreated using Python Tkinter\n\nVersion 1.0")

if __name__ == "__main__":
    root = tk.Tk()
    notepad = Notepad(root)
    root.mainloop()
