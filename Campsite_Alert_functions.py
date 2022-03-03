import pandas as pd 
import numpy as np
import requests 
# import datetime
import re 
import time 
import datetime 

import argparse

from tabulate import tabulate


def get_urls(start_date, end_date, park_id):
    """
    Generate a list of URLs for all months between start_date and end_date.
    """
    url_base = "https://www.recreation.gov/api/camps/availability/campground/{park_id}/month?start_date="
    
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    
    urls = []
    current = start.replace(day=1)  # Always start from the 1st of the month
    while current <= end:
        url_date_end = current.strftime("%Y-%m-%d") + "T00%3A00%3A00.000Z"
        url = url_base.format(park_id=park_id) + url_date_end
        urls.append(url)
        # Move to the first day of the next month
        next_month = current.month % 12 + 1
        next_year = current.year if next_month > 1 else current.year + 1
        current = datetime.datetime(next_year, next_month, 1)
    
    return urls


def get_website(urls, headers):
    """
    Fetch and merge availability data from multiple URLs (months).
    """
    merged_data = {}

    for url in urls:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            website_data = response.json().get('campsites', {})
            for site_id, site_info in website_data.items():
                if site_id not in merged_data:
                    merged_data[site_id] = site_info
                else:
                    # Merge availability data for overlapping months
                    merged_data[site_id]['availabilities'].update(site_info['availabilities'])
        else:
            print(f"Error fetching data from {url}: {response.status_code}")
            return response

    return merged_data

def my_dates(start_date, end_date):
    dates = []
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    date_array = (start + datetime.timedelta(days=x) for x in range(0, (end-start).days))
    for date_object in date_array:
        dates.append(date_object.strftime("%Y-%m-%d"))
    return dates

# Create available_dates dict which holds campsite: [dates available]
def get_available_dates(website):
    available_dates = {}
    for campsite in website.keys():
        site_id = website[campsite]['site']
        available_dates[site_id] = [] #assigns actual site_id 
        for day in website[campsite]['availabilities'].keys():
            if website[campsite]['availabilities'][day] == "Available":
                available_dates[site_id].append(re.sub("T00:00:00Z", "", day)) 
        if available_dates[site_id] == []:
            del available_dates[site_id] # removes the campsite that have no available dates 
    return available_dates

# Filters available_dates by the desired dates. 
def filter_by_dates(available_dates, dates):
    compatible_dates = {}
    for site_id in available_dates.keys():              
        temp = [x for x in dates if x in available_dates[site_id]]
        if not temp == []: 
            compatible_dates[site_id] = temp
    return compatible_dates

def filter_by_campsite(compatible_dates, campsites=None):
    """
    Filters the available campsites to return only those specified in the `campsites` list.
    If a specified campsite is not available, it is removed from the list.
    If no campsites remain after filtering, the function terminates the query.
    """
    if campsites is None:
        return compatible_dates  # Return all campsites if no filtering is needed

    # Remove campsites that are not found in compatible_dates
    campsites = [site for site in campsites if site in compatible_dates]

    # If no campsites remain, terminate the query
    if not campsites:
        print("No matching campsites found. Terminating query.")
        return {}  # Return an empty dictionary to indicate termination

    # Filter the results
    filtered_compatible_dates = {
        site: compatible_dates.get(site, ["RESERVED"]) for site in campsites
    }

    return filtered_compatible_dates
    

def print_results(compatible_dates, start_date, end_date, park_id):
    """
    Takes in filtered campsite availability and formats it into a readable output.
    If no compatible campsites are found, it returns a termination message.
    """
    if not compatible_dates:  # Check if compatible_dates is empty
        return f"No available campsites found from {start_date} to {end_date} at park_id {park_id}. Terminating query."

    output = [f"From the specified dates of {start_date} to {end_date} at park_id {park_id}:\n"]
    
    for campsite, days in compatible_dates.items():
        if days == ["RESERVED"]:
            status = "     COMPLETELY RESERVED"
        else:
            status = "\n".join(f"     AVAILABLE on {day}" for day in days)
        
        output.append(f"Campsite {campsite} status:\n{status}")

    return "\n".join(output)


def print_summary(compatible_dates, start_date, end_date, park_ids, park_names, num_days):
    """
    Prints a concise summary of available campsites for multiple parks.
    Displays the park name, queried dates, and the number of available campsites for each date range.
    If no compatible campsites are found, it returns a termination message.
    """
    if not compatible_dates:  # Check if compatible_dates is empty
        return f"\n🚫 No available campsites found from {start_date} to {end_date} at the specified parks. Terminating query.\n"

    # Initialize output for multiple parks
    summary = []
    
    # Convert start_date and end_date to datetime objects for comparison
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    for park_id, park_name in zip(park_ids, park_names):
        # Extract the compatible dates for the current park
        compatible_dates_park = compatible_dates.get(park_id, {})

        # Skip the park if no data
        if not compatible_dates_park:
            continue

        # Create a list of all available dates and convert to datetime.date objects
        all_available_dates = sorted(set(datetime.datetime.strptime(date, "%Y-%m-%d").date() for dates in compatible_dates_park.values() for date in dates))

        # If num_days > 1, group consecutive available dates into sliding date ranges
        grouped_dates = []
        if num_days > 1:
            for i in range(len(all_available_dates) - num_days + 1):
                start = all_available_dates[i]
                end = all_available_dates[i + num_days - 1]
                grouped_dates.append((start, end))
        else:
            grouped_dates = [(date, date) for date in all_available_dates]

        # Count the available campsites for each date range
        available_counts = {}
        for start, end in grouped_dates:
            available_counts[(start, end)] = sum(
                1 for days in compatible_dates_park.values() if any(start <= datetime.datetime.strptime(date, "%Y-%m-%d").date() <= end for date in days)
            )

        # Add park info and availability to the summary
        park_summary = f"🏞️ {park_id:^8d}: {park_name}"
        park_summary += f"\n📅 Dates: {start_date} to {end_date}\n"

        # Add availability for each grouped date range
        for (start, end), count in available_counts.items():
            park_summary += f"On {start} --> {end}: {count} out of {len(compatible_dates_park)} campsites are available.\n"

        summary.append(park_summary)

    # Return all summaries
    return "\n".join(summary)

