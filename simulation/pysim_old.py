#!/usr/bin/python3
# Alberto Maria Segre
#
# Copyright 2021, The University of Iowa.  All rights reserved.
# Permission is hereby given to use and reproduce this software 
# for non-profit educational purposes only.
#
# Usage:
#    psyim.py config n infile.csv
# Assumes input data are sorted by itime, otime. Reports total
# number of hcws, patients, and infections.
#
# Our infection model is quite simple (see Carrat et al, 2008). People
# are exposed for E days (the incubation period), then infected for I
# additional days (the symptomatic period). Individuals are infectious
# as either E or I.  Carrat et al. (2008) indicate E~2 and I~7 for
# influenza.
#
# Recall status[] starts at E+I and counts down to REC=0.
#
# If I=7, E=2:
#   SUS REC                   I    I+E
#     |  |                    |     | 
#    -1  0  1  2  3  4  5  6  7  8  9
#          |===================||====|
#
# New infecteds start at 10 on day of infection and then become
# infectious at end of day when they decrement. Set MODEL=SIS to allow
# for reinfection, else model defaults to SIR.
#
from fileinput import filename
import sys
import csv
from math import ceil, exp
from datetime import date, datetime
from random import random, randint, shuffle
import pandas as pd

LOS = 3  # Expected length of stay, in days.
SUS = -1 # Susceptible
EXP = 9  # Exposed
INF = 7  # Infected
# Shedding factor is an array indexed by status.
SHD = [0, 0.1, 0.1, 0.15, 0.2, 0.5, 0.7, 1, 0.5, 0.2, 0]

SIS = -1
SIR = 0
MODEL = SIR

R = {}   # Rooms and who is currently in them
P = {}   # Patients currently in hospital, with their current status
S = []   # HCW rosters by day of week 0-6
W = {}   # HCW information, including job type and schedule, by wid

######################################################################
# Returns True if a transmission has occurred based on disease
# characteristics and amount of overlap. The arguments are strings,
# where now is the current event time, leave1 is the time the current
# actor will leave the room, and leave2 is the time the other actor
# will leave room. If last leave time is 0, it means the other actor
# is a patient, and so isn't going anywhere until they are
# discharged.
#
# Add a parameter that takes the day of the shedder's infection to
# modify transmission probability.
#
def transmit(now, leave1, leave2, infectivity):
    # Compute overlap in minutes.
    if leave2==0:
        overlap = (datetime.fromisoformat(leave1) - datetime.fromisoformat(now)).total_seconds()/60
    else:
        overlap = (min(datetime.fromisoformat(leave1),datetime.fromisoformat(leave1)) - datetime.fromisoformat(now)).total_seconds()/60
    # Need to attenuate by day of infection for shedding element.
    # Transmission formula of 1-e^-0.2t peaks at .99 at t=23min    
    return(random() < 1-exp(SHD[infectivity]*(-0.2)*overlap))

######################################################################
# Creates a weekly schedule that can be repeated to staff a
# hospital. Number of shifts per week given as dayson. Without
# randomization, an attempt is made to reduce number of part timers.
def schedule(cover, dayson=3, randomize=False):
    # How many people do you need?
    N = ceil(7*cover/dayson)
    # Create proto schedule.
    L=[1]*dayson + [0]*(7-dayson)
    # Randomize days off by shuffling.
    if randomize:
        shuffle(L)
    # Create N shifted versions of the proto schedule.
    S=[ cls(list(L), (i*2)%len(L)) for i in range(N) ]
    # Ensure even coverage.
    c = coverage(S)
    while min(c) < cover:
        # Find an understaffed day.
        i = c.index(min(c))
        # Find overstaffed days
        overstaffed = [ j for j in range(len(c)) if c[j] > cover ]
        for s in S:
            overage = [ j for j in overstaffed if s[j]==1 ]
            if s[i] == 0 and overage:
                s[i] += 1
                s[overage[0]] -= 1
                break
        c = coverage(S)
    # Drop extra shifts.
    while max(c) > cover:
        # Find an overstaffed day.
        i = c.index(max(c))
        # Preference is to create a designated part-time employee
        for s in sorted(S, key=lambda x: sum(x)):
            if s[i] == 1:
                s[i] = 0
                break
        c = coverage(S)
    # Done.
    shuffle(S)
    return(S)

