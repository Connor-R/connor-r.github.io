import sys
import os
import csv
import argparse
from datetime import timedelta,date,datetime
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


from py_db import db

db = db('personal')


key_file = os.getcwd()+"/un_pw.csv"
key_list = {}
with open(key_file, 'rU') as f:
    mycsv = csv.reader(f)
    for row in mycsv:
        un, pw = row
        key_list[un]=pw


def generate_body(author, topic, medium, keyword, count, to_address):
    sub = 'Daily Quotes [%s]' % (str(date.today()))

    quote_lookup = """SELECT 
    QuoteID, estimated_date, author, topic, medium, source, source_location, quote
    FROM quotes
    WHERE 1
    AND (author LIKE "%%%s%%" AND topic LIKE "%%%s%%" AND medium LIKE "%%%s%%" AND quote LIKE "%%%s%%")
    ORDER BY rand()
    LIMIT %s
    ;""" % (author, topic, medium, keyword, count)
    res = db.query(quote_lookup)

    mesg = ''
    for i, row in enumerate(res):
        _id, _date, _author, _topic, _medium, _source, _sourceLocation, _quote = row

        mesg += "\n\t" + "Quote #" + str(i+1) + " (QuoteID " + str(_id) + ") of " + str(len(res)) + ":"

        mesg += "\n\tTopic: " + str(_topic)

        src = ""
        if _source is None:
            src = _medium
        else:
            src = _source
        mesg += "\n\t" + "On " + str(_date) + ", " + _author + " says via " + src + ":\n\"\"\""

        mesg += "\n" + _quote 

        mesg += "\n\"\"\"\n"

        mesg += "\n------------------------------------------------------------------------------------\n"

    email(sub, mesg, to_address)



def email(sub, mesg, to_address):
    email_address = "connor.reed.92@gmail.com"
    fromaddr = email_address
    toaddr = to_address
    bcc_addr = email_address

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['BCC'] = bcc_addr
    msg['Subject'] = sub
    body = mesg
    msg.attach(MIMEText(mesg,'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, key_list.get(email_address))
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--author',default='')
    parser.add_argument('--topic',default='')
    parser.add_argument('--medium',default='')
    parser.add_argument('--keyword',default='')
    parser.add_argument('--count',default=5)
    parser.add_argument('--to_address',default='connor.reed.92@gmail.com')

    args = parser.parse_args()

    generate_body(args.author, args.topic, args.medium, args.keyword, args.count, args.to_address)

