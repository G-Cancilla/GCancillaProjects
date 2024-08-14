#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 20:26:15 2019

@author: Joshua L. Phillips
Department of Computer Science
Middle Tennessee State University
Illustration of a set

Portions based on Python code provided by
Scott P. Morton
Center for Computational Science
Middle Tennessee State University
"""

import copy

class Set():
    def __init__(self):
        self.thisSet = set()
    def add(self,entry):
        if entry is not None:
            self.thisSet.add(entry.__hash__())
    def length(self):
        return len(self.thisSet)
    def isMember(self,query):
        return query.__hash__() in self.thisSet


class state():
    def __init__(self):
        self.xpos = 0
        self.ypos = 0
        self.tiles = [[0,1,2],[3,4,5],[6,7,8]]
    def left(self):
        if (self.ypos == 0):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos-1]
        s.ypos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def right(self):
        if (self.ypos == 2):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos+1]
        s.ypos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def up(self):
        if (self.xpos == 0):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos-1][s.ypos]
        s.xpos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def down(self):
        if (self.xpos == 2):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos+1][s.ypos]
        s.xpos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def __hash__(self):
        return (tuple(self.tiles[0]),tuple(self.tiles[1]),tuple(self.tiles[2]))
    def __str__(self):
        return '%d %d %d\n%d %d %d\n%d %d %d\n'%(
                self.tiles[0][0],self.tiles[0][1],self.tiles[0][2],
                self.tiles[1][0],self.tiles[1][1],self.tiles[1][2],
                self.tiles[2][0],self.tiles[2][1],self.tiles[2][2])
    def copy(self):
        s = copy.deepcopy(self)
        return s


def main():
    s = state()

    su = s.up()
    sd = s.down()
    sl = s.left()
    sr = s.right()

    myset = Set()

    myset.add(s)
    myset.add(su) # Can't move up from goal state
    myset.add(sd)
    myset.add(sl) # Can't move left from goal state
    myset.add(sr)

    print(myset.isMember(s))
    print(myset.isMember(su)) # Should be False
    print(myset.isMember(sd))
    print(myset.isMember(sl)) # Should be False
    print(myset.isMember(sr))
    
main()
