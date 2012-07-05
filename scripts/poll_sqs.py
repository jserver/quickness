#!/usr/bin/env python

import argparse
import glob
import multiprocessing
import os
import signal
import subprocess
import sys
import time
from ConfigParser import SafeConfigParser

import boto


def get_instance(conn, name, host):
    reservations = conn.get_all_instances(filters={'tag:Name': 'quickness'})
    for res in reservations:
        for instance in res.instances:
            if host in instance.private_dns_name:
                return instance


def copy_private(name, host):
    conn = boto.connect_ec2()
    instance = get_instance(conn, name, host)

    if not instance:
        print 'Unable to find instance %s' % name
        return

    instance_name = instance.tags.get('Quickness')

    # Time to copy in the private files
    print 'Copying private files to new machine'
    if glob.glob('etc/private/*'):
        subprocess.call('scp -i $AWS_IDENTITY -o StrictHostKeyChecking=no etc/private/* ubuntu@%s:~/.quickness_repo/etc/private' % instance.public_dns_name, shell=True)
    if glob.glob('formulas/*_private'):
        subprocess.call('scp -i $AWS_IDENTITY -o StrictHostKeyChecking=no formulas/*_private ubuntu@%s:~/.quickness_repo/formulas' % instance.public_dns_name, shell=True)
    if glob.glob('tweaks/*_private'):
        subprocess.call('scp -i $AWS_IDENTITY -o StrictHostKeyChecking=no tweaks/*_private ubuntu@%s:~/.quickness_repo/tweaks' % instance.public_dns_name, shell=True)

    print '%s [%s]: %s (%s)' % (instance_name, instance.id, instance.state, instance.public_dns_name)
    print 'To login: bin/quick_ec2 ssh %s' % instance_name


def signal_handler(signal, frame):
    print 'You pressed ctrl+c!'
    sys.exit(0)


def start_polling(filename, verbose=False):
    signal.signal(signal.SIGINT, signal_handler)


    cparser = SafeConfigParser()
    cparser.read(os.path.join('etc/private/', filename))


    if 'AWS_IDENTITY' not in os.environ:
        print 'Please set the AWS_IDENTITY environment variable to create a new ec2 machine'
        return

    sqs = boto.connect_sqs()
    q = sqs.get_queue(cparser.defaults()['queue'])
    print 'polling... <ctrl+c to quit>'
    while True:
        time.sleep(3)
        rs = q.get_messages()
        for m in rs:
            body = m.get_body()
            if verbose:
                print body
            q.delete_message(m)
            name, host, process, status = body.split(':')
            if process == 'bootstrap' and status == 'finished':
                p = multiprocessing.Process(target=copy_private, args=(name,host,))
                p.start()


if __name__ == '__main__':
    aparser = argparse.ArgumentParser(description='Create an ec2 instance.')
    aparser.add_argument('-f', '--file', dest='filename', default='ec2.conf',
                         help='Name of the config file in etc/private - defaults to ec2.conf')
    aparser.add_argument('-v', '--verbose', action='store_true',
                         help='Show all messages when polling')
    args = aparser.parse_args()

    start_polling(args.filename, verbose=True)
