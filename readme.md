# To Run:

Please download 'load_db_and_table_data.py' and the json data file.
Check you have installed:
* python3
* python modules such as sqlite3, pandas, numpy
* enter cmd or terminal, switch to directly where the script sits and enter 'python load_db_and_table_data.py'
Note: only checked on MacOS

## Assumptions:
I have assumed certain things for this exercise. This includes:
* The user_engagement engagement_time_msec is the relevant figure for time on site. No user_engagement value in {} == not included (counted as 0 time)
* The events are all valuable
* The unique number of sessions can be a proxy for the active user count (alternately could do by userID by switching strings in the script)
