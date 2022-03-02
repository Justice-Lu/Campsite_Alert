{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "6ae23eec",
   "metadata": {},
   "outputs": [],
   "source": [
    "import time \n",
    "import pandas as pd \n",
    "import numpy as np\n",
    "import sys\n",
    "import argparse\n",
    "import importlib\n",
    "\n",
    "import campsite_alert_functions as campsite_function "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 107,
   "id": "1aefa22d",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<module 'campsite_alert_functions' from '/Users/justice/Documents/github_site/Campsite_finder/campsite_alert_functions.py'>"
      ]
     },
     "execution_count": 107,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "importlib.reload(campsite_function)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 53,
   "id": "0958f842",
   "metadata": {},
   "outputs": [],
   "source": [
    "start_date = \"2022-03-01\"\n",
    "end_date = \"2022-03-10\"\n",
    "park_id = 232447\n",
    "campsite = ['047']\n",
    "cycle_time = 1\n",
    "total_time = 1"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 57,
   "id": "ad1ba050",
   "metadata": {},
   "outputs": [],
   "source": [
    "campsite = None"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 108,
   "id": "f1418074",
   "metadata": {
    "scrolled": false
   },
   "outputs": [
    {
     "ename": "KeyboardInterrupt",
     "evalue": "",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mKeyboardInterrupt\u001b[0m                         Traceback (most recent call last)",
      "\u001b[0;32m/var/folders/zp/w4fqjghj3gs6mj6hwys2hsvc0000gn/T/ipykernel_39612/2726558053.py\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m      4\u001b[0m     \u001b[0mcurrent_time\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mtime\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mtime\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m     \u001b[0melapsed_time\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mround\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mcurrent_time\u001b[0m \u001b[0;34m-\u001b[0m \u001b[0mstart_time\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;36m0\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 6\u001b[0;31m     \u001b[0mtime\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0msleep\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mcycle_time\u001b[0m \u001b[0;34m-\u001b[0m \u001b[0mtime\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mtime\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m \u001b[0;34m%\u001b[0m \u001b[0mcycle_time\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      7\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      8\u001b[0m     \u001b[0;31m#inputs start_date at day 01 as that's the format that recreational.gov accepts. Filter dates lateron\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;31mKeyboardInterrupt\u001b[0m: "
     ]
    }
   ],
   "source": [
    "start_time = time.time()\n",
    "\n",
    "while True:\n",
    "    current_time = time.time()\n",
    "    elapsed_time = round(current_time - start_time,0)\n",
    "    time.sleep(cycle_time - time.time() % cycle_time)\n",
    "\n",
    "    #inputs start_date at day 01 as that's the format that recreational.gov accepts. Filter dates lateron\n",
    "    url = campsite_function.get_url(start_date, park_id)\n",
    "    dates = campsite_function.my_dates(start_date[0:8]+\"01\", end_date) \n",
    "    website = campsite_function.get_website(url)\n",
    "    available_dates = campsite_function.get_available_dates(website)\n",
    "    compatible_dates = campsite_function.filter_by_dates(available_dates, dates)\n",
    "    compatible_dates = campsite_function.filter_by_campsite(available_dates, campsite)\n",
    "    \n",
    "    output = campsite_function.print_results(compatible_dates, start_date, end_date, park_id)    \n",
    "    print(output)\n",
    "    \n",
    "    \n",
    "    if elapsed_time > total_time*60:\n",
    "        print(\"Finished iterating in: \" + str(int(elapsed_time))  + \" seconds \\n script stopped\")\n",
    "        break"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "200c709f",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8207fb67",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "692a6285",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "aa7c6a13",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ad77dbb3",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "616e2850",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
