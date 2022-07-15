#!/usr/local/anaconda3/bin/python
# Alberto Maria Segre
#
# Copyright 2021, The University of Iowa.  All rights reserved.
# Permission is hereby given to use and reproduce this software 
# for non-profit educational purposes only.
from sys import stdin
import re

# Parse Ellie's R output.
#
#   Treats input as a series of analyses. In each analysis, we collect
#   information from consecutive lines and produce a single CSV file
#   line. Each analysis looks like this:
#  
#   [1] "GroupA.tsv" "weekday" "day"
#   [1] "Group Facility IDs: 21 Job Type ID: 1"
#   [2] "Group Facility IDs: 29 Job Type ID: 1"
#   [3] "Group Facility IDs: 28 Job Type ID: 1"
#   
#   Call:
#   zeroinfl(formula = hcwVistsPerHour$Freq ~ 1, dist = "poisson")
#   
#   Pearson residuals:
#       Min      1Q  Median      3Q     Max
#   -0.1538 -0.1538 -0.1538 -0.1538 26.3548
#   
#   Count model coefficients (poisson with log link):
#               Estimate Std. Error z value Pr(>|z|)
#   (Intercept) 1.104703   0.001066    1036   <2e-16 ***
#   
#   Zero-inflation model coefficients (binomial with logit link):
#               Estimate Std. Error z value Pr(>|z|)
#   (Intercept) 3.450733   0.001783    1936   <2e-16 ***
#   ---
#   Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
#   
#   Number of iterations in BFGS optimization: 9
#   Log-likelihood: -2.119e+06 on 2 Df
#
# And produces a single output line; here:
#    Group,shift,facilities,job,slope,intercept
#    A,weekday,21 29 28,1,1.104703,0.001066

# Set up regular expressions we need to find in the output.
# Detect: [1] "GroupA.tsv" "weekday" "day"
RE0 = re.compile('\[\d+\]\s+"Group([A-Z]+).tsv"[^"]+"([^"]+)"[^"]+"([^"]+)"')

# Detect: [3] "Group Facility IDs: 28 Job Type ID: 1"
RE1 = re.compile('\[\d+\]\s+"Group Facility IDs:\s(\d+)\s+Job\sType\sID:\s(\d+)"')

# Detect: (Intercept) 0.753144   0.004796   157.1   <2e-16 ***
RE2 = re.compile('\(Intercept\)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+')

# Detect: [1] "=========================="
RE3 = re.compile('\[\d+\]\s+"=+"')

RE4 = re.compile('\[\d+\]\s+"Less Than 25 Observations"')

if __name__ == '__main__':
    # Print header of CSV file.
    print('Group,day,shift,facilities,job,slope,intercept')
    # Operate in 3 phases: 0=initiate, 1=search, 2=parameters
    phase = 0
    while True:
        # Read next line.
        line = stdin.readline()
        #print('{}: {}'.format(phase,line.strip()))
        if len(line) == 0:
            # EOF
            break
        elif phase == 0:
            # Looking for a m0 match to mark start of an analysis.
            m0 = RE0.match(line.strip())
            if m0:
                # Match.
                analysis = '{},{},{},'.format(m0.group(1),m0.group(2),m0.group(3))
                # Go on to next phase.
                phase = 1
                #print("End phase 0")
            continue
        elif phase == 1:
            # Looking for facility ids that apply.
            m1 = RE1.match(line.strip())
            if m1:
                # Match. Add it to analysis.
                analysis = analysis + '{} '.format(m1.group(1))
                job = m1.group(2)
            else:
                # Go on to next phase. But first strip trailing
                # blank from analysis and add in job type.
                analysis = analysis.rstrip() + ',{}'.format(job)
                phase = 2
                #print("End phase 1")
            continue
        elif phase == 2:
            # Looking for results. We want the first matching
            # intercept line, not the zero-inflation line.
            l2 = line.strip()
            m2 = RE2.match(l2)
            m4 = RE4.match(l2)
            if m2:
                # Match. Print the analysis and start looking for the
                # next one.
                print(analysis + ',{},{}'.format(m2.group(1), m2.group(2)))
                phase = 3
                #print("End phase 2")
            elif m4:
                print(analysis + ', NULL, NULL' )
                phase = 3
        elif phase == 3:
            # Looking for next analysis. This is just like phase 0 but
            # with a different regular expression to kick things off.
            m3 = RE3.match(line.strip())
            if m3:
                # Match. Group, shift and day remain the same, so just
                # reset analysis.
                analysis = '{},{},{},'.format(m0.group(1),m0.group(2),m0.group(3))
                # Go on to next phase.
                phase = 1
                #print("End phase 3")
            continue

##  BUG NOTES
# Script isn't capturing the Groups Properly ... everything is marked as group A
# Scipt doesn't recognize the RE4