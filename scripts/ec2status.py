#!/usr/bin/env python

import argparse

import boto
from boto.sqs.message import Message
from boto.sqs.queue import Queue


aparser = argparse.ArgumentParser(description='Send status messages to sqs.')
aparser.add_argument('access_key', type=str)
aparser.add_argument('secret_key', type=str)
aparser.add_argument('queue', type=str)
aparser.add_argument('name', type=str)
aparser.add_argument('process', type=str)
aparser.add_argument('status', type=str)
args = aparser.parse_args()


conn = boto.connect_sqs(args.access_key, args.secret_key)
q = Queue(conn, args.queue)
m = Message()
m.set_body('%s:%s:%s' % (args.name, args.process, args.status))
q.write(m)
