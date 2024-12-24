import os
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import ttk

# A class to design advanced Notepad
class AdvancedNotepad:

    def __init__(self, width=800, height=600):
        self.root = Tk()

        # Set default window dimensions
        self.thisWidth = width
        self.thisHeight = height
        self.thisTextArea = Text(self.root, undo=True, wrap=WORD)
        self.thisMenuBar = Menu(self.root)
        self.thisFileMenu = Menu(self.thisMenuBar, tearoff=0)
        self.thisEditMenu = Menu(self.thisMenuBar, tearoff=0)
        self.thisHelpMenu = Menu(self.thisMenuBar, tearoff=0)

        # Line number widget
        self.line_numbers = Text(self.root, width=4, padx=3, takefocus=0, border=0,
                                  background='#f0f0f0', state='disabled')

        # Scrollbar for text area
        self.thisScrollBar = Scrollbar(self.root)
        self._file = None
        self.dark_mode = False

        # Set the window title
        self.root.title("Untitled1 - Notepad")

        # Center the window
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()
        left = (screenWidth / 2) - (self.thisWidth / 2)
        top = (screenHeight / 2) - (self.thisHeight / 2)
        self.root.geometry('%dx%d+%d+%d' % (self.thisWidth, self.thisHeight, left, top))

        # Grid configuration
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Packing widgets
        self.line_numbers.grid(row=0, column=0, sticky=N + S)
        self.thisTextArea.grid(row=0, column=1, sticky=N + E + S + W)
        self.thisScrollBar.grid(row=0, column=2, sticky=N + S)

        self.thisScrollBar.config(command=self.thisTextArea.yview)
        self.thisTextArea.config(yscrollcommand=self.thisScrollBar.set)

        # File menu
        self.thisFileMenu.add_command(label="New", command=self._newFile)
        self.thisFileMenu.add_command(label="Open", command=self._openFile)
        self.thisFileMenu.add_command(label="Save", command=self._saveFile)
        self.thisFileMenu.add_command(label="Exit", command=self._exitApplication)
        self.thisMenuBar.add_cascade(label="File", menu=self.thisFileMenu)

        # Edit menu
        self.thisEditMenu.add_command(label="Cut", command=self._cut)
        self.thisEditMenu.add_command(label="Copy", command=self._copy)
        self.thisEditMenu.add_command(label="Paste", command=self._paste)
        self.thisEditMenu.add_command(label="Undo", command=self._undo)
        self.thisEditMenu.add_command(label="Redo", command=self._redo)
        self.thisMenuBar.add_cascade(label="Edit", menu=self.thisEditMenu)

        # Help menu
        self.thisHelpMenu.add_command(label="About Notepad", command=self._showAbout)
        self.thisMenuBar.add_cascade(label="Help", menu=self.thisHelpMenu)

        # View menu for Dark Mode
        self.thisViewMenu = Menu(self.thisMenuBar, tearoff=0)
        self.thisViewMenu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode)
        self.thisMenuBar.add_cascade(label="View", menu=self.thisViewMenu)

        # Configure menu
        self.root.config(menu=self.thisMenuBar)

        # Update line numbers dynamically
        self.thisTextArea.bind("<KeyRelease>", lambda e: self.update_line_numbers())
        self.update_line_numbers()

    # To exit the application
    def _exitApplication(self):
        self.root.destroy()

    # About dialog
    def _showAbout(self):
        showinfo("Notepad", "Advanced Notepad with Python and Tkinter")

    # Open a file
    def _openFile(self):
        self._file = askopenfilename(defaultextension=".txt",
                                     filetypes=[("All Files", "*.*"),
                                                ("Text Documents", "*.txt")])
        if self._file:
            self.root.title(os.path.basename(self._file) + " - Notepad")
            self.thisTextArea.delete(1.0, END)
            with open(self._file, "r") as file:
                self.thisTextArea.insert(1.0, file.read())

    # Create a new file
    def _newFile(self):
        self.root.title("Untitled - Notepad")
        self._file = None
        self.thisTextArea.delete(1.0, END)

    # Save the file
    def _saveFile(self):
        if not self._file:
            self._file = asksaveasfilename(initialfile='Untitled.txt',
                                           defaultextension=".txt",
                                           filetypes=[("All Files", "*.*"),
                                                      ("Text Documents", "*.txt")])
            if not self._file:
                self._file = None
        if self._file:
            with open(self._file, "w") as file:
                file.write(self.thisTextArea.get(1.0, END))
            self.root.title(os.path.basename(self._file) + " - Notepad")

    # Edit functionalities
    def _cut(self):
        self.thisTextArea.event_generate("<<Cut>>")

    def _copy(self):
        self.thisTextArea.event_generate("<<Copy>>")

    def _paste(self):
        self.thisTextArea.event_generate("<<Paste>>")

    def _undo(self):
        self.thisTextArea.edit_undo()

    def _redo(self):
        self.thisTextArea.edit_redo()

    # Toggle dark mode
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        bg_color = "#2E2E2E" if self.dark_mode else "#FFFFFF"
        fg_color = "#FFFFFF" if self.dark_mode else "#000000"
        self.thisTextArea.config(bg=bg_color, fg=fg_color)
        self.line_numbers.config(bg=bg_color, fg=fg_color)

    # Update line numbers
    def update_line_numbers(self):
        self.line_numbers.config(state="normal")
        self.line_numbers.delete(1.0, END)
        lines = self.thisTextArea.index('end-1c').split('.')[0]
        line_number_string = "\n".join(str(i) for i in range(1, int(lines) + 1))
        self.line_numbers.insert(1.0, line_number_string)
        self.line_numbers.config(state="disabled")

    # Run the application
    def run(self):
        self.root.mainloop()

# Run the Advanced Notepad
notepad = AdvancedNotepad(width=800, height=600)
notepad.run()
