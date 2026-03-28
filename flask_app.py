import flask
import database
import os
import secrets
from werkzeug.security import check_password_hash

app = flask.Flask("__name__")
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


@app.route("/chatroom", methods=["POST", "GET"])
def chatroom():
    username = flask.session.get("username")
    if not username:
        return flask.redirect(flask.url_for("login"))

    if flask.request.method == "POST":
        message = flask.request.form["message"]
        database.WriteMessage(username, message)

    messages = database.FetchMessages()
    return flask.render_template("chatroom.html", logged=username, messages=messages)

    # TODO: Apache With Conduit Matrix Server


@app.route("/news", methods=["POST", "GET"])
def displaynews():
    username = flask.session.get("username")  # Получаем из сессии
    if not username:  # Защита
        return flask.redirect(flask.url_for("login"))
    news = database.FetchNews()
    roles = database.FetchUserRoles(username)
    if flask.request.method == "POST":
        title = flask.request.form.get("title")
        content = flask.request.form.get("content")
        if title and content:
            database.WriteNews(title, username, content)
            flask.flash("Новость опубликована!")
            news = database.FetchNews()
    
    return flask.render_template("news_page.html", logged=username, news=news, roles=roles)

@app.context_processor
def inject_user_info():
    return {
        'logged': flask.session.get('username'),
        'roles': flask.session.get('roles', [])
    }
@app.before_request
def log_session():
    print(f"REQUEST {flask.request.path}: session.username={flask.session.get('username')}")

app.run(debug=True)


# TODO: HTML REFRACTOR + CSS DESIGN(ITS IN THE TELE GROUP)
