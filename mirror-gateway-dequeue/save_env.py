#!/usr/bin/env python

import os

for k,v in os.environ.items():
    if ":" not in k:
        print 'export {}="{}"'.format(k, v.replace('"', '\"'))
