#create a csv file in the format 

#rid,hid,duration,itime,otime,idisp,odisp,jtid,jtname

import sys
from turtle import st
from importlib_metadata import unique_everseen
import numpy as np
from datetime import date, datetime
import random
import PoissonSampling as ps
import random
import MCClustSampling as ms
import datetime

#Initialize simulation characteristics
initial_id = 0
n_rooms = 7
schedule = []
#input_staffing[x] = [# of staff of that jtype, [mu, sigma, prop] duration params, lambda total visits per hour, lambda unique visits ]
input_staffing = {}
start_date = datetime.datetime(2020,1,1,7,0)
# Set Up for Facility 15

input_staffing[1] = [1, [[4.5,5.5],[0.03,0.75],[.5,.5]], 4,3.5 ] #7
# input_staffing[2] = [3, ]
# input_staffing[3] = [1, ] 
# input_staffing[7] = [2,]
# input_staffing[8] = 1
# input_staffing[11] = 1
# input_staffing[33] = 1

# Set Up for Facility 19

# input_staffing[1] = [14]
# input_staffing[2] = [2]
# input_staffing[3] = [4]
# input_staffing[4] = 2
# input_staffing[5]= 1
# input_staffing[6] = 10 
# input_staffing[7] = [1,]
# input_staffing[8] = 1
# input_staffing[9] = 2
# input_staffing[10 ] = 3
# input_staffing[18] = 1
# input_staffing[20] = 6
# input_staffing[21] = 1
# input_staffing[23] = 1
# input_staffing[26] = 1
# input_staffing[30] = 1
# input_staffing[33] = 1

#Returns a list of numbers that represent the rids and order that they are visited in
def room_order(unique_r,total_r):
    # global n_rooms
    # #Shuffle the rooms randomly 
    # rooms = list(range(0,n_rooms))
    # random.shuffle(rooms)
    visited = []
    #If there is >1 unique room pick from the first 
    #n rooms with replacement to choose the next (total -n) rooms
    if len(unique_r) > 1:
        for i in range(0,total_r):
            idx = random.randint(0, len(unique_r)-1)
            visited.append(unique_r[idx])
    else:
        r = unique_r[0]
        visited = [r] * total_r

    return visited
        
        # first_n_rooms = len(visited)
        # visited = unique_r[0:unique_r]

    #     for i in range(0, total_r-unique_r):
    #         idx = random.randint(0,first_n_rooms-1)
    #         visited.append(visited[idx])
    # #Otherwise repeat the same room 
    # else:
    #     visited = [rooms[0]] * total_r
        
    # return visited
    

#Assign an hid number to the healthcare worker 
def assign_hid():
    global initial_id
    tmp = initial_id
    initial_id = initial_id +1
    return tmp

def assign_visit_dur(staff_info):
    #Initialize Parameters 
    mu = staff_info[1][0]
    sigma = staff_info[1][1]
    prop = staff_info[1][2]
    #Sample mcclust for duration time
    duration = ms.generate_sample(mu,sigma,prop) ## This needs to be fixed ... how
    #otime = itime + datetime.timedelta(seconds=duration)

    return duration

def generate_visits(hid,jtid,staff_info,visited,itime):
    #print(hid,jtid,visited,itime)
    
    durations = []
    synthetic_v = []
    #print(type(visited),visited)
    for i in range(0,len(visited)):
        # itimes.append(random_date(itime))
        durations.append(assign_visit_dur(staff_info))
        #print(visited)
    not_visit_time = (60*60-sum(durations))/len(visited)
    # print(len(visited),not_visit_time)
    itimes = random_date(itime,not_visit_time,len(visited))
    for i in range(0,len(itimes)):
        intime = itimes[i]
        
        dur = durations[i]
        otime = intime + datetime.timedelta(seconds=dur)
        rid = visited[i]
        synthetic_v.append((hid,jtid,rid,dur,str(intime),str(otime)))
    return(synthetic_v)

        
    #itimes = sorted(itimes)## This doesn't work how do i get it to work
    #print(itimes)

def total_visits_shift(lam): #,shift_len):
    #lam = lam per hour
    #shift_len in hours 
    
    # for i in range(0,shift_len):
    total_v= ps.generate_sample(lam)
    return total_v



def random_date(start,not_visit_time,n_visits):
    itimes = []
    for n in range(0,n_visits):
        
        random_date = start + datetime.timedelta(seconds=random.randrange(not_visit_time//10))
        itimes.append(random_date)
        start = start + datetime.timedelta(seconds= not_visit_time)

    return itimes

#print(random_date(start_date, end_date))

#For each job type...
if __name__ == "__main__":
    for jtid in input_staffing.keys():
        staff_info = input_staffing[jtid]
        #Generate n staff...
        for n_staff in range(0,staff_info[0]):
            #Assign hid, n rooms visited 
            hid = assign_hid()
            #unq_v = ps.generate_sample(staff_info[3])
            unq_r = list(range(0,n_rooms))
            random.shuffle(unq_r)
            unq_r = unq_r[0: (ps.generate_sample(staff_info[3])-1) ]
            print(unq_r)
            for h in range(0,12):
                #total_v = total_visits_shift(staff_info[2],12)
                total_v = total_visits_shift(staff_info[2])
                # print(total_v, unq_r)
                if total_v > 0: 
                    visited = room_order(unq_r,total_v)
                else:
                    visited = []
                
                if len(visited) > 0:
                    schedule.append(generate_visits(hid,jtid,staff_info,visited,start_date + datetime.timedelta(hours=h)))
    print(schedule)
                
                #Generate duration using hid, jtid, visits given 
                
                # for visits in range(0,total_v[h]):
                #     itime = random_date(start_date + datetime.timedelta(hours = h))#, start_date + datetime.timedelta(hours=1+h))
                #     schedule.append(assign_visit_dur(hid,jtid, staff_info,visited[visits],itime))
                #     print(schedule[-1])
                # for visits in range(0,total_v[h]):
                #     visited.pop(0)
            
            
            
                #print(visited,visits)
            #     print(itime)
            #schedule.append(assign_visit_dur(hid,jtid, staff_info,visited[i]))
            #print(schedule[-1])
