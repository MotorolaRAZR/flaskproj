


import sqlite3


# con = sqlite3.connect("test.db")


# cur = con.cursor()



# cur.execute("""CREATE TABLE IF NOT EXISTS User(
#     id INTEGER PRIMARY KEY,
#     username TEXT NOT NUll,
#     password TEXT NOT NUll
# )""")
# con.commit()


def addNewUser(username, password):
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    cur.execute("""INSERT INTO User(username, password) VALUES(?, ?)""", (username, password)) 
    con.commit()

def fetchUsers(username):
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    users = cur.execute("SELECT * FROM User").fetchall()
    con.commit()
    for i in users:
        if i[1] == username:
            return i 
#addNewUser("asf", "asf")
# fetchUsers("asf")

# con.close()
