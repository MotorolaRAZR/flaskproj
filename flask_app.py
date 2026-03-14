import flask
import database
import os
import secrets
from werkzeug.security import generate_password_hash, check_password_hash

app = flask.Flask('__main__')
app.secret_key = secrets.token_hex(16)

@app.route("/", methods=['POST', "GET"])
def main():
    returnvalue = ""
    logged = None

    if flask.request.method == "POST":
        if 'username' in flask.request.form:
            inputfromUser = flask.request.form['username']
            returnvalue = database.fetchUsers(inputfromUser)
        else:
            returnvalue = ""

        if "makeUser" in flask.request.form and "makepassword" in flask.request.form:
            name2Create = flask.request.form['makeUser']
            pass2Create = flask.request.form['makepassword']
            hashed = generate_password_hash(pass2Create)
            database.addNewUser(name2Create, hashed)

        return flask.render_template("main.html", returnedName=returnvalue) # if creation succeeds

    return flask.render_template("main.html", loggedIn=flask.session.get('username') )

@app.route("/login", methods=["POST", "GET"])
def login():
    if flask.request.method == "POST":
        username = flask.request.form['username']
        password = flask.request.form['password']

        answer = database.fetchUsers(username)

        if answer != None:
            if answer[1] == username and check_password_hash(answer[2], password):
                flask.session['username'] = username
                return flask.redirect(flask.url_for("main"))
    print(flask.session)
    return flask.render_template("login.html", loggedIn=flask.session.get('username'))

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    if flask.request.method == "POST":
        flask.session.pop('username', None)
    return flask.redirect(flask.url_for("static", filename="main.html"))

app.run(debug=True)