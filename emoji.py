#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# (c) 2016, Mario Santos <mario.rf.santos@gmail.com>
#

import os
import sys
import re
import json
import requests
import argparse
from lxml import html
from tabulate import tabulate

EMOJICONS_URL = 'http://emojicons.com/'
ROUTES = {
    'search': 'tag/%s',
    'hof': 'hall-of-fame',
    'popular': 'popular',
    'random': 'random',
    'get': 'e/%s'
}
XPATHS = {
    'ids': '//div[@class="emoticons-list"]/div[@class="emoticon-item"]/@id',
    'titles': '//div[@class="emoticons-list"]/div[@class="emoticon-item"]/div[@class="title"]/a/text()',
    'emojis': '//div[@class="emoticons-list"]/div[@class="emoticon-item"]/div[@class="listing"]//textarea/text()'
}


def fetch_emojis(route):
    """Requests a given route and parses the results"""
    url = EMOJICONS_URL + route
    page = requests.get(url)
    tree = html.fromstring(page.text)
    emojis = []
    for id, t, e in zip([re.search("^emoticon-(\d+)$", x).group(1) for x in tree.xpath(XPATHS.get('ids'))],
                        tree.xpath(XPATHS.get('titles')),
                        tree.xpath(XPATHS.get('emojis'))):
        emojis.append({'id': id, 'title': t, 'emoji': e})
    return emojis


def load_file(file_path, graceful=False):
    """Loads a file into a json object"""
    try:
        with open(file_path) as data_file:
            json_obj = json.load(data_file)
    except IOError:
        if graceful:
            json_obj = []
        else:
            print "¯\_(ツ)_/¯ There is no such file: '%s'" % file_path
            sys.exit(1)
    except ValueError:
        print "¯\_(ツ)_/¯ That's not JSON at all! '%s'" % file_path
        sys.exit(2)
    return json_obj


def save_file(file_path, json_obj):
    """Saves json object into a file"""
    try:
        with open(file_path, 'w') as outfile:
                json.dump(json_obj, outfile)
    except IOError:
        print "¯\_(ツ)_/¯ Can't even open the file for writing: '%s'" % file_path
        sys.exit(1)


def print_table(emojis):
    """Prints a table with the emoji_list"""
    if len(emojis) > 0:
        table = []
        for i in emojis:
            table.append([i.get('id'), i.get('title'), i.get('emoji')])
        print tabulate(table, headers=["ID", "Title", "Emoji"])
    else:
        print "¯\_(ツ)_/¯ Nothing to see here..."


def site_request(args):
    """Builds a route and prints the results"""
    subparser_name = args.subparser_name
    try:
        subargs = ' '.join(args.str)
        emojis = fetch_emojis(ROUTES.get(subparser_name) % subargs)
    except AttributeError:
        emojis = fetch_emojis(ROUTES.get(subparser_name))
    print_table(emojis)


def list_offline(args):
    """Lists the emojis saved to disk"""
    json_file = args.file[0]
    emojis = load_file(json_file)
    print_table(emojis)


def save_emojicon(args):
    """Fetches an emoji online and saves it to disk"""
    json_file = args.file[0]
    emoji_id = args.id[0]
    emojis = load_file(json_file, graceful=True)
    try:
        emoji = fetch_emojis(ROUTES.get('get') % emoji_id)[0]
        if emoji.get('id') not in [x.get('id') for x in emojis]:
            emojis.append(emoji)
            save_file(json_file, emojis)
            print "Emoji saved to '%s'" % json_file
            print_table([emoji])
        else:
            print "¯\_(ツ)_/¯ Emoji with id '%s' already saved!" % emoji_id
    except IndexError:
        print "¯\_(ツ)_/¯ Couldn't find the emoji with id '%s'!" % emoji_id
        sys.exit(3)


def delete_emojicon(args):
    """Deletes an emoji from disk"""
    json_file = args.file[0]
    emoji_id = args.id[0]
    emojis = load_file(json_file, graceful=True)
    if emoji_id in [x.get('id') for x in emojis]:
        emojis[:] = [e for e in emojis if e.get('id') != emoji_id]
        save_file(json_file, emojis)
        print "Emoji with id '%s' deleted from '%s'" % (emoji_id, json_file)
    else:
        print "¯\_(ツ)_/¯ Couldn't find the emoji with id '%s'!" % emoji_id
        sys.exit(3)

def main():
    """Program entry point"""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help', dest='subparser_name')
    parser.set_defaults(func=site_request)

    search = subparsers.add_parser('search', help='search for an emojicon')
    search.add_argument('str', nargs='*', help='search string')

    subparsers.add_parser('hof', help='shows the hall of fame')

    subparsers.add_parser('popular', help='shows popular stuff')

    subparsers.add_parser('random', help='shows random stuff')

    save_e = subparsers.add_parser('save', help='save an emojicon to filesystem')
    save_e.add_argument('id', nargs=1, help='id of the emojicon')
    save_e.add_argument('--file', '-f', nargs=1, default=[os.getenv('HOME') + '/.emoji.json'])
    save_e.set_defaults(func=save_emojicon)

    delete_e = subparsers.add_parser('delete', help='delete an emojicon from filesystem')
    delete_e.add_argument('id', nargs=1, help='id of the emojicon')
    delete_e.add_argument('--file', '-f', nargs=1, default=[os.getenv('HOME') + '/.emoji.json'])
    delete_e.set_defaults(func=delete_emojicon)

    list_e = subparsers.add_parser('list', help='lists all emojis currently saved in filesystem')
    list_e.add_argument('--file', '-f', nargs=1, default=[os.getenv('HOME') + '/.emoji.json'])
    list_e.set_defaults(func=list_offline)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()