import sqlite3
import uuid

def clear_today_table():
    con = sqlite3.connect('exercise.db')
    cursor = con.cursor()
    cursor.execute("DELETE FROM today")
    con.commit()
    con.close()

def generate_random_tokens():
    con = sqlite3.connect('exercise.db')
    cursor = con.cursor() 
    cursor.execute('SELECT name FROM users') 
    rows = cursor.fetchall()
    for row in rows:
        token_data = (row[0], str(uuid.uuid4()))
        cursor.execute('INSERT INTO today (name, token) VALUES (?, ?)', token_data)
        con.commit()
    con.close()


if __name__ == '__main__':
    clear_today_table()
    generate_random_tokens()