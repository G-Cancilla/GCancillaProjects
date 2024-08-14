#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import argparse
import sys
import pickle
import string

def stateToString(state):
    stateToString = "" 
    endStateFlag = 0
    for row in state:
        for num in row:
            stateToString += str(num)
        endStateFlag +=1
        if(endStateFlag < 3):
            stateToString += "\n"
    
    return stateToString

def mainServerFunction():
    goalState = [[0,1,2],[3,4,5],[6,7,8]]
    
    goalStateString = stateToString(goalState)
    print(goalStateString)
mainServerFunction()


