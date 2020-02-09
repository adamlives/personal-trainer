import imaplib
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3
import uuid

import account_details

response = "yes"

def get_users_to_check():
    results = []
    con = sqlite3.connect('exercise.db')
    cursor = con.cursor() 
    cursor.execute('''SELECT users.name, users.email, today.token 
                        FROM users 
                        INNER JOIN today ON users.name = today.name 
                        WHERE today.response IS NULL''') 
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        results.append(row)
    con.close()
    return results

def update_completed_users(name):
    print(name)
    con = sqlite3.connect('exercise.db')
    cursor = con.cursor() 
    cursor.execute('''UPDATE today 
                        SET response = "TRUE" 
                        WHERE today.name = ?''', name)
    con.commit()
    con.close()

def check_received_emails(name, email_address, token):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(account_details.account, account_details.password)
    mail.list()
    mail.select("inbox")
    _, data = mail.search(None, "ALL")
    ids = data[0]
    id_list = ids.split()
    latest_email_id = id_list[-1]
    _, data = mail.fetch(latest_email_id, "(RFC822)")
    msg = email.message_from_string(data[0][1].decode('utf-8'))

    if token in msg['Subject'] and response in msg.get_payload()[0].get_payload().lower():
        print("Done for the day!")
        update_completed_users(name)
    else:
        print("Isn't it about time?")

if __name__ == '__main__':
    results = get_users_to_check()
    for result in results:
        name = (result[0],)
        email_address = result[1]
        token = result[2]
        check_received_emails(name, email_address, token)