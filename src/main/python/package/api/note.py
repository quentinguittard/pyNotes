import os
import json
from uuid import uuid4
from glob import glob

from package.api.constants import NOTES_DIR


def get_notes():
    """Create a list of Notes objects from all notes contained in notes directory.

    :return: The list of the notes objects saved in notes directory.
    :rtype: list
    """
    notes = []
    note_files = glob(os.path.join(NOTES_DIR, "*.json"))
    for note_file in note_files:
        with open(note_file, "r") as f:
            note_data = json.load(f)
            note_uuid = os.path.splitext(os.path.basename(note_file))[0]
            note_title = note_data.get("title")
            note_content = note_data.get("content")
            note = Note(uuid=note_uuid, title=note_title, content=note_content)
            notes.append(note)

    return notes


class Note:
    """The Note class implements the note mechanics.

    Attributes:
        content (str): The note content.
        path (str): The note file path.
        title (str): The name of the note.
        uuid (str): The note universal unique identifier.
    """

    def __init__(self, title="", content="", uuid=None):
        """Create a new Note.

        :param title: The name of the note.
        :param content: The note content.
        :param uuid: The note universal unique identifier.
        :type title: str
        :type content: str
        :type uuid: str
        """
        self.uuid = uuid or str(uuid4())
        self.title = title
        self.content = content

    def __repr__(self):
        return f"{self.title} ({self.uuid})"

    def __str__(self):
        return self.title

    @property
    def content(self):
        """The property to get the content of the note.

        :return: The content of the note.
        :rtype: str
        """
        return self._content

    @property
    def path(self):
        """The property to get the path of the note.

        :return: The path of the note.
        :rtype: str
        """
        return os.path.join(NOTES_DIR, self.uuid + ".json")

    @content.setter
    def content(self, value):
        """The property to set the content of the note.

        :param value: The new content of the note.
        :type value: str

        :raise TypeError: The value parameter is not a string.
        """
        if isinstance(value, str):
            self._content = value
        else:
            raise TypeError("Invalid value (string expected)")

    def delete(self):
        """The function to delete the note.

        :return: False if the path of the note does not exists or True if the note is deleted.
        :rtype: bool
        """
        os.remove(self.path)
        if os.path.exists(self.path):
            return False
        return True

    def save(self):
        """The function to save the note."""
        if not os.path.exists(NOTES_DIR):
            os.makedirs(NOTES_DIR)

        data = {"title": self.title, "content": self.content}
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)
