import sqlite3

import email_address_list


def create_user_table():
    con = sqlite3.connect('exercise.db')
    cursor = con.cursor()
    cursor.execute("CREATE TABLE users(name text PRIMARY KEY, email text)")
    con.commit()
    con.close()

def populate_users():
    con = sqlite3.connect('exercise.db')
    cursor = con.cursor()
    for member in email_address_list.members:
        details = (member, email_address_list.members[member])
        cursor.execute('INSERT INTO users (name, email) VALUES(?, ?)', details)
    con.commit()
    con.close()

def create_today_table():
    con = sqlite3.connect('exercise.db')
    cursor = con.cursor()
    cursor.execute("CREATE TABLE today(name text PRIMARY KEY, token text, response text)")
    con.commit()
    con.close()

def setup_db():
    create_user_table()
    populate_users()
    create_today_table()


if __name__ == '__main__':
    setup_db()