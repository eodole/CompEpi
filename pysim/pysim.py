#!/usr/bin/python3
# Alberto Maria Segre
#
# Copyright 2021, The University of Iowa.  All rights reserved.
# Permission is hereby given to use and reproduce this software 
# for non-profit educational purposes only.
#
# Usage:
#    psyim.py infile.csv
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
# infectious at end of day when they decrement. Here, we assume an SIS
# model, so when we get to 0, we are reset to -1.
#
import sys
import csv
from datetime import date, datetime
from random import random

LOS = 3  # Expected length of stay, in days.
SUS = -1
EXP = 9
INF = 7
R = {}   # Rooms
P = {}   # Patient status
H = {}   # HCW status

# Returns True if a transmission has occurred based on disease
# characteristics and amount of overlap. The arguments are strings,
# where now is the current event time, leave1 is the time the current
# actor will leave the room, and leave2 is the time the other actor
# will leave room. If last leave time is 0, it means the other actor
# is a patient, and so isn't going anywhere until they are
# discharged..
def transmit(now, leave1, leave2=0):
    if leave2==0:
        overlap = datetime.fromisoformat(leave1) - datetime.fromisoformat(now)
    else:
        overlap = min(datetime.fromisoformat(leave1),datetime.fromisoformat(leave1)) - datetime.fromisoformat(now)
    print(overlap) 
    return(random() < 0.2)

D = None # Current simulation day
pcnt = 0
icnt = 1
days = 0
roster = set()
with open(sys.argv[1], newline='') as infile:
    F = csv.DictReader(infile)
    # rid,hid,duration,itime,otime,idisp,odisp,jtid,jtname
    for row in F:
        # Get intime as date object.
        date=date.fromisoformat(row['itime'].split()[0])
        if D is None or D < date:
            # Do daily updates; decrement each infected agent: there
            # is no recovered state in this simulation, so if you get
            # to 0 just drop HCW and they will be reinstated as -1.
            H = { hid:H[hid]-1 for hid in H.keys() if H[hid] > 1 }
            # Do the same for the patients, but also consider
            # discharging each patient.
            P = { pid:P[pid]-1 for pid in P.keys() if P[pid] > 1 and random() < 1/LOS }

            # Also: seed very first patient in simulation as infected.
            if D is None:
                print("Patient {} is infected.".format(row['rid'])) #Seeds first patient (always same patient) 
                P[int(row['rid'])] = 9

            # Update your date memory.
            D = date
            days = days + 1
            print("Simulating {}".format(row['itime'].split()[0]))

        rid = int(row['rid'])
        hid = int(row['hid'])
        # Update the roster if HCW is new.
        roster.add(hid)
        
        # Do we know anything about this HCW?
        if hid not in H:
            # Assume HCW is uninfected
            H[hid] = -1

        # Do we know anything about this patient?
        if rid not in P:
            # Assume patient is uninfected; add 1 to your patient counter.
            P[rid] = -1
            pcnt = pcnt+1
            
        # Are there other HCWs in the room?
        if rid not in R:
            # Room is empty of other HCWs, add this one
            R[rid] = { hid:row['otime'] }
        else:
            # Filter out any HCWs who have already left.
            R[rid] = { hid:R[rid][hid] for hid in R[rid] if R[rid][hid] >= row['itime'] }
            # Add this hid
            R[rid][hid] = row['otime']
            
        # Now make any infection status changes from this event. We
        # consider two cases; first, if the hid is infected, and,
        # second, if they are susceptible.
        if H[hid] > 0:
            # hid is infected; they can infect the patient or infect
            # other HCWs based on their overlap and if they are
            # susceptible.
            for hcw in R[rid].keys():
                if (hcw not in H or H[hcw] == SUS) and transmit(row['itime'], row['otime'], R[rid][hcw]):
                    # hid infects other hcw.
                    H[hcw] = EXP+1
                    icnt = icnt+1
            if rid in P and P[rid] == SUS and transmit(row['itime'], row['otime']):
                # hid infects patient.
                P[rid] = EXP+1
                icnt = icnt+1
        else:
            # hid is susceptible; they can be infected by the patient
            # or other HCWs if they are infected.
            for hcw in R[rid].keys():
                if hcw in H and 0 < H[hcw] <= EXP and transmit(row['itime'], row['otime'], R[rid][hcw]):
                    # other hcw infects hid.
                    H[hid] = EXP+1
                    icnt = icnt+1
            if rid in P and 0 < P[rid] <= EXP and transmit(row['itime'], row['otime']):
                # patient infects hid.
                H[hid] = EXP+1
                icnt = icnt+1
        #print("State: R {},\n P {},\n H {}".format(R,P,H))
print("Finished: {} simulation days, {} patients, {} HCWs, and {} infections.".format(days, pcnt, len(roster), icnt))
