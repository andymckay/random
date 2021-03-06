#!/usr/bin/env python
# check to see if documents exists for a specific query

from optparse import OptionParser
from datetime import datetime, timedelta
import sys
import urllib2
import json


def get_date(delay):
    today = datetime.now()
    yesterday = today - timedelta(hours=delay)
    return "%s-%s-%s" % (yesterday.year, yesterday.month, yesterday.day)


def check_query(host, index, date):
    body = json.dumps({'query': {'term': {'date': date}}})
    url = "http://%s:9200/%s/_search" % (host, index)
    req = urllib2.Request(url, body, {'Content-Type': 'application/json'})
    result = json.loads(urllib2.urlopen(req).read())
    return result['hits']['total']


def alert(result, date):
    if result > 0:
        print "ES DOCUMENTS OK: %s documents for %s" % (result, date)
        sys.exit(0)
    else:
        print "ES DOCUMENTS CRITICAL: %s documents for %s" % (result, date)
        sys.exit(2)


def main():
    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option("-d", "--delay",
                      default=9,
                      type=int,
                      help="Delay")
    parser.add_option("-e", "--host",
                      default='localhost',
                      type='string',
                      help="Elasticsearch Host")
    parser.add_option("-i", "--index",
                      default='*',
                      type='string',
                      help="Elasticsearch index")

    (options, args) = parser.parse_args()

    date = get_date(options.delay)
    result = check_query(options.host, options.index, date)
    alert(result, date)

if __name__ == '__main__':
    main()
