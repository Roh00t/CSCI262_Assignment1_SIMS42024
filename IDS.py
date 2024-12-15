import json
import os
import sys
import time
import statistics as s
from datetime import datetime, timedelta

def userInput():
    """Validate command line arguments"""
    if len(sys.argv) != 4:
        print("Usage: python main.py <Events.txt> <Stats.txt> <Days>")
        exit(1)

    eventFile = sys.argv[1]
    statsFile = sys.argv[2]
    
    try:
        days = int(sys.argv[3])
    except ValueError:
        print("Days must be an integer.")
        exit(1)

    if not os.path.exists(eventFile):
        print(f"Error: {eventFile} does not exist.")
        exit(1)

    if not os.path.exists(statsFile):
        print(f"Error: {statsFile} does not exist.")
        exit(1)

    if days <= 0:
        print("Days must be greater than 0.")
        exit(1)

    return eventFile, statsFile, days

def readEvents(filename):
    """Read and parse Events.txt"""
    with open(filename, "r") as fin:
        lines = [line.strip() for line in fin.readlines()]
    return lines

def readStats(filename):
    """Read and parse Stats.txt"""
    with open(filename, "r") as fin:
        lines = [line.strip() for line in fin.readlines()]
    return lines

def consistencyCheck(eventData, statsData):
    """Check consistency between Events.txt and Stats.txt"""
    noOfEventData = int(eventData[0])
    noOfStatsData = int(statsData[0])
    
    if noOfEventData != noOfStatsData:
        print("Number of data is inconsistent")
        return False
        
    for i in range(1, noOfEventData):
        if eventData[i].split(":")[0] != statsData[i].split(":")[0]:
            print(f"Inconsistencies found in line {i + 1}")
            return False
            
    print("No inconsistencies found")
    return True

def processEvents(data):
    """Process and validate event data"""
    noOfEvents = int(data[0])
    allWeight = []
    event_info = {}  # Store event information for JSON output
    
    for i in range(1, noOfEvents + 1):
        each = data[i].split(":")
        eventName = each[0]
        eventType = each[1]
        minimum = each[2]
        maximum = each[3]
        weight = each[4]

        # Validation checks
        if eventType not in ['C', 'D']:
            print("Event type must be either C or D")
            return None
        if not all([minimum, maximum, weight]):
            print("Values cannot be empty")
            return None
        if '.' in weight:
            print("Weight values must be an integer")
            return None
        if eventType == 'D' and any('.' in x for x in [minimum, maximum]):
            print("Float found in a Discrete Event")
            return None

        # Format values
        if eventType == 'C':
            minimum = float(minimum)
            maximum = float(maximum)
        else:
            minimum = int(minimum)
            maximum = int(maximum)

        allWeight.append(int(weight))
        event_info[eventName] = {
            'type': eventType,
            'min': minimum,
            'max': maximum,
            'weight': int(weight)
        }
        
        print(f"Event:{eventName}, Type:{eventType}, Min:{minimum}, Max:{maximum}, Weight:{weight}")
    
    return allWeight, event_info

def generateDataSet(days, eventData, statsData):
    """Generate dataset based on statistical parameters"""
    print(f"Currently generating data for {days} days of events...")
    noOfEvents = int(eventData[0])
    activityData = []
    
    for i in range(days):
        for j in range(1, noOfEvents + 1):
            eData = eventData[j].split(":")
            eventName = eData[0]
            eventType = eData[1]
            minimum = float(eData[2])
            maximum = float(eData[3])
            
            sData = statsData[j].split(":")
            mean = float(sData[1])
            standardDeviation = float(sData[2])
            
            dataSet = generateData(mean, standardDeviation, days, minimum, maximum, eventType)
            activityData.append(dataSet)
            
    print("Data set generation completed!")
    return activityData

def generateData(mean, standardDeviation, days, minimum, maximum, eventType):
    """Generate random data following statistical distribution"""
    while True:
        n = s.NormalDist(mu=mean, sigma=standardDeviation)
        samples = n.samples(days)
        
        for index in range(len(samples)):
            if eventType == "D":
                samples[index] = round(samples[index])
            else:
                samples[index] = round(samples[index], 2)
                
            if samples[index] < minimum or samples[index] > maximum:
                continue
                
        if days >= 10:
            if not (0.95 * mean <= s.mean(samples) <= 1.05 * mean and 
                   0.95 * standardDeviation <= s.stdev(samples) <= 1.05 * standardDeviation):
                continue
        else:
            if not (0.9 * mean <= s.mean(samples) <= 1.1 * mean and 
                   0.9 * standardDeviation <= s.stdev(samples) <= 1.1 * standardDeviation):
                continue
                
        return samples

def simulateActivity(filename, days, eventData, dataSet):
    """Simulate and record activity data"""
    print(f"\nCurrently simulating activity with the data set generated...")
    noOfEvents = int(eventData[0])
    logs_data = []  # Store logs for JSON output
    
    with open(filename, "w") as fout:
        for i in range(days):
            day_data = {
                "date": (datetime(2024, 11, 24) + timedelta(days=i)).strftime("%Y-%m-%d"),
                "events": {}
            }
            
            fout.write(f"Day {i + 1}\n")
            fout.write(f"{noOfEvents}\n")
            
            for j in range(noOfEvents):
                data = eventData[j + 1].split(":")
                eventName = data[0]
                eventType = data[1]
                value = dataSet[j][i]
                
                fout.write(f"{eventName}:{eventType}:{value}:\n")
                day_data["events"][eventName.lower()] = value
                
            fout.write("\n")
            logs_data.append(day_data)
            
    # Write logs to JSON
    with open('logs.json', 'w') as f:
        json.dump(logs_data, f, indent=2)
        
    print(f"{days} days of data has been written to {filename} and logs.json!")

