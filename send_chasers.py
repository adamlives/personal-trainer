import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3

import account_details

response = "yes"
SUBJECT = 'Exercise checker'
text = "Have you done your exercises for the day?\n\n"
html = "Have you done your exercises for the day?<br><br>"


def get_users_to_email():
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

def send_mail(person, email_address, token):
    # Send the chasing email
    # Gmail Sign In

    gmail_SENDER = account_details.account
    gmail_PASSWD = account_details.password

    # Setup server object
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_SENDER, gmail_PASSWD)

    msg = MIMEMultipart('alternative')
    # msg['To'] = ", ".join(email_address)
    msg['To'] = email_address
    msg['From'] = "Personal Trainer<" + gmail_SENDER + ">"
    msg['Subject'] = SUBJECT
    part1 = MIMEText(text + " " + token, 'plain')
    part2 = MIMEText(html + " " + token, 'html')

    msg.attach(part1)
    msg.attach(part2)
    
    """mail_body = '\r\n'.join(['To: %s' % self.TO,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % self.SUBJECT,
                        '', self.TEXT])"""
    
    try:
        server.sendmail(gmail_SENDER, email_address, msg.as_string())
        print ('email sent')
    except:
        print ('error sending mail')
    finally:    
        server.quit()


if __name__ == '__main__':
    results = get_users_to_email()
    for result in results:
        send_mail(result[0], result[1], result[2])