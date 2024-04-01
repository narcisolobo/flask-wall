from datetime import datetime
from flask import flash
from flask_app.models import user
from flask_app.config.mysql_connection import connectToMySQL


class Note:
    _db = "private-wall"

    def __init__(self, data: dict[str, str | datetime], sender=None) -> None:
        self.id: str = data["id"]
        self.sender_id: str = data["sender_id"]
        self.recipient_id: str = data["recipient_id"]
        self.body: str = data["body"]
        self.created_at: datetime = data["created_at"]
        self.updated_at: datetime = data["updated_at"]
        self.sender: sender

    @staticmethod
    def note_is_valid(form_data: dict[str, str]) -> bool:
        is_valid = True
        if len(form_data["body"].strip()) < 5:
            flash(
                "Note must be at least five characters.",
                form_data['recipient_name']
            )
            is_valid = False
        return is_valid

    @classmethod
    def create_note(cls, form_data: dict[str, str]) -> int:
        query = "INSERT INTO notes (sender_id, recipient_id, body) VALUES (%(sender_id)s, %(recipient_id)s, %(body)s);"
        return connectToMySQL(Note._db).query_db(query, form_data)

    @classmethod
    def find_notes_by_recipient_with_sender(cls, recipient_id: int):
        query = "SELECT * FROM notes JOIN users ON notes.sender_id = users.id WHERE recipient_id = %(recipient_id)s;"
        data = {
            "recipient_id": recipient_id
        }
        results = connectToMySQL(Note._db).query_db(query, data)
        notes = []
        if len(results) > 0:
            for result in results:
                note = Note(result)
                sender = user.User.find_user_by_id(result['sender_id'])
                note.sender = sender
                notes.append(note)
        return notes

    @classmethod
    def delete_one_note(cls, note_id: int):
        query = "DELETE FROM notes WHERE id = %(note_id)s;"
        data = {
            "note_id": note_id
        }
        return connectToMySQL(Note._db).query_db(query, data)

    @classmethod
    def get_note_count(cls, sender_id: int):
        query = "SELECT COUNT(*) AS sent_notes_count FROM notes WHERE sender_id = %(sender_id)s;"
        data = {
            "sender_id": sender_id
        }
        results = connectToMySQL(Note._db).query_db(query, data)
        return results[0]["sent_notes_count"]
