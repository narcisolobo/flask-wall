from flask_app import app
import flask_app.controllers.users
import flask_app.controllers.notes


if __name__ == '__main__':
    app.run(host="localhost", port=5001, debug=True)