def tabulate_results(compatible_dates, start_date, end_date, park_ids, park_names, num_days):
    """
    Formats the available campsite data into a tabular format using `tabulate`.
    Campsites are displayed as columns, and dates (or date ranges) as rows.
    If no compatible campsites are found, it returns a termination message.
    """
    if not compatible_dates:  # Check if compatible_dates is empty
        return f"No available campsites found from {start_date} to {end_date} at the specified parks. Terminating query."

    # Convert start_date and end_date to datetime objects for comparison
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    # Initialize the result to store tables for all parks
    result = []

    # Process each park_id and corresponding compatible dates
    for park_id, park_name in zip(park_ids, park_names):
        # Extract the compatible dates for the current park
        compatible_dates_park = compatible_dates.get(park_id, {})
        
        if not compatible_dates_park:  # Skip park if no data
            continue

        # Create a list of all available dates and convert to datetime.date objects
        all_available_dates = sorted(set(datetime.datetime.strptime(date, "%Y-%m-%d").date() for dates in compatible_dates_park.values() for date in dates))

        # If num_days > 1, group consecutive available dates into ranges (sliding windows)
        grouped_dates = []
        if num_days > 1:
            for i in range(len(all_available_dates) - num_days + 1):
                start = all_available_dates[i]
                end = all_available_dates[i + num_days - 1]
                grouped_dates.append((start, end))
        else:
            grouped_dates = [(date, date) for date in all_available_dates]

        # Prepare the headers for the tabular output (camp site IDs)
        headers = ["Dates"] + list(compatible_dates_park.keys())

        # Prepare the rows for each grouped date range
        table = []  # Initialize a table for the current park
        for start, end in grouped_dates:
            row = [f"{start} --> {end}"]  # Start the row with the date range

            # Check availability for each campsite and append to row
            for campsite in compatible_dates_park.keys():
                availability = "A" if any(start <= datetime.datetime.strptime(date, "%Y-%m-%d").date() <= end for date in compatible_dates_park[campsite]) else "x"
                row.append(availability)

            # Add this row to the table
            table.append(row)

        # Add the formatted table for the current park to the result
        result.append(f"🏞️ {park_id:^8d}: {park_name}\n" + tabulate(table, headers=headers, tablefmt="heavy_grid"))

    # Return the concatenated result for all parks
    return "\n\n".join(result)

def get_website_for_parks(start_date, end_date, park_ids, headers):
    """
    Gets campsite availability data for multiple parks at once.
    """
    websites = {}
    for park_id in park_ids:
        url = get_urls(start_date, end_date, park_id)
        website = get_website(url, headers)
        websites[park_id] = website
    return websites


def get_available_dates_for_parks(websites):
    """
    Gets available dates for multiple parks.
    """
    available_dates_for_parks = {}
    for park_id, website in websites.items():
        available_dates_for_parks[park_id] = get_available_dates(website)
    return available_dates_for_parks

def filter_consecutive_days(compatible_dates, num_days):
    """
    Filters the compatible dates to return campsites with at least num_days of consecutive available days.
    """
    if num_days == 1:
        return compatible_dates  # No filtering needed if num_days is 1

    filtered_compatible_dates = {}

    # Iterate through each campsite and check for consecutive dates
    for campsite, dates in compatible_dates.items():
        # Convert date strings to datetime objects
        sorted_dates = sorted([datetime.datetime.strptime(date, "%Y-%m-%d") for date in dates])

        consecutive_streaks = []

        streak = []
        for i in range(len(sorted_dates)):
            if not streak:
                streak.append(sorted_dates[i])
            elif (sorted_dates[i] == streak[-1] + datetime.timedelta(days=1)):  # Check if the next date is consecutive
                streak.append(sorted_dates[i])
            else:
                if len(streak) >= num_days:
                    consecutive_streaks.append(streak)
                streak = [sorted_dates[i]]

        # Check the last streak
        if len(streak) >= num_days:
            consecutive_streaks.append(streak)

        # If there are any valid streaks of consecutive days, keep this campsite
        if consecutive_streaks:
            filtered_compatible_dates[campsite] = consecutive_streaks

    return filtered_compatible_dates