# Circular left shift.
def cls(L, i):
    L[len(L):] = L[:i]
    L[:i] = []
    return(L)

# Computed coverage for schedule S.
def coverage(S):
    C=[0]*7
    for s in S:
        for d in range(len(s)):
            if s[d]==1:
                C[d] = C[d]+1 
    return(C)

######################################################################
######################################################################
# Start processing here. Invoke as:
#   pysim.py config nwk data.csv run_num
if len(sys.argv) != 5:
    print("Usage: pysim.py config week data.csv")
    print("where: config is name of staff configuration file")
    print("       week is number of shifts per week")
    print("       data.csv file containing HCW events")
    print("       run_num is the number run of experiment you are on.")   
    exit()
nwk = int(sys.argv[2])
run_num = int(sys.argv[4]) 
fac = sys.argv[3].split(sep="_")[0]


######################################################################
######################################################################
# Setup staff. Staffing levels are specified in the config file.  To
# meet these daily staff needs, we will require a greater number of
# workers, working specific schedules. These will be entries in the W
# dictionary, containing jtid and schedule for each of the workers.
# Workers are on an nwk-day-per-week schedule (typically, 3).
#
# In addition, we'll need to set up a 7-day mapping from hid to wid in
# S (schedule). Each sublist of S is an ordered list of wids
# corresponding to the (sequential) hids in the original data, so
# S[day][hid] => wid.
W = {}
S = [ list() for i in range(7) ]
with open(sys.argv[1], newline='') as cfile:
    # Reads jtid,n
    F = csv.DictReader(cfile)
    wid = 0
    for spec in F:
        # Assumes 3 12-hour shifts per week
        sched = schedule(int(spec['n']), dayson=nwk)
        #print("Coverage for jtid {} is {}".format(spec['jtid'], coverage(sched)))
        for s in sched:
            W[wid] = { 'jtid':int(spec['jtid']), 'schedule':s, 'state':-1 }
            for i in range(7):
                if s[i]==1:
                    # OK, wid is working on day i.
                    S[i].append(wid)
            wid = wid + 1

# Show state
#print("Schedules:")
#for i in W.keys():
#    print(" HCW {} jtid={}: {}".format(i, W[i]['jtid'], W[i]['schedule'])) 
#print("Rosters:")
#for i in range(len(S)):
#    print(" Day {}: {}".format(i, S[i])) 

######################################################################
# Now start the simulation.
pcnt = 0  # Number of patients
pinf = 0  # Number of current patient infections
hinf = 0  # Number of current HCW infections
results = []
#pinf_total = 0 # Number of total patient infections 
#hinf_total = 0 # Number of total HCW infections