def calculateAnalysisResults(data, eventName):
    """Calculate statistical analysis results"""
    mean = []
    stddev = []
    results = {}
    
    for index, values in enumerate(data):
        mean.append(round(sum(values) / len(values), 2))
        variance = sum((x - mean[-1]) ** 2 for x in values) / len(values)
        stddev.append(round(variance ** 0.5, 2))
        
        results[eventName[index].lower()] = {
            "total": round(sum(values), 2),
            "mean": mean[-1],
            "stddev": stddev[-1]
        }
    
    # Write analysis results to JSON
    with open('analysis_results.json', 'w') as f:
        json.dump(results, f, indent=2)
        
    return mean, stddev

def anomalyDetection(filename, weight, mean, stddev):
    """Detect anomalies in the data"""
    threshold = sum(weight) * 2
    daily_scores = []
    dates = []
    
    with open(filename, 'r') as fin:
        while True:
            day_line = fin.readline().strip()
            if not day_line:
                break
                
            day_num = int(day_line.split()[1])
            dates.append((datetime(2024, 11, 24) + timedelta(days=day_num-1)).strftime("%Y-%m-%d"))
            
            num_events = int(fin.readline().strip())
            daily_score = 0
            
            for i in range(num_events):
                line = fin.readline().strip()
                value = float(line.split(':')[2])
                z_score = abs(value - mean[i]) / stddev[i]
                daily_score += z_score * weight[i]
                
            daily_scores.append(round(daily_score, 2))
            fin.readline()  # Skip empty line
            
    # Generate alerts JSON
    alerts = []
    for i, score in enumerate(daily_scores):
        alerts.append({
            "date": dates[i],
            "anomaly_score": score,
            "threshold": threshold,
            "status": "FLAGGED" if score > threshold else "OK"
        })
        
    with open('alerts.json', 'w') as f:
        json.dump(alerts, f, indent=2)
        
    return daily_scores, threshold

def main():
    # Initial Input and Validation
    eventFile, statsFile, days = userInput()
    eventData = readEvents(eventFile)
    statsData = readStats(statsFile)
    
    print("--------------------------------------------------------------------")
    print(f"Checking for inconsistencies between {eventFile} and {statsFile}...")
    print("--------------------------------------------------------------------")
    if not consistencyCheck(eventData, statsData):
        exit()
    print("\n")
    
    print("------------------------")
    print(f"Processing {eventFile}...")
    print("------------------------")
    result = processEvents(eventData)
    if result is None:
        exit()
    allWeight, event_info = result
    print("\n")
    
    print("------------------------")
    print(f"Processing {statsFile}...")
    print("------------------------")
    # Store event names for later use
    eventNames = [line.split(':')[0] for line in eventData[1:int(eventData[0])+1]]
    print("\n")

    # Activity Engine and Logs
    dataSet = generateDataSet(days, eventData, statsData)
    simulateActivity("baseline_logs.txt", days, eventData, dataSet)
    print("\n")

    # Analysis Engine
    data = [[] for _ in range(int(eventData[0]))]
    with open("baseline_logs.txt", 'r') as f:
        while True:
            day = f.readline()
            if not day:
                break
            num_events = int(f.readline())
            for i in range(num_events):
                value = float(f.readline().split(':')[2])
                data[i].append(value)
            f.readline()  # Skip empty line
    
    mean, stddev = calculateAnalysisResults(data, eventNames)

    # Alert Engine
    while True:
        newStatsFile = input("Enter filename for new Stats File: ")
        if not os.path.exists(newStatsFile):
            print("File does not exist. Please try again.")
            continue
            
        newDays = int(input("Enter the number of Days: "))
        newStatsData = readStats(newStatsFile)
        
        # Generate new dataset and logs
        newDataSet = generateDataSet(newDays, eventData, newStatsData)
        newLogsFile = "anomaly_logs.json"
        simulateActivity(newLogsFile, newDays, eventData, newDataSet)
        
        # Perform anomaly detection
        daily_scores, threshold = anomalyDetection(newLogsFile, allWeight, mean, stddev)
        
        # Print results
        print(f"\nThreshold: {threshold}")
        flagged_days = []
        for i, score in enumerate(daily_scores):
            status = "--- FLAGGED" if score > threshold else ""
            print(f"Day {i + 1} anomaly score = {score} {status}")
            if status:
                flagged_days.append(i + 1)
                
        if flagged_days:
            print("\nALERT! Anomalies detected!")
            print("--------------------------")
            for day in flagged_days:
                print(f"Day {day} has been flagged!")
        else:
            print("\nNo anomalies detected!")
            
        option = input("\nContinue to read new Stats file? (y/n): ")
        if option.lower() != 'y':
            break
            
    print("Exiting Alert Engine...")

if __name__ == "__main__":
    main()