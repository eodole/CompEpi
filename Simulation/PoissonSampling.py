import random
import numpy as np
import math
import scipy
from scipy import stats
import sys

#Read in csv parameters or intake from command line arguments

#Inputs: Lambda parameter as lam

#poission equation
def find_maxVisits(lam):
    return scipy.stats.poisson.ppf(.995,1)
    

def poission_distribution(lam,k):
    return ((lam**k)*(math.exp(-lam)))/(math.factorial(k))
    

def generate_sample(n, lam, maxVisits):
    n_samples = []
    while len(n_samples) <n:
        x = random.randint(0, maxVisits)  
        y = random.random()
        if y < poission_distribution(lam, x):
            n_samples.append(x)
    return n_samples

if __name__ == "__main__":
    ##Read inputs
        # lambda, n_samples 
    lam = sys.argv[1]

        ##Do I need to transform lamda? 
    maxVisits = find_maxVisits(lam)
    print(maxVisits)
    print(generate_sample(7,1,maxVisits))


#output