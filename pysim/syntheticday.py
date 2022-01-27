#create a csv file in the format 

#rid,hid,duration,itime,otime,idisp,odisp,jtid,jtname

import sys
from importlib_metadata import unique_everseen
import numpy as np
from datetime import datetime
import random
import PoissonSampling as ps
import random
import MCClustSampling as ms

#Initialize simulation characteristics
initial_id = 0
n_rooms = 7
schedule = []
#input_staffing[x] = [# of staff of that jtype, lamdba duration, lambda total visits per hour, lambda unique visits ]
input_staffing = {}
input_staffing[1] = [2, [[4.4,5.1],[.0007, .008],[.4,.6]], 1.5, 4]
# input_staffing[2] = [1,5,1.5,4]
# input_staffing[3] = [1, 7,2,4] 
# input_staffing[4] = [1,8,2.5,4] 

#Returns a list of numbers that represent the rids and order that they are visited in
def room_order(unique_r,total_r):
    global n_rooms
    #Shuffle the rooms randomly 
    rooms = list(range(0,n_rooms))
    random.shuffle(rooms)
    
    #If there is >1 unique room pick from the first 
    #n rooms with replacement to choose the next (total -n) rooms
    if unique_r > 1:

        visited = rooms[0:unique_r]
        first_n_rooms = len(visited)
        #print(first_n_rooms)
        for i in range(0, total_r-unique_r):
            idx = random.randint(0,first_n_rooms)
            visited.append(visited[idx])
    #Otherwise repeat the same room 
    else:
        visited = [rooms[0]] * total_r
        
    return visited
    

#Assign an hid number to the healthcare worker 
def assign_hid():
    global initial_id
    tmp = initial_id
    initial_id = initial_id +1
    return tmp

def assign_visit_dur(hid, jtid,staff_info, rid):
    #Initialize Parameters 
    mu = staff_info[1][0]
    sigma = staff_info[1][1]
    prop = staff_info[1][2]
    #Sample mcclust for duration time
    duration = ms.generate_sample(mu,sigma,prop) ## This needs to be fixed 

    return [hid, jtid, rid, duration]

def total_visits_shift(lam,shift_len):
    #lam = lam per hour
    #shift_len in hours 
    total_v = 0
    for i in range(0,shift_len):
        total_v = total_v + ps.generate_sample(lam)
    return total_v



#For each job type...
for jtid in input_staffing.keys():
    staff_info = input_staffing[jtid]
    #Generate n staff...
    for n_staff in range(0,staff_info[0]):
        #Assign hid, n rooms visited 
        hid = assign_hid()
        unq_v = ps.generate_sample(staff_info[3])
        total_v = total_visits_shift(staff_info[2],8)
        visited = room_order(unq_v,total_v)
        #visited = room_order(1,total_v)
        for i in range(0,len(visited)):
            #Generate duration using hid, jtid, visits given 
            schedule.append(assign_visit_dur(hid,jtid, staff_info,visited[i]))
            print(schedule[-1])

#For each healthcare worker
# Sum up the time that they're spending patient rooms,      
        



# #Establish the number of patient rooms being simulated
# n_pat_rooms = int(sys.argv[1])
# #Establist num of hcw being simulated 
# nhid = int(sys.argv[2]) 

# begin_date =  datetime.strptime(sys.argv[3], "%Y/%M/%d") 

# print(n_pat_rooms, nhid, begin_date)

# rid = np.arange(1,n_pat_rooms)
# hid = np.arange(100,100+nhid)



# #Create large csv file 
# col_names = ['rid','hid','duration']  #["rid,hid,duration,itime,otime,idisp,odisp,jtid,jtname"]
# output_csv = pd.DataFrame(columns=col_names)

# def generate_row():
#     global rid
#     global hid
#     r1 = random.randint(0,len(rid)-1)
#     r2 = random.randint(0,len(hid)-1)
#     d1 = generate_sample(1.1) #### Needs to be changed to generate a sample from mclust
#     return {'rid':rid[r1], 'hid': hid[r2],'duration': d1 }


# h = 0 
# for hour in range(0,24):
#     for i in range(0,generate_sample(1.1)): ## Need to generate the Poi num of visits
         
#         output_csv = output_csv.append(generate_row(), ignore_index=True)
#     #Take each healthcare worker
#     #Calculate how many time they visit rooms
#     #randomly select room to visit
#     #Caluclate duration of vist
#     #Add row to data table 

# print(output_csv)
