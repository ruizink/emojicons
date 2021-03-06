#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# (c) 2016, Mario Santos <mario.rf.santos@gmail.com>
#

from __future__ import unicode_literals

import os
import sys
import logging
import re
import json
import requests
import argparse
import pyperclip
from lxml import html
from tabulate import tabulate

logging.basicConfig(stream=sys.stderr, level=logging.WARNING, format='%(levelname)s:%(asctime)s:%(message)s')

_config = {
    'emojicons_baseurl': 'http://emojicons.com/',
    'route': {
        'search': 'tag/{text}',
        'hof': 'hall-of-fame',
        'popular': 'popular',
        'random': 'random',
        'get': 'e/{id}'
    },
    'xpath': {
        'ids': '//div[@class="emoticons-list"]/div[@class="emoticon-item"]/@id',
        'titles': '//div[@class="emoticons-list"]/div[@class="emoticon-item"]/div[@class="title"]/a/text()',
        'emojis': '//div[@class="emoticons-list"]/div[@class="emoticon-item"]/div[@class="listing"]//textarea/text()'
    }
}

def fetch_emojis(route):
    """Requests a given route and parses the results"""
    url = _config['emojicons_baseurl'] + route
    logging.debug("Requesting URL '{0}'".format(url))
    page = requests.get(url)
    tree = html.fromstring(page.text)
    emojis = []
    for id, t, e in zip([re.search("^emoticon-(\d+)$", x).group(1) for x in tree.xpath(_config['xpath']['ids'])],
                        tree.xpath(_config['xpath']['titles']),
                        tree.xpath(_config['xpath']['emojis'])):
        emojis.append({'id': id, 'title': t, 'emoji': e})
    return emojis


def load_file(file_path, graceful=False):
    """Loads a file into a json object"""
    try:
        with open(file_path) as data_file:
            json_obj = json.load(data_file)
        logging.debug("Loaded JSON file from '{0}'".format(file_path))
    except IOError:
        if graceful:
            json_obj = []
        else:
            logging.error("¯\_(ツ)_/¯ There is no such file: '{0}'".format(file_path))
            sys.exit(1)
    except ValueError:
        logging.error("¯\_(ツ)_/¯ That's not JSON at all! '{0}'".format(file_path))
        sys.exit(2)
    return json_obj


def save_file(file_path, json_obj):
    """Saves json object into a file"""
    try:
        with open(file_path, 'w') as outfile:
            json.dump(json_obj, outfile)
        logging.debug("Saved JSON to file '{0}'".format(file_path))
    except IOError:
        logging.error("¯\_(ツ)_/¯ Can't even open the file for writing: {0}'".format(file_path))
        sys.exit(1)


def print_table(emojis):
    """Prints a table with the emoji_list"""
    if len(emojis) > 0:
        table = []
        for i in emojis:
            table.append([i.get('id'), i.get('title'), i.get('emoji')])
        print(tabulate(table, headers=["ID", "Title", "Emoji"]))
    else:
        print("¯\_(ツ)_/¯ Nothing to see here...")


def do_request(route, text):
    """Builds a route and prints the results"""
    emojis = fetch_emojis(_config['route'][route].format(text=text))
    return emojis


def go_fetch(args):
    """Expand the args, do the site request and print the results"""
    if hasattr(args, 'str'):
        emojis = do_request(args.subcommand, ' '.join(args.str))
    else:
        emojis = do_request(args.subcommand)
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
        emoji = fetch_emojis(_config['route']['get'].format(id=emoji_id))[0]
        if emoji.get('id') not in [x.get('id') for x in emojis]:
            emojis.append(emoji)
            save_file(json_file, emojis)
            print("Emoji saved to '{0}'".format(json_file))
            print_table([emoji])
        else:
            print("¯\_(ツ)_/¯ Emoji with id '{0}' already saved!".format(emoji_id))
    except IndexError:
        logging.error("¯\_(ツ)_/¯ Couldn't find the emoji with id '{0}'!"
                      .format(emoji_id))
        sys.exit(3)


def copy_to_clip(args):
    """Copies an emoji from disk to the clipboard"""
    json_file = args.file[0]
    emoji_id = args.id[0]
    emojis = load_file(json_file, graceful=True)
    filtered_list = list(filter(lambda x: x.get('id') == emoji_id 
                         or x.get('title') == emoji_id,
                         emojis))
    if len(filtered_list) == 1:
        emoji = filtered_list[0].get('emoji')
        pyperclip.copy(emoji)
        print("Emoji '{0}' copied to clipboard!".format(emoji))
    else:
        logging.error("¯\_(ツ)_/¯ Couldn't find the emoji with title or id '{0}'!".format(emoji_id))
        sys.exit(3)


def delete_emojicon(args):
    """Deletes an emoji from disk"""
    json_file = args.file[0]
    emoji_id = args.id[0]
    emojis = load_file(json_file, graceful=True)
    if emoji_id in [x.get('id') for x in emojis]:
        emojis[:] = [e for e in emojis if e.get('id') != emoji_id]
        save_file(json_file, emojis)
        print("Emoji with id '{0}' deleted from '{1}'".format(emoji_id, json_file))
    else:
        logging.error("¯\_(ツ)_/¯ Couldn't find the emoji with id '{0}'!".format(emoji_id))
        sys.exit(3)


def main():
    """Program entry point"""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand', help='subcommand help')

    search = subparsers.add_parser('search', help='search for an emojicon')
    search.add_argument('str', nargs='*', help='search string')
    search.set_defaults(func=go_fetch)

    hof = subparsers.add_parser('hof', help='shows the hall of fame')
    hof.set_defaults(func=go_fetch)

    popular = subparsers.add_parser('popular', help='shows popular stuff')
    popular.set_defaults(func=go_fetch)

    random = subparsers.add_parser('random', help='shows random stuff')
    random.set_defaults(func=go_fetch)

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

    clip = subparsers.add_parser('clip', help='copy an emojicon to the clipboard')
    clip.add_argument('id', nargs=1, help='id of the emojicon')
    clip.add_argument('--file', '-f', nargs=1, default=[os.getenv('HOME') + '/.emoji.json'])
    clip.set_defaults(func=copy_to_clip)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()