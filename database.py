import sqlite3
from werkzeug.security import generate_password_hash


db_name = "zzz.db"

def get_connection():
    return sqlite3.connect(db_name)

def init_db():
    Con = get_connection()
    Cur = Con.cursor()

    Cur.execute("""CREATE TABLE IF NOT EXISTS User(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )""")

    Cur.execute("""CREATE TABLE IF NOT EXISTS Roles(
        id INTEGER PRIMARY KEY,
        RoleName TEXT NOT NULL UNIQUE
    )""")

    Cur.execute("""CREATE TABLE IF NOT EXISTS UserRoles(
        userId INTEGER,
        roleId INTEGER,
        UNIQUE (userId, roleId),
        FOREIGN KEY (userId) REFERENCES User (id),
        FOREIGN KEY (roleId) REFERENCES Roles (id)
    )""")
    
    Cur.execute("INSERT OR IGNORE INTO Roles (RoleName) VALUES ('admin')")
    Cur.execute("INSERT OR IGNORE INTO Roles (RoleName) VALUES ('member')")
    Con.commit()
    Con.close()


def AddNewUser(Username, Password):
    Con = get_connection()
    Cur = Con.cursor()
    hashed = generate_password_hash(Password)
    try:
        Cur.execute("""INSERT INTO User(username, password) VALUES(?, ?)""", (Username, hashed)) 
        Con.commit()
        return 0   
    except sqlite3.IntegrityError:
        return 1
    finally:
        Con.close()

def FetchUsers(Username):
    Con = get_connection()
    Cur = Con.cursor()
    Cur.execute("SELECT * FROM User WHERE username = ?", (Username,))
    User = Cur.fetchone()
    if User:
        roles = FetchUserRoles(Username)
        Con.close()
        return (User[0], User[1], User[2], roles)
    Con.close()
    return None

def FetchUserRoles(Username):                                          # defining a user's name in their role
    Con = get_connection()
    Cur = Con.cursor()
    print(f"Find roles for users: {Username}")
    Cur.execute("""
        SELECT Roles.RoleName
        FROM User
        JOIN UserRoles ON User.id = UserRoles.userId
        JOIN Roles ON Roles.id = UserRoles.roleId
        WHERE User.username = ?
    """, (Username,))
    rows = Cur.fetchall()
    print(f"Find roles: {len(rows)}")
    print(f"Roles: {rows}")
    Con.close()
    return [row[0] for row in rows]


def AssignRole(UserName, RoleName):
    Con = get_connection()
    Cur = Con.cursor()

    #  userid
    Cur.execute("SELECT id FROM User WHERE username = ?", (UserName,))
    UserResult = Cur.fetchone()
    
    # roleid
    Cur.execute("SELECT id FROM Roles WHERE RoleName = ?", (RoleName,))
    RoleResult = Cur.fetchone()

    if UserResult and RoleResult:
        UserId = UserResult[0]
        RoleId = RoleResult[0]
        try:
            # duplicate check
            Cur.execute("INSERT OR IGNORE INTO UserRoles(userId, roleId) VALUES(?,?)", (UserId, RoleId))
            Con.commit()
        except sqlite3.Error as Error:
            print(f"Error: {Error}")
    
    Con.close()

AddNewUser("admin", "admin")
AssignRole("admin", "admin")
# fetchUsers("asf")

# con.close()
