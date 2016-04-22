#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# (c) 2016, Mario Santos <mario.rf.santos@gmail.com>
#

from lxml import html
import requests
import argparse
from tabulate import tabulate

EMOJICONS_URL = 'http://emojicons.com/'
ENDPOINTS = {
    'search': 'tag/%s',
    'hof': 'hall-of-fame',
    'popular': 'popular',
    'random': 'random'
}
XPATHS = {
    'titles': '//div[@class="emoticons-list"]/div[@class="emoticon-item"]/div[@class="title"]/a/text()',
    'emojis': '//div[@class="emoticons-list"]/div[@class="emoticon-item"]/div[@class="listing"]//textarea/text()'
}


def fetch_emojis(endpoint):
    url = EMOJICONS_URL + endpoint
    page = requests.get(url)
    tree = html.fromstring(page.text)
    titles = tree.xpath(XPATHS.get('titles'))
    emojis = tree.xpath(XPATHS.get('emojis'))
    return titles, emojis


def print_table(emoji_list):
    table = []
    for t, e in zip(*emoji_list):
        table.append([t, e])
    if len(table) > 0:
        print tabulate(table, headers=["Title", "Emoji"])
    else:
        print "¯\_(ツ)_/¯ Nothing to see here..."


def route_cmd(args):
    subparser_name = str(args.subparser_name)
    try:
        subargs = ' '.join(args.str)
        #print "Executing command: %s with args %s..." % (subparser_name, subargs)
        emojis_list = fetch_emojis(ENDPOINTS.get(subparser_name) % subargs)
    except AttributeError:
        #print "Executing command: %s..." % subparser_name
        emojis_list = fetch_emojis(ENDPOINTS.get(subparser_name))
    print_table(emojis_list)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help', dest='subparser_name')
    parser.set_defaults(func=route_cmd)

    search = subparsers.add_parser('search', help='search for an emojicon')
    search.add_argument('str', nargs='*', help='search string')

    hof = subparsers.add_parser('hof', help='show the hall of fame')

    popular = subparsers.add_parser('popular', help='show popular stuff')

    random = subparsers.add_parser('random', help='show random stuff')

    args = parser.parse_args()
    args.func(args)