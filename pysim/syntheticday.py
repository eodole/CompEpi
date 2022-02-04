#create a csv file in the format 

#rid,hid,duration,itime,otime,idisp,odisp,jtid,jtname

import sys
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
    duration = ms.generate_sample(mu,sigma,prop) 
    return duration


# Visits are generate in an hourly fashion 
# Where each hour is returned as a list of visit tuples 
# Each tuple represents a healthcare worker visiting a room
# Parameters for each tuple are hid,jtid,duration, intime, outtime 
def generate_visits(hid,jtid,staff_info,visited,itime):
    
    durations = []
    synthetic_v = []
    
    # Generate visit length for each visit in that hour
    for i in range(0,len(visited)):
        durations.append(assign_visit_dur(staff_info))
    
    # Find the amount of time not being used in visits 
    not_visit_time = (60*60-sum(durations))/len(visited)
   
    # Find the itimes using the non_visit time information to 
    # properly space the visits
    itimes = random_date(itime,not_visit_time,len(visited))
    
    #Put everything together and append each tuple to synthetic visits for that hour
    for i in range(0,len(itimes)):
        intime = itimes[i] 
        dur = durations[i]
        otime = intime + datetime.timedelta(seconds=dur)
        rid = visited[i]
        synthetic_v.append((hid,jtid,rid,dur,str(intime),str(otime)))
    return(synthetic_v)

        

def total_visits_shift(lam): 
    #lam = lam per hour
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

if __name__ == "__main__":
    #For each job type...
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
            #Start at hour 0 of the day 
            for h in range(0,12):
                #Find the total num visits made in that hour
                total_v = total_visits_shift(staff_info[2])
                
                #If num rooms are visited then visited == empty
                if total_v > 0: 
                    visited = room_order(unq_r,total_v)
                else:
                    visited = []
                
                #If there are visits made in that hour, generate them 
                if len(visited) > 0:
                    schedule.append(generate_visits(hid,jtid,staff_info,visited,start_date + datetime.timedelta(hours=h)))
    print(schedule)
                
               
            