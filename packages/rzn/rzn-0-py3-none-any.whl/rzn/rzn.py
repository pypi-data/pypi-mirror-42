#!/usr/bin/env python3
import argparse
import os
import configparser
import datetime
import shlex
import sys

def main():
    dotrzn = None
    cwd = os.getcwd()
    while cwd != '/':
        test = cwd + '/.rzn'
        if os.path.exists(test):
            dotrzn = test
            break
        cwd = os.path.split(cwd)[0]

    if dotrzn is None:
        print("error: .rzn not found")
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(dotrzn)

    parser = argparse.ArgumentParser(description="rzn - rsync wrapper")
    parser.add_argument("--dry-run", action='store_true')
    args, unknown = parser.parse_known_args()

    if 'command' in config['main']:
        rsync = config['main']['command'].split(' ')
    else:
        rsync = ['rsync']

    c = {
        'datetimeisoformat': datetime.datetime.now().isoformat()
    }
    c['append'] = config['main'].get('append', '')
    c['remote'] = config['main']['remote'] + c['append']
    c['local'] = os.path.dirname(dotrzn) + c['append']

    if 'push' in unknown:
        c['fulltarget'] = config['main']['remote']
        c['target'] = ":".join(config['main']['remote'].split(':')[1:])
    else:
        c['fulltarget'] = c['target'] = c['local'] + '..'

    sparsefilters = config["main"].get('sparsefilters')
    if sparsefilters:
        for item in sparsefilters.split('\n'):
            if not item: continue
            if item[0] == "#": continue
            parent = "/"
            for part in item.split("/")[1:-1]:
                parent += part + "/"
                rsync += ["--filter=+ " + parent]
            rsync += [
                "--filter=+ " + item,
                "--filter=R " + item,
            ]
        rsync.append("--filter=- ***")
        if 'push' in unknown:
            rsync.append("--filter=P ***")

    rsync += shlex.split(config['main'].get('args', '').format(**c))

    if 'push' in unknown:
        rsync += shlex.split(config['main'].get('push_args', '').format(**c))

        rsync.append(c['local'])
        rsync.append(c['remote'])

    if 'pull' in unknown:
        rsync += shlex.split(config['main'].get('pull_args', '').format(**c))

        rsync.append(c['remote'])
        rsync.append(c['local'])

    if args.dry_run:
        for arg in rsync:
            print(arg)
        rsync.append("--dry-run")

    os.execvp(rsync[0], rsync)

if __name__ == "__main__":
    main()
