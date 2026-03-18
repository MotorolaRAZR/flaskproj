import flask
import database
import os
import secrets
from werkzeug.security import check_password_hash

app = flask.Flask("__main__")
app.secret_key = secrets.token_hex(16)


@app.route("/", methods=["POST", "GET"])
def main():
    returnvalue = ""
    logged = flask.session.get("username")
    roles = database.FetchUserRoles(logged)

    if flask.request.method == "POST":
        if "username" in flask.request.form:
            inputfromUser = flask.request.form["username"]
            returnvalue = database.FetchUsers(inputfromUser)
        else:
            returnvalue = ""

        if (
            "makeUser" in flask.request.form
            and "makepassword" in flask.request.form
            and "role" in flask.request.form
        ):
            name2Create = flask.request.form["makeUser"]
            pass2Create = flask.request.form["makepassword"]
            role = flask.request.form["role"]
            database.AddNewUser(name2Create, pass2Create)
            database.AssignRole(name2Create, role)

        return flask.render_template(
            "main.html", loggedIn=logged, returnedName=returnvalue, roles=roles
        )

    # another return if other one fails when we create user
    return flask.render_template(
        "main.html", loggedIn=logged, roles=roles, returnedName=returnvalue
    )


@app.route("/login", methods=["POST", "GET"])
def login():
    sesh = flask.session
    if flask.request.method == "POST":
        if "username" in flask.request.form and "password" in flask.request.form:
            username = flask.request.form["username"]
            password = flask.request.form["password"]
            answer = database.FetchUsers(username)
            print(answer)
            if answer != None:
                if answer[1] == username and check_password_hash(answer[2], password):
                    flask.session["username"] = username  # put username into username
                    flask.session["roles"] = database.FetchUserRoles(
                        username
                    )  # put roles into the session
                    return flask.redirect(flask.url_for("main"))
        else:
            pass
        if "logout" in flask.request.form:
            print("aaaaa")
            return flask.redirect("/logout")
    print(flask.session)
    return flask.render_template("login.html", session=sesh)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if flask.request.method == "GET":
        flask.session.clear()
    return flask.redirect(flask.url_for("main"))


# TODo MAYBE ADD WEBSOCKET CHATROOM

app.run(debug=True)
