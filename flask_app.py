import flask
import database

app = flask.Flask('__main__')

@app.route("/", methods=['POST', "GET"])
def main():
    if flask.request.method == "POST":
        if 'username' in flask.request.form:
            inputfromUser = flask.request.form['username']
            returnvalue = database.fetchUsers(inputfromUser)
        else:
            returnvalue = ""

        if "makeUser" in flask.request.form and "makepassword" in flask.request.form:
            name2Create = flask.request.form['makeUser']
            pass2Create = flask.request.form['makepassword']
            creation = database.addNewUser(name2Create, pass2Create)
        return flask.render_template("main.html", returnedName=returnvalue)
    return flask.render_template("main.html")

app.run(debug=True)