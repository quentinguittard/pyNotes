from PySide2 import QtWidgets, QtGui

from package.api.note import Note, get_notes


class MainWindow(QtWidgets.QWidget):
    """This is a class to create the window of the application."""

    def __init__(self, ctx):
        """The constructor of the window.

        :param ctx: The context of the application.
        :type ctx: ApplicationContext
        """
        super().__init__()
        self.ctx = ctx
        self.setWindowTitle("PyNotes")
        self.setup_ui()
        self.populate_notes()

    def setup_ui(self):
        """Setup the user interface of the application."""
        self.create_widgets()
        self.create_layouts()
        self.modify_widgets()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        """Create the widgets of the application."""
        self.btn_createNote = QtWidgets.QPushButton("Create a note")
        self.lw_notes = QtWidgets.QListWidget()
        self.te_content = QtWidgets.QTextEdit()

    def modify_widgets(self):
        """Apply a CSS style sheet to the user interface of the application."""
        css_file = self.ctx.get_resource("style.css")
        with open(css_file, "r") as f:
            self.setStyleSheet(f.read())

    def create_layouts(self):
        """Create the grid layout of the user interface."""
        self.main_layout = QtWidgets.QGridLayout(self)

    def add_widgets_to_layouts(self):
        """Add created widgets to the user interface layout."""
        self.main_layout.addWidget(self.btn_createNote, 0, 0, 1, 1)
        self.main_layout.addWidget(self.lw_notes, 1, 0, 1, 1)
        self.main_layout.addWidget(self.te_content, 0, 1, 2, 1)

    def setup_connections(self):
        """Setup the connections between the widgets and their functions."""
        self.btn_createNote.clicked.connect(self.create_note)
        self.te_content.textChanged.connect(self.save_note)
        self.lw_notes.itemSelectionChanged.connect(self.populate_note_content)
        QtWidgets.QShortcut(QtGui.QKeySequence("Backspace"), self.lw_notes, self.delete_selected_note)

    # END UI

    def add_note_to_listwidget(self, note):
        """Add a note to the list.

        :param note: A note object.
        :type note: Note
        """
        lw_item = QtWidgets.QListWidgetItem(note.title)
        lw_item.note = note
        self.lw_notes.addItem(lw_item)

    def create_note(self):
        """Create a note."""
        title, result = QtWidgets.QInputDialog.getText(self, "Add a note", "Title: ")
        if result and title:
            note = Note(title=title)
            note.save()
            self.add_note_to_listwidget(note)

    def delete_selected_note(self):
        """Delete a selected note from the note list."""
        selected_item = self.get_selected_lw_item()
        if selected_item:
            result = selected_item.note.delete()
            if result:
                self.lw_notes.takeItem(self.lw_notes.row(selected_item))

    def get_selected_lw_item(self):
        """Get the first selected note.

        :return: The first item of the selection or None if there is no selection.
        :rtype: QListWidgetItem or None
        """
        selected_items = self.lw_notes.selectedItems()
        if selected_items:
            return selected_items[0]
        return None

    def populate_notes(self):
        """Populate the note list with the notes found in the notes directory."""
        notes = get_notes()
        for note in notes:
            self.add_note_to_listwidget(note)

    def populate_note_content(self):
        """Populate note content in the user interface from a selected note."""
        selected_item = self.get_selected_lw_item()
        if selected_item:
            self.te_content.setText(selected_item.note.content)
        else:
            self.te_content.clear()

    def save_note(self):
        """Save the content of the selected note."""
        selected_item = self.get_selected_lw_item()
        if selected_item:
            selected_item.note.content = self.te_content.toPlainText()
            selected_item.note.save()
