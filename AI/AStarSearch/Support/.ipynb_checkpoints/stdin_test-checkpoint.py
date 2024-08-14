#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 23:25:15 2020

@author: Joshua L. Phillips
Department of Computer Science
Middle Tennessee State University
Illustration of reading from
standard input...

"""

import sys


if (len(sys.argv) != 1):
    print()
    print("Usage: %s" %(sys.argv[0]))
    print()
    sys.exit(1)

# There is no error checking in this code
# Well formatted input is assumed as well as
# proper processing given well-formed input

def main():
    inputs = []
    for line in sys.stdin:
        inputs += line.split()

    print(' '.join(inputs))
        
main()
