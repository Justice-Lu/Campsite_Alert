import time 
import pandas as pd 
import numpy as np
import sys
import argparse

import Campsite_Alert_functions as campsite_function 


parser = argparse.ArgumentParser(description = "Campsite_Alert looks for desired parks and campsites on recreation.gov and alert you if there are avaialbilities!")
parser.add_argument('--start_date', 
                    help = "Specify desired start_date. (ex. 2022-02-22)", 
                   required=True)
parser.add_argument('--end_date', 
                    help = "Specify desired start_date. (ex. 2022-02-22)", 
                   required=True)
parser.add_argument('--park_id', 
                    type = int, 
                    help = "park_id can be found at the end of the url. \n (ex. recreation.gov/camping/campgrounds/>>>>232447<<<<<) ", 
                   required=True)
parser.add_argument('--campsite', nargs = '+',
                    help = "Desired specific campsites can be tracked.")
parser.add_argument('--cycle_time',
                    default=1,
                    type = float, 
                    help = "Seconds until results are refreshed")
parser.add_argument('--total_time',
                    default=1,
                    type = float,
                    help = "Total time in minutes until script exits")
args = parser.parse_args()

    


start_time = time.time()

while True:
    current_time = time.time()
    elapsed_time = round(current_time - start_time,0)
    time.sleep(args.cycle_time*60 - time.time() % args.cycle_time*60)
    
#     print('Running, time = ' + str(elapsed_time))

    
    url = campsite_function.get_url(args.start_date[0:8]+"01", args.park_id)    
    website = campsite_function.get_website(url)
    
    dates = campsite_function.my_dates(args.start_date, args.end_date)
    available_dates = campsite_function.get_available_dates(website)
    compatible_dates = campsite_function.filter_by_dates(available_dates, dates)
    compatible_dates = campsite_function.filter_by_campsite(compatible_dates, args.campsite)
    
    output = campsite_function.print_results(compatible_dates, args.start_date, args.end_date, args.park_id)    
    print(output)
        
    if elapsed_time > args.total_time*60*60:
        print("Finished iterating in: " + str(int(elapsed_time))  + " seconds \n script stopped")
        break