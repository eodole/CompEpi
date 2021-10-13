#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 11:14:56 2021

@author: ellieodole
"""

import random 
import numpy as np

mu = [0,4]
sigma = [.5,3]
prop = [.33,.67]

#Generate pdf
maxSec = 5
n = 5

def normal_dist(x , mean , sd):
    prob_density = (1/(sd*np.sqrt(2*np.pi))* np.exp((-1/2)*(((x - mean)/sd)**2)))
    return prob_density

def mixtureModel(x): 
    prob_density = 0
    for i in range(0, len(mu)):
        
        prob_density = prob_density + prop[i]*normal_dist(x, mu[i], sigma[i])
   
    return prob_density
    
n_samples =[]
while len(n_samples) < n:
     x = random.randint(0, maxSec) #Needs to be modified
     y = random.random()
     
     if y < mixtureModel(x):
        
        n_samples.append(x)

print(n_samples)