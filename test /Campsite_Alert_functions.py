import pandas as pd 
import numpy as np
import requests 
# import datetime
import re 
import time 
import datetime 
from fake_useragent import UserAgent
import argparse

def get_url(start_date, park_id):
    url_base = "https://www.recreation.gov/api/camps/availability/campground/{park_id}/month?start_date="
    url_date_end = start_date + "T00%3A00%3A00.000Z"
    url = url_base.format(park_id = park_id) + url_date_end
    return url

def get_website(url):
    headers = {"user-agent": UserAgent().random}
    reponse = requests.get(url, headers=headers)
    website = reponse.json()['campsites']
#    website = reponse.json()
    return website

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

# Filters compatible_dates by campsites. return only campsites that are matched 
# IF specified campsite have no reservations, add notification 
def filter_by_campsite(compatible_dates, campsite):
    filterred_compatible_dates = {}
    if campsite == None: 
        return compatible_dates
    for keep_sites in campsite: 
        if keep_sites in compatible_dates:
            filterred_compatible_dates[keep_sites] = compatible_dates[keep_sites]
        else: 
                filterred_compatible_dates[keep_sites] = ["RESERVED"]
    return filterred_compatible_dates
    

# takes in parameters and format a more readable outputs 
def print_results(compatible_dates, start_date, end_date, park_id):
    output = ""
    output += 'From the specified dates of '+start_date+" to "+end_date+" at park_id "+str(park_id)+' \n'
    for campsite in compatible_dates.keys():
        days = ""
        for day in compatible_dates[campsite]:
            if day == "RESERVED": 
                days += '     COMPLETELY RESERVED \n'
                continue
            days += ("     AVAILABLE on "+day+"\n")
        output += 'Campsite '+campsite+ ' status:  \n'+str(days)
    return output