# Read in each observation and process them one at a time.
D = None # Current simulation date
with open(sys.argv[3], newline='') as infile:
    # hid,jtid,rid,duration,itime,otime
    F = csv.DictReader(infile)

    for observation in F:
        # Current observation's location, or rid.
        rid = int(observation['rid'])

        # Get itime as date object.
        date=date.fromisoformat(observation['itime'].split()[0])
        # A brand new day!
        if D is None or D < date:
            # Do daily updates; decrement each infected HCW until you
            # get to whichever MODEL is operative.
            for wid in W.keys():
                if W[wid]['state'] > MODEL:
                    W[wid]['state'] = W[wid]['state']-1

            # Also: seed very first patient in simulation as
            # infected. Start counting simulation days.
            if D is None:
                #print("Patient in room {} is infected.".format(observation['rid']))
                P[rid] = INF	# Start at symptoms.
                day = 1
            else:
                day = day+1

            # Decrement any infected patient, but also consider
            # discharging them as long as they are no longer ill.  If
            # they're not in P, they've gone home.
            old = set(P.keys())
            P = { pid:(P[pid]-1) for pid in P.keys() if (P[pid] > 0 or random() > 1/LOS) }
            
            # Update your date memory.
            D = date
            # Set your HCW roster
            roster = S[(day-1)%7]

            # Print out the daily infection report: how many workers
            # (both here and off-shift) and how many patients are
            # currently infected.
            # print("\nSimulating {}: {} HCW, {} patient(s) infected.".format(observation['itime'].split()[0],
                                                                        #   len([wid for wid in W.keys() if W[wid]['state'] > MODEL]),
                                                                        #   len([rid for rid in P if P[rid] > MODEL])), "\nDaily totals: {} HCWs, {} Patients".format(hinf, pinf))
            results.append([fac,run_num,observation['itime'].split()[0],pinf, hinf])
            #print("Day {} staff roster [{}]: {}".format(day, len(roster), roster))
        # Turn on vacancies printing here
            # if old-set(P.keys()):
            #     print("Day {} vacancies: {}".format(day, list(old-set(P.keys()))))

        # Do we know anything about this room? Does it have a patient?
        if rid not in P:
            # Assume newly admitted patient is uninfected; add 1 to
            # your patient counter.
            P[rid] = -1
            pcnt = pcnt+1
            
        # Current observation's hid's equivalent wid (correct for 0-indexing).
        #print("Observation r{} h{}=>w{}".format(observation['rid'],observation['hid'],wid))
        wid = roster[int(observation['hid'])-1] 

        # Are there other HCWs in the room?
        if rid not in R:
            # Room is empty of other HCWs, add this one
            R[rid] = { wid:observation['otime'] }
        else:
            # Room is occupied: filter out HCWs who have already left.
            R[rid] = { wid:R[rid][wid] for wid in R[rid] if R[rid][wid] >= observation['itime'] }
            # Add this new HCW by wid
            R[rid][wid] = observation['otime']

        # Now make any infection status changes from this event. We
        # consider two cases; first, if the wid is infected, and,
        # second, if they are susceptible. Note we check the upper
        # bound against EXP to prohibit single-cycle transmission.
        if 0 < W[wid]['state'] <= EXP:
            # HCW is infected: do they infect other susceptible HCWs in Room rid?
            for hcw in R[rid].keys():
                # R[rid][hcw] is hcw's otime from room rid.
                if W[hcw]['state'] == SUS and transmit(observation['itime'], observation['otime'], R[rid][hcw], W[hcw]['state']):
                    # wid infects other hcw.
                    W[hcw]['state'] = EXP+1
                    hinf = hinf+1
                    #print("Day {}: HCW {} infected by HCW {}: {}".format(day, hcw, wid, W[hcw]))
            # HCW is infected: do they infect a susceptible patient?
            if rid in P and P[rid] == SUS and transmit(observation['itime'], observation['otime'], 0, W[hcw]['state']):
                # wid infects patient.
                P[rid] = EXP+1
                pinf = pinf+1
                #print("Day {}: Patient in room {} infected by HCW {}: {}".format(day, rid, wid, P[rid]))
        elif W[wid]['state'] == SUS:
            # HCW is susceptible; are they infected by some other infected HCW?
            for hcw in R[rid].keys():
                if 0 < W[hcw]['state'] <= EXP and transmit(observation['itime'], observation['otime'], R[rid][hcw], W[wid]['state']):
                    # other hcw infects wid.
                    W[wid]['state'] = EXP+1
                    hinf = hinf+1
                    #print("Day {}: HCW {} infected by HCW {}: {}".format(day, wid, hcw, W[wid]))
            # HCW is susceptible; are they infected by infected patient?
            if rid in P and 0 < P[rid] <= EXP and transmit(observation['itime'], observation['otime'], 0, P[rid]):
                # patient infects hid.
                W[wid]['state'] = EXP+1
                #print("Day {}: HCW {} infected by patient {}: {}".format(day, wid, rid, W[wid]))
                hinf = hinf+1
                
#print("Finished: {} day(s): patients {}/{} [{}%]; HCWs {}/{} [{}%].".format(day, pinf, pcnt, 100*pinf//pcnt, hinf, len(W), 100*hinf//len(W)))
print(f"{fac},{run_num},{len(W)},{pcnt},")
results_df = pd.DataFrame(results, columns=['facility','run','sim_day', 'pat_inf','hcws_inf'])
filename = f"{fac}_r{run_num}.csv"
#filename = "test.csv"
results_df.to_csv(f"./results/{filename}")