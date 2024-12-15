README.txt
Instructions for Execution

	1.	Prerequisites:
	•	Ensure Python 3.x is installed.
	•	All the Files are in the same directory
	2.	Running the Script:
	•	Execute the script to process the data and generate reports:
	•	python IDS.py Events.txt Stats.txt 10

                EXAMPLE OUTCOME:
                (base) rohitpanda@Rohits-MBP src % python3 main.py Events.txt Stats.txt 10
                --------------------------------------------------------------------
                Checking for inconsistencies between Events.txt and Stats.txt...
                --------------------------------------------------------------------
                No inconsistencies found


                ------------------------
                Processing Events.txt...
                ------------------------
                Event:Logins, Type:D, Min:0, Max:100, Weight:2
                Event:Time online, Type:C, Min:0.0, Max:1440.0, Weight:3
                Event:Emails sent, Type:D, Min:0, Max:100, Weight:1
                Event:Emails opened, Type:D, Min:0, Max:100, Weight:1
                Event:Emails deleted, Type:D, Min:0, Max:100, Weight:2


                ------------------------
                Processing Stats.txt...
                ------------------------


                Currently generating data for 10 days of events...
                Data set generation completed!

                Currently simulating activity with the data set generated...
                10 days of data has been written to baseline_logs.txt and logs.json!


                Enter filename for new Stats File: Stats_new.txt
                Enter the number of Days: 10
                Currently generating data for 10 days of events...
                Data set generation completed!

                Currently simulating activity with the data set generated...
                10 days of data has been written to anomaly_logs.json and logs.json!

                Threshold: 18
                Day 1 anomaly score = 9.55 
                Day 2 anomaly score = 10.4 
                Day 3 anomaly score = 18.4 --- FLAGGED
                Day 4 anomaly score = 17.25 
                Day 5 anomaly score = 6.0 
                Day 6 anomaly score = 7.56 
                Day 7 anomaly score = 32.15 --- FLAGGED
                Day 8 anomaly score = 12.03 
                Day 9 anomaly score = 20.75 --- FLAGGED
                Day 10 anomaly score = 11.39 

                ALERT! Anomalies detected!
                --------------------------
                Day 3 has been flagged!
                Day 7 has been flagged!
                Day 9 has been flagged!

                Continue to read new Stats file? (y/n): n
                Exiting Alert Engine...

Overview
This repository contains files related to anomaly detection and user activity analysis. 
Below is a description of the files, their purposes, and instructions for execution.
File Descriptions
1. alerts.json

	•	Description: Contains flagged anomaly scores compared to a threshold. Each entry provides the date, anomaly score, threshold, and status (OK or FLAGGED).
	•	Purpose: Tracks potential anomalies in user activity.
	•	Structure:
{
  "date": "YYYY-MM-DD",
  "anomaly_score": <float>,
  "threshold": <int>,
  "status": "FLAGGED/OK"
}

2. analysis_results.json

	•	Description: Provides statistical analysis of user activity data, including logins, time online, emails sent, opened, and deleted.
	•	Purpose: Summarizes activity metrics with total, mean, and standard deviation values.
	•	Structure:
{
  "metric": {
    "total": <float>,
    "mean": <float>,
    "stddev": <float>
  }
}
3. anomaly_logs.json

	•	Description: Logs daily user activity data for comparison against baseline metrics.
	•	Purpose: Tracks deviations in daily behavior to identify anomalies.
	•	Structure:
Day N
Logins:D:<int>:
Time online:C:<float>:
Emails sent:D:<int>:
Emails opened:D:<int>:
Emails deleted:D:<int>:
4. baseline_logs.txt

	•	Description: Contains baseline activity data used for anomaly detection.
	•	Purpose: Serves as a reference to compare daily activity logs.
	•	Structure: Similar to anomaly_logs.json.

5. logs.json

	•	Description: JSON format of daily activity events including logins, time online, and email interactions.
	•	Purpose: Provides structured event data for processing and analysis.
	•	Structure:
{
  "date": "YYYY-MM-DD",
  "events": {
    "logins": <int>,
    "time online": <float>,
    "emails sent": <int>,
    "emails opened": <int>,
    "emails deleted": <int>
  }
}
6. Stats_new.txt

	•	Description: Summarizes key activity statistics.
	•	Structure:
