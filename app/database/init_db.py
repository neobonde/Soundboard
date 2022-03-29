import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# cur.execute("INSERT INTO sounds (title, sound_uri, thumb_uri) VALUES (?, ?, ?)",
#             ('Test sound', 'default.ogg', 'default.png')
            # )

connection.commit()
connection.close()
