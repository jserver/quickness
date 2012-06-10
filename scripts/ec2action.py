#!/usr/bin/env python

import argparse

import boto


aparser = argparse.ArgumentParser(description='Perform an action on an ec2 instance.')
aparser.add_argument('action', type=str,
                     help='Action: reboot start stop terminate')
aparser.add_argument('name', type=str,
                     help='Name of the quickness machine')
args = aparser.parse_args()


conn = boto.connect_ec2()

# Make sure quickness machine exists and if it does give user 1 last chance to save it
reservations = conn.get_all_instances(filters={'tag:Name': 'quickness', 'tag:Quickness': args.name})
for res in reservations:
    for instance in res.instances:
        if args.action == 'reboot':
            print 'Rebooting %s' % args.name
            instance.reboot()
        elif args.action == 'start':
            print 'Starting %s' % args.name
            instance.start()
        elif args.action == 'stop':
            print 'Stopping %s' % args.name
            instance.stop()
        elif args.action == 'terminate':
            s = raw_input('Are you sure you want to terminate %s (Y/N)? ' % args.name)
            if s == 'Y':
                print 'Terminating %s' % args.name
                instance.terminate()
