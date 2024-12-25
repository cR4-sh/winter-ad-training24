import sqlite3


def sqlescape(s):
    s = str(s)
    return s.translate(
        s.maketrans({
            "\0": "\\0",
            "\r": "\\r",
            "\x08": "\\b",
            "\x09": "\\t",
            "\x1a": "\\z",
            "\n": "\\n",
            "\"": "\\\"",
            "'": "''",
            "\\": "\\\\",
            "%": "\\%"
        }))


def register_user(username, password):
    connection = sqlite3.connect('./database.sqlite')
    c = connection.cursor()
    c.execute(f"SELECT id from Users Where username='{sqlescape(username)}'")
    if len(c.fetchall()) > 0:
        return False
    c.execute(f"INSERT INTO Users (username, password) VALUES ('{sqlescape(username)}', '{sqlescape(password)}')")
    c.execute(f"SELECT id from Users ORDER BY id DESC LIMIT 1")
    id = c.fetchone()[0]
    c.execute(f"INSERT INTO Score (user_id, game_id, points) VALUES ({id}, 1, 0), ({id}, 2, 0), ({id}, 3, 0)")
    connection.commit()
    connection.close()
    return id


def login_user(username, password):
    connection = sqlite3.connect('./database.sqlite')
    c = connection.cursor()
    c.execute(f"SELECT id from Users WHERE username='{sqlescape(username)}' AND password='{sqlescape(password)}'")
    user = c.fetchall()
    if len(user) == 0:
        return False
    connection.close()
    return user[0][0]


def get_score(game_id):
    connection = sqlite3.connect('./database.sqlite')
    c = connection.cursor()
    c.execute(f"SELECT username, points from Score LEFT JOIN Users ON Score.user_id=Users.id "
              f"Where Score.game_id={game_id} AND Score.points > 0 ORDER BY Score.points DESC")
    return c.fetchall()


def get_score_by_userid(user_id):
    connection = sqlite3.connect('./database.sqlite')
    c = connection.cursor()
    c.execute(f"SELECT points from Score WHERE user_id='{int(user_id)}' ORDER BY game_id")
    fetched = c.fetchall()
    connection.close()
    return fetched[0][0], fetched[1][0], fetched[2][0]


def update_score(user_id, game_id, points):
    connection = sqlite3.connect('./database.sqlite')
    c = connection.cursor()
    c.execute(f"UPDATE Score SET points={int(points)} WHERE user_id={int(user_id)} "
              f"AND game_id = {int(game_id)}")
    connection.commit()
    connection.close()


def insert_news(title, text):
    connection = sqlite3.connect('./database.sqlite')
    c = connection.cursor()
    c.execute(f"INSERT INTO News (title, txt) VALUES('{sqlescape(title)}', '{sqlescape(text)}')")
    connection.commit()
    connection.close()


def get_news():
    connection = sqlite3.connect('./database.sqlite')
    c = connection.cursor()
    c.execute(f"SELECT title, txt, time from News ORDER BY id DESC LIMIT 30")
    return_val = c.fetchall()
    connection.close()
    return return_val


def get_user(user_id):
    connection = sqlite3.connect('./database.sqlite')
    c = connection.cursor()
    c.execute(f"SELECT username, password FROM Users WHERE id={user_id}")
    return_val = c.fetchone()
    connection.close()
    return return_val


def update_password(user_id, username, password):
    connection = sqlite3.connect('./database.sqlite')
    c = connection.cursor()
    c.execute(f"UPDATE Users SET password='{password}' WHERE id={int(user_id)} AND username='{username}'")
    connection.commit()
    connection.close()


def ban_user(user_id):
    connection = sqlite3.connect('./database.sqlite')
    c = connection.cursor()
    c.execute(f"DELETE FROM Users WHERE id={user_id}")
    c.execute(f"DELETE FROM Score WHERE user_id={int(user_id)}")
    connection.commit()
    connection.close()
