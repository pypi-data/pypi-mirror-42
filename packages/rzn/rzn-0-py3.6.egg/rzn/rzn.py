#!/usr/bin/env python3
import argparse
import os
import configparser
import datetime
import shlex

def get_dotrzn():
    cwd = os.getcwd()
    while cwd != '/':
        dotrzn = cwd + '/.rzn'
        if os.path.exists(dotrzn):
            return dotrzn
        cwd = os.path.split(cwd)[0]
    return None

def main():
    config = configparser.ConfigParser()
    dotrzn = get_dotrzn()
    config.read(dotrzn)

    parser = argparse.ArgumentParser(description="rzn - rsync wrapper")
    args, unknown = parser.parse_known_args()

    rsync = ['rsync']

    c = {
        'datetimeisoformat': datetime.datetime.now().isoformat()
    }
    c['remote'] = config['main']['remote']
    c['local'] = os.path.dirname(dotrzn) + config['main'].get('append', '')

    rsync += shlex.split(config['main'].get('args', '').format(**c))
    if 'push' in unknown:
        rsync.append(c['local'])
        rsync.append(c['remote'])
    if 'pull' in unknown:
        rsync.append(c['remote'])
        rsync.append(c['local'])

    print([rsync])

    os.execvp('rsync', rsync)

if __name__ == "__main__":
    main()
