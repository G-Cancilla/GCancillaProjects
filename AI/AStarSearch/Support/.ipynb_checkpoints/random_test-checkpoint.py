#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 20:26:15 2019

@author: Joshua L. Phillips
Department of Computer Science
Middle Tennessee State University
Illustration of random movement generation

Portions based on Python code provided by
Scott P. Morton
Center for Computational Science
Middle Tennessee State University
"""

import sys, numpy.random as random


if (len(sys.argv) != 3):
    print()
    print("Usage: %s [seed] [number of random moves]" %(sys.argv[0]))
    print()
    sys.exit(1)

# There is no error checking in this code
# Well formatted input is assumed as well as
# proper processing given well-formed input

def main():
    # Just once
    rng = random.default_rng(int(sys.argv[1]))
    number_of_moves = int(sys.argv[2])
    
    # Can call this as many times as needed to generate moves...
    for x in range(number_of_moves):
        # These moves will be 0,1,2,3 which can each be
        # associated with a particular movement direction
        # (i.e. up, down, left, right).
        move = rng.integers(4) 
        print(move)
        
main()
