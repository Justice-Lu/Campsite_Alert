


# Campsite Alert 

Welcome to Campsite Alert. The script simply updates you on the availability of your favorite campsite at your favorite park on [recreation.gov](https://recreation.gov/) on a given schedule. 



## Using Campsite_Alert

Some of the required parameters of the script consists of 

`--start_date --end_date --park_id`

An example to run the code is listed below: 

The given parameters simply state that you're interested in looking for the 
campsite available...

between `2022-03-09` and `2022-03-30` 

at the park `232453` and the specific campsite of `042`.

Continue to refresh the results every `1` minute for `1` hour. 

```bash
python3 Campsite_Alert.py \
    --start_date 2022-03-01 \
    --end_date 2022-03-30 \
    --park_id 232453 \
    --campsite 042 \
    --cycle_time 1 \
    --total_time 1
```

Output

```bash
From the specified dates of 2022-03-01 to 2022-03-30 at park_id 232447 
Campsite 042 status:  
     AVAILABLE on 2022-03-08
     AVAILABLE on 2022-03-09
```

## Park and campsite IDs 
#### --park_id
To find the necessary IDs for the park you're interested in. Simply navigate to through the 
[recreation.gov](https://recreation.gov/)
and find your park of interest. For example, the 
[Upper Pines](https://www.recreation.gov/camping/campgrounds/232447)
shows the url of 
`https://www.recreation.gov/camping/campgrounds/232447`. The park_id is simply the numeric value at the end of the url, which is `232447`. 

#### --campsite
The campsite is simply the designated `Sites` referred to on the chart. 
![Campsite chart](images/Campsite_availability_chart.png)







