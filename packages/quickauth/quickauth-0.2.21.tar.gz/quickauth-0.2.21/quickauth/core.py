import argparse
from datetime import datetime
from uuid import uuid1, uuid4

from redislite import Redis


class QuickAuth:
    def __init__(self, dbfile='auth.db'):
        self.conn = Redis(dbfile)

    def register(self, key=None):
        if key is None:
            key = str(uuid1(clock_seq=int(datetime.now().timestamp())))
        value = str(uuid4())
        if self.conn.set(key, value):
            return {
                'key': key,
                'secret': value
            }
        else:
            raise ValueError('write to database failed: {} = {}'.format(key, value))

    def authorize(self, key, value):
        c = self.conn.get(key)
        if c is not None:
            return c.decode() == value
        return False

    def update(self, key):
        if self.conn.get(key):
            return self.register(key=key)
        else:
            raise ValueError('key is not found: {}'.format(key))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', type=str, default='auth.db', help='database file, default: auth.db')
    parser.add_argument('-k', '--key', type=str, help='key')
    parser.add_argument('-s', '--secret', type=str, help='secret')
    parser.add_argument('operation', metavar='OPERATION', type=str, choices=['register', 'authorize', 'update'], help='register, authorize, or update')
    args, _ = parser.parse_known_args()
    auth = QuickAuth()
    if args.operation == 'register':
        print(auth.register())
    elif args.operation == 'authorize':
        if args.key is not None:
            if args.secret is not None:
                print(auth.authorize(args.key, args.secret))
            else:
                parser.error('secret is not provided')
        else:
            parser.error('key is not provided')
    elif args.operation == 'update':
        if args.key is not None:
            print(auth.update(args.key))
        else:
            parser.error('key is not provided')
