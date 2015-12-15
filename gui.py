import tkinter as tk
from tkinter import filedialog
from tkinter import font
from tkinter import messagebox as mbox
from csv import Error as csvError
from table_handling import load_table, roll_against, TableFormatError


class TableRollerGUI:
    '''Implements a GUI for the table rolling utility.'''

    def __init__(self, master):
        # Initialise frame.
        frame = tk.Frame(master)
        frame.pack(fill=tk.BOTH)

        # Add label for file chooser.
        self.chooser_label = tk.Label(frame, text="Current file:")
        self.chooser_label.grid(row=0, sticky=tk.W)

        # Add label for event description with default text.
        self.desc_font = font.Font(family="Times", size=15,
                                   weight=font.BOLD, slant=font.ITALIC)
        self.event_desc = tk.Label(frame, text=("Roll against a table to see "
                                                "an event description."),
                                   font=self.desc_font, wraplength=300)
        self.event_desc.grid(row=1, columnspan=3, pady=5)

        # Add button to roll against the table.
        self.roll_btn = tk.Button(frame, text="Roll", command=self.roll)
        self.roll_btn.grid(row=2, column=0, columnspan=3)

        # Initialise dict of loaded tables and initialise the current table to
        # be Non i.e. there is no current table on first starting.
        self.tables = {}
        self.current_table = None

        # Add a button that allows the user to open a file dialog and load new
        # tables.
        self.load_btn = tk.Button(frame, text="Load tables...",
                                  command=self.load_new_tables)
        self.load_btn.grid(row=0, column=2)

        # Add table chooser menu.
        # Define StringVar to point to the name of the currently selected table
        # This differs from self.current_table, which points to the actual
        # table dict.
        self.chosen_table = tk.StringVar(frame)
        self.chosen_table.set("Please select a table...")
        self.table_menu = tk.OptionMenu(frame, self.chosen_table,
                                        "Please select a table...",
                                        *self.tables.keys())
        self.table_menu.grid(row=0, column=1)
        # Update self.current_table when a new table is selected
        self.chosen_table.trace("w", self.update_current_table)

        # Configure grid rows to fill the window.
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)

    def load_new_tables(self):
        '''Opens a file chooser dialog so that the user can choose table files
           to load. Loads these into dicts.'''

        file_opts = {"defaultextension": ".csv",
                     "title": "Choose table file(s)",
                     }
        filenames = filedialog.askopenfilenames(**file_opts)
        for f in filenames:
            table_name = f[f.rfind('/')+1:f.rfind('.csv')]
            try:
                self.tables[table_name] = load_table(f)
            except TableFormatError as err:
                mbox.showwarning("Open file",
                                 "Bad formatting: {}".format(err.err_msg))
                return
            except csvError:
                mbox.showwarning("Open file",
                                 "Cannot open file: Bad CSV input.")
                return
            except FileNotFoundError:
                mbox.showwarning("Open file",
                                 "Cannot open file: File not found.")
                return
            # Update the options in self.table_menu.
            new_comm = tk._setit(self.chosen_table, table_name)
            self.table_menu['menu'].add_command(label=table_name,
                                                command=new_comm)

    def roll(self):
        '''Rolls against the currently selected table and displays the result
           in the GUI.'''

        if self.current_table:
            self.event_desc['text'] = roll_against(self.current_table)

    def update_current_table(self, *args):
        '''Updates the value of self.current_table to the table specified by
           self.chosen_table.'''
        self.current_table = self.tables[self.chosen_table.get()]


if __name__ == "__main__":
    root = tk.Tk()
    root.title("D&D Random Table Roller")
    app = TableRollerGUI(root)
    root.mainloop()
