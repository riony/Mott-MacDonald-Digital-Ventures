# Mott MacDonald Digital Ventures

The code can be run by executing 
" python .\script.py -f accumRainfall.csv -r 5 -p 30 -a 60 "
-
within a suitable python 3.7 environment
the only other file required is that the .csv dataset be in the same folder location as the script

The tags are as follow
-f is the input dataset filename 
-r is the temporal resolution for deaccumulation of the data, this is given in minutes, reccommended to use 1-5 and in whole numbers
-p is the period for which the max rainfall amount is to be found for, in minutes, for the given task it was 30
-a is the period which the data is accumulated for, in minutes, in this task it was 60

The output for the variables in the example above is
-----------------------------------------------------
highest rain fall in 30 minutes:
-
1.0092 inches
-
Time which maximum rainfall occurs:
-
2016-06-16 02:30:00 UTC time
-----------------------------------------------------

Given the magnitude of the hourly measurements it is likely that the units are in inches 
The time generated is in UTC, the local time for the site in Pennsylvania would be 22:30:00, 2016-06-15.

As the code is currently written with individual functions for parsing, deaccumulating and calculation of max values it can be easily extended by adding suitable function for parsing any new databse or types

The script writes to file the extended deaccumulated dataset, if new data is added it can be combined with this processed dataset, however the model might need to be modified to better utilize overlapping data points, such as interpolation or averaging 

As new data is added to this dataset, a second function for calling the current dataset has to be added. The new dataset has to be compared for the timestamps, and the final dataset has to be extended if needed. Care needs to be taken to ensure that the deaccumulated time resolution is the same when adding new datasets. 

