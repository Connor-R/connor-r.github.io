import argparse
import sys
from py_db import db

# Finds quotes with certain author/topic/medium/keyword

db = db('personal')


def process(author, topic, medium, keyword):

    if (author == '' and topic == '' and medium == '' and keyword == ''):
        sys.exit('\n\nplease specify an author, topic, medium, or keyword\n\n')

    quote_lookup = """SELECT 
    estimated_date, author, topic, medium, source, source_location, quote
    FROM quotes
    WHERE 1
    AND (author LIKE "%%%s%%" AND topic LIKE "%%%s%%" AND medium LIKE "%%%s%%" AND quote LIKE "%%%s%%")
    ;""" % (author, topic, medium, keyword)

    res = db.query(quote_lookup)

    for i, row in enumerate(res):
        _date, _author, _topic, _medium, _source, _sourceLocation, _quote = row

        print "\n-----------------------------\n"

        print "\t" + "Quote #" + str(i+1) + " of " + str(len(res)) + ":"

        print "\tTopic: " + str(_topic)

        src = ""
        if _source is None:
            src = _medium
        else:
            src = _source
        print "\t" + "On " + str(_date) + ", " + _author + " says via " + src + ":\n\"\"\""

        print _quote 

        print "\"\"\"\n"




if __name__ == "__main__":  

    parser = argparse.ArgumentParser()

    parser.add_argument('--author',default='')
    parser.add_argument('--topic',default='')
    parser.add_argument('--medium',default='')
    parser.add_argument('--keyword',default='')

    args = parser.parse_args()

    process(args.author, args.topic, args.medium, args.keyword)
    
    