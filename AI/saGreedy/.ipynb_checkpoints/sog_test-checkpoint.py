#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 10:12:37 2019

@author: Joshua L. Phillips
Department of Computer Science
Middle Tennessee State University
Illustration of how to sample
from the SoG function.

Portions based on Python code provided by
Scott P. Morton
Center for Computational Science
Middle Tennessee State University

Modifed by J.L.P - 2022-09-29 12:05:38
"""
import SumofGaussians as SG
import numpy as np, sys

seed = int(sys.argv[1])
dims = int(sys.argv[2])
ncenters = int(sys.argv[3])

rng = np.random.default_rng(seed)
sog = SG.SumofGaussians(dims,ncenters,rng)

epsilon = 1e-8

# Data
data_input = np.loadtxt(sys.stdin)

for i in data_input:
    print("%.8f"%(sog.Evaluate(i)),end=' ')
    print(" ".join(["%.8f"%(x) for x in sog.Gradient(i)]))
    
sys.exit(0)

