#!/usr/bin/env python

import sys

import boto


conn = boto.connect_ec2()

# Make sure quickness name is going to be unique
groups = conn.get_all_security_groups()
for group in groups:
    print group.id, group.name
