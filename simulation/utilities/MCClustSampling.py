# Copyright 2022, The University of Iowa.  All rights reserved.
# Permission is hereby given to use and reproduce this software 
# for non-profit educational purposes only.

# REU Computing for Health and Well-being 2022
# Partial Funding from CDC MiND Grant and NSF REU Grant
# Authors: Leona Odole, Maren Gingerich, Amanda Perera

# Functions Avaiable
#   - readMclust : which accepts mclust output csv file and stores parameters in a data frame
#   - generate_sample: randomly generates a duration of visit in seconds from a mixture model
#   - normal_dist: finds the probability for a normal distribution at a given point x
#   - mixtureModel: finds the probability for a mixture model at a given point x
#   - grab_parameters: create a list of parameters that can be used as input for generate_sample function

import pandas as pd 
import random
import numpy as np


# Find the probability for a single normal distribution
def normal_dist(x , mean , sd):
    prob_density = (1/(sd*np.sqrt(2*np.pi))* np.exp((-1/2)*(((x - mean)/sd)**2)))
    return prob_density

# Find the probability at a point for the mixture model
def mixtureModel(x ,mu, sigma, prop): 
    prob_density = 0
    for i in range(0, len(mu)):
        
        prob_density = prob_density + prop[i]*normal_dist(x, mu[i], sigma[i])
   
    return prob_density

# Input: filename of csv file containing Mclust data by jtid
# Output: dataframe indexed by jtid
def readMclust(filename):
    df = pd.read_csv(filename, index_col='jtid')
    return df



def prepend(list, str):
    str += '{0}'
    list = [str.format(i) for i in list]
    return list

# Create a list of parameters that can be used as input for generate_sample function 
# Inputs: dataframe from readMclust function and jtid specified by user
# Outputs: list of all mu, var, and prop for each cluster for that jtid 
def grab_parameters(frame, ftid, utid, jtid):
    new = frame[(frame['jtid'] == jtid) & (frame['ftid'] == ftid) & (frame['utid'] == utid)]
    nclust = int(new['num_dists'])
    lst = list(range(1,nclust + 1))
    pro = prepend(lst, 'pro ')
    mean = prepend(lst, 'mean ')
    sigmasq = prepend(lst, 'sigmasq ')
    mu = []
    var = []
    prop = []
    for i in range(0, len(lst)):
        a = list(new[mean[i]])
        mu.append(a)
        b = list(new[sigmasq[i]])
        var.append(b)
        c = list(new[pro[i]])
        prop.append(c)

    return mu, var, prop
    


# Input: mu_list, sigma_list, prop_list, lists of parameters for an mclust mixture model 
#       (might change this to accept dataframe instead.)
# Output: a randomly generated observation based on the input mixutre model, using rejection sampling: 
#           for more information on rejection sampling, see: https://en.wikipedia.org/wiki/Rejection_sampling

def generate_sample(mu_list,sigma_list,prop_list):
    sample = None
    while sample == None:
        #Randomly generate a sample from the mixture model using rejection sampling from  :
            # 1. Sample a point on the x-axis from the proposal distribution.
            # 2. Draw a vertical line at this x-position, up to the maximum y-value of the probability density function of the proposal distribution.
            # 3. Sample uniformly along this line from 0 to the maximum of the probability density function. If the sampled value is greater than the 
            # value of the desired distribution at this vertical line, reject the x-value and return to step 1; else the x-value is a sample from 
            # the desired distribution.
        x = random.random() * 60 * 60 * 4 # limiting length to 4 hrs 
        y = random.random()
        if y < mixtureModel(x, mu_list, sigma_list,prop_list) :
            sample = x 
    return sample

