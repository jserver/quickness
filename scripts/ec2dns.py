#!/usr/bin/env python

import argparse

import boto


aparser = argparse.ArgumentParser(description='Return the public_dns of one of your instances.')
aparser.add_argument('name', metavar='name', type=str,
                     help='Name of the quickness machine')
args = aparser.parse_args()


conn = boto.connect_ec2()

# Make sure quickness name is going to be unique
reservations = conn.get_all_instances(filters={'tag:Name': 'quickness', 'tag:Quickness': args.name})
for res in reservations:
    for instance in res.instances:
        print instance.public_dns_name
