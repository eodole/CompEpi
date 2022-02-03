#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 11:14:56 2021

@author: ellieodole
"""

import random 
import numpy as np
import sys
import ast
import math

#Find the probability for a single normal distribution
def normal_dist(x , mean , sd):
    prob_density = (1/(sd*np.sqrt(2*np.pi))* np.exp((-1/2)*(((x - mean)/sd)**2)))
    return prob_density

#Find the probability as a point for the mixture model
def mixtureModel(x ,mu, sigma, prop): 
    prob_density = 0
    for i in range(0, len(mu)):
        
        prob_density = prob_density + prop[i]*normal_dist(x, mu[i], sigma[i])
   
    return prob_density

#Randomly generate a sample from the mixture model 
def generate_sample(mu_list,sigma_list,prop_list):
    sample = None
    while sample == None:
        x = random.random() * 7  # x in (0,5) => 0 sec - 4 hour visits are possible.
        y = random.random()
        if y < mixtureModel(x, mu_list, sigma_list,prop_list) :
            sample = x 
    return math.exp(sample) 

## DEFUNT: 

# def generate_sample(n):
#     n_samples =[]
#     while len(n_samples) < n:
#         x = random.randint(0, maxSec) 
#         y = random.random()
        
#         if y < mixtureModel(x):
            
#             n_samples.append(x)
#     return n_samples



# if __name__ == "__main__":
#     #Takes inputs as :
#     # proportion list "[p1,p2....pn]""
#     # mean list "[m1,m2,....,m_n]""
#     # standard deviation list "[s1,s2,....,sn]"
#     prop = ast.literal_eval(sys.argv[1])
#     print(prop)
#     print(type(prop))
#     mu = ast.literal_eval(sys.argv[2])
#     sigma = ast.literal_eval(sys.argv[3])
#     n = ast.literal_eval(sys.argv[4])
#     print(generate_samples(n))
    

    