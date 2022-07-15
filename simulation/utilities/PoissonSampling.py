import random
import numpy as np
import math
import scipy
from scipy import stats


#Read in csv parameters or intake from command line arguments

#Inputs: Lambda parameter as lam

#poission equation
def find_maxVisits(lam):
    return scipy.stats.poisson.ppf(.995,1)
    

def poission_distribution(lam,k):
    return ((lam**k)*(math.exp(-lam)))/(math.factorial(k))
    

def generate_sample(lam):
    n = True
    while n == True:  
        maxVisits = find_maxVisits(lam)
        x = random.randint(0, maxVisits)  
        y = random.random()
        if y < poission_distribution(lam, x):
            n = x
    return n

# if __name__ == "__main__":
#     ##Read inputs
#         # lambda, n_samples 
#     lam = sys.argv[1]
#     n = sys.argv[2]
#         ##Do I need to transform lamda? 
#     maxVisits = find_maxVisits(lam)
#     print(maxVisits)
#     print(generate_sample(n,lam,maxVisits))


#output