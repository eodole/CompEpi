#!/bin/bash

facilities="19 21"

for fac in $facilities
do 
    for run in {1..10}
    do
        python3 ./pysim_old.py ./fac"$fac"config.csv 3 ./fac"$fac"_schedule.csv $run >> ./results/population.csv
    done
done