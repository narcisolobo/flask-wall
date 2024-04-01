from flask_app import app
from flask_app.models.user import User
from flask_app.models.note import Note
from flask import flash, redirect, render_template, request, session, url_for


@app.get('/wall')
def wall():
    if 'user_id' not in session:
        flash("Please log in.", "auth")
        return redirect(url_for('login_form'))

    recipients = User.find_all_users_except_logged_in_user(session['user_id'])
    notes = Note.find_notes_by_recipient_with_sender(session['user_id'])
    user = User.find_user_by_id(session['user_id'])
    count = Note.get_note_count(session['user_id'])
    return render_template('wall.html', user=user, notes=notes, count=count, recipients=recipients)


@app.post('/notes/create')
def send_note():
    if not Note.note_is_valid(request.form):
        return redirect(url_for('wall'))

    Note.create_note(request.form)
    return redirect(url_for('wall'))
