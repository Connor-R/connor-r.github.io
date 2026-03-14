import requests
import smtplib
import os
import csv
from email.mime.text import MIMEText

# Define the file to store the last known IP address
IP_FILE = 'ip_last.txt'

# Define your email credentials
current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
key_file = os.path.join(parent_directory, 'quotes', 'un_pw.csv')
key_list = {}
with open(key_file, 'rU') as f:
    mycsv = csv.reader(f)
    for row in mycsv:
        un, pw = row
        key_list[un]=pw
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587


def get_external_ip():
    response = requests.get('https://api.ipify.org')
    return response.text

def send_email(subject, body):
    email_address = "connor.reed.92@gmail.com"


    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = email_address

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(email_address, pw)
    server.sendmail(email_address, email_address, msg.as_string())
    server.quit()

def main():
    current_ip = get_external_ip()

    if os.path.exists(IP_FILE):
        with open(IP_FILE, 'r') as file:
            last_ip = file.read().strip()
    else:
        last_ip = ''

    if current_ip != last_ip:
        subject = 'IP Address Changed'
        body = 'Your new IP address is: {}'.format(current_ip)
        send_email(subject, body)

        with open(IP_FILE, 'w') as file:
            file.write(current_ip)

        print "\n##########################\nNEW IP ADDRESS", current_ip, "\n##########################\n"

if __name__ == '__main__':
    main()