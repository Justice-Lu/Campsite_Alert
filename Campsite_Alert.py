import time
import argparse
import datetime

import Campsite_Alert_functions as cf  # Import your functions

# Define argument parser
parser = argparse.ArgumentParser(description="Campsite_Alert monitors recreation.gov for campsite availabilities.")
parser.add_argument('--start_date', required=True, help="Specify the desired start date (YYYY-MM-DD).")
parser.add_argument('--end_date', required=True, help="Specify the desired end date (YYYY-MM-DD).")
parser.add_argument('--park_ids', nargs='+', type=int, required=True,
                    help="List of park IDs. Found at the end of the URL on recreation.gov.")
parser.add_argument('--campsites', nargs='+', help="Optional list of specific campsites to track.")
parser.add_argument('--num_days', type=int, default=1, help="Number of consecutive days required for a valid booking.")
parser.add_argument('--cycle_time', type=float, default=1, help="Time (in minutes) between checks.")
parser.add_argument('--total_time', type=float, default=1, help="Total time (in minutes) before the script exits.")
parser.add_argument('--output_format', choices=['summary', 'table', 'both'], default='both',
                    help="Choose output format: 'summary' for compact info, 'table' for structured data, 'both' for all.")

args = parser.parse_args()

# Start the timer
start_time = time.time()

while True:
    current_time = time.time()
    elapsed_time = round(current_time - start_time, 0)

    # Get park availability data
    websites = cf.get_website_for_parks(args.start_date, args.end_date, args.park_ids, 
                                        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                                                   "Accept": "application/json",
                                                   "Origin": "https://www.recreation.gov"}
                                        )

    park_names = []
    compatible_dates_all_parks = {}

    for park_id in args.park_ids:
        website = websites.get(park_id)
        
        if website == 403:             
            print(f"Skipping {park_id} due to a 403 error. . .")
            continue  # Skip this park and continue with the others
        
        # Extract park name
        park_name = website[list(website.keys())[0]]['loop']
        park_names.append(park_name)
        
        # Process availability
        dates = cf.my_dates(args.start_date, args.end_date)  # Generate the range of dates to check
        available_dates = cf.get_available_dates(website)  # Fetch available dates from the website
        compatible_dates = cf.filter_by_dates(available_dates, dates)  # Filter available dates within range
        compatible_dates = cf.filter_by_campsite(compatible_dates, args.campsites)  # Apply campsite filter
        compatible_dates = {site: compatible_dates[site] for site in sorted(compatible_dates.keys())}  # Sort by campsite

        # Store data
        compatible_dates_all_parks[park_id] = compatible_dates

    # Print output based on selected format
    if args.output_format in ['summary', 'both']:
        output = cf.print_summary(compatible_dates_all_parks, args.start_date, args.end_date, args.park_ids, park_names, args.num_days)
        print(output)

    if args.output_format in ['table', 'both']:
        output = cf.tabulate_results(compatible_dates_all_parks, args.start_date, args.end_date, args.park_ids, park_names, args.num_days)
        print(output)

    # Stop execution if total time limit is reached
    if elapsed_time > args.total_time * 60:
        print(f"Finished iterating in: {int(elapsed_time)} seconds. Script stopped.")
        break

    # Wait before the next cycle
    time.sleep(args.cycle_time * 60 - time.time() % args.cycle_time)