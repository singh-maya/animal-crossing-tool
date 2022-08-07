import numpy as np
import pandas as pandas
import requests as requests
import json
from datetime import datetime
import csv


# Create a GET request on the server, and get the response as a json object
def request_json(https):
    resp = requests.get(https)
    if resp.status_code != 200:
        # This means something went wrong.
        raise Exception('{}: Error {}'.format(https, resp.status_code))

    return resp.json()


def getFishData():
    api_endpoint = 'https://acnhapi.com/v1/{}'
    data = request_json(api_endpoint.format('fish'))
    return data


def getBugData():
    api_endpoint = 'https://acnhapi.com/v1/{}'
    data = request_json(api_endpoint.format('bugs'))
    return data


def printFishData(data, name, hour, month):
    fName = data[name]['name']['name-USen']
    fAvail = data[name]['availability']
    fMonth = np.array(fAvail['month-array-northern'])
    fTimes = np.array(fAvail["time-array"])
    fLocation = np.array(fAvail["location"])

    if month in fMonth:
        canFishMonth = True
    else:
        canFishMonth = False
    if hour in fTimes:
        canFishHour = True
    else:
        canFishHour = False

    if canFishMonth and canFishHour is True:
        print("Can Fish: " + fName)
    elif canFishHour is False:
        print("Not right time, times are listed below: ")
        print(fTimes)
    elif canFishMonth is False:
        print("Not right month, months are listed below: ")
        print(fMonth)
    print("Location: " + fLocation)
    menuSelect()


def printBugData(data, name, hour, month):
    name = data[name]['name']['name-USen']
    avail = data[name]['availability']
    month_array = np.array(avail['month-array-northern'])
    times = np.array(avail["time-array"])
    location = np.array(avail["location"])

    if month in month_array:
        canCatchMonth = True
    else:
        canCatchMonth = False
    if hour in times:
        canCatchHour = True
    else:
        canCatchHour = False

    if canCatchMonth and canCatchHour is True:
        print("Can Catch: " + name)
    elif canCatchHour is False:
        print("Not right time, times are listed below: ")
        print(times)
    elif canCatchMonth is False:
        print("Not right month, months are listed below: ")
        print(month)
    print("Location: " + location)
    menuSelect()


def getAvailableFish(data, hour, month):
    list_name = []
    print("Available Fish in month " + str(month) + " and hour " + str(hour))
    for x in data:
        if hour in data[x]['availability']['time-array'] and month in data[x]['availability']['month-array-northern']:
            list_name.append(data[x]['name']['name-USen'])
    print("Available Fish")
    for x in list_name:
        print(x)
    menuSelect()


def getAvailableBugs(data, hour, month):
    list_name = []
    print("Available Bugs in month " + str(month) + " and hour " + str(hour))
    for x in data:
        if hour in data[x]['availability']['time-array'] and month in data[x]['availability']['month-array-northern']:
            list_name.append(data[x]['name']['name-USen'])
    print("Available Bugs")
    for x in list_name:
        print(x)
    menuSelect()


def checkCSV(fish, bug):
    islandName = input("What is your island name? ")
    while True:
        try:
            file = open(islandName + ".csv", "r")
            break
        except FileNotFoundError:
            createCSV(islandName, fish, bug)
    logCritter(islandName, fish, bug)


def createCSV(name, fish, bug):
    fileName = name + ".csv"
    fish_list = []
    bug_list = []

    for x in fish:
        fish_list.append(fish[x]['name']['name-USen'])
    for y in bug:
        bug_list.append(bug[y]['name']['name-USen'])
    critterList = fish_list + bug_list
    tupleForCSV = []
    for x in critterList:
        tupleForCSV.append((x, "no"))

    header = ['Critter', 'Caught']
    with open(fileName, 'w', encoding='UTF8', newline='') as f:
        csv.register_dialect("custom", delimiter=",", skipinitialspace=True)
        writer = csv.writer(f, dialect="custom")
        writer.writerow(header)
        for tup in tupleForCSV:
            writer.writerow(tup)


def logCritter(file_name, fish, bugs):
    fileName = file_name + ".csv"
    critter = input("What critter do you want to log? ")
    critter = critter.lower()

    # log in critter
    df = pandas.read_csv(fileName, index_col='Critter')
    file = open(fileName)
    found = False
    for row in file:
        if critter in row:
            found = True
    if found is True:
        df.loc[critter, "Caught"] = "yes"
        df.to_csv(fileName)
    else:
        print("Critter not found")
        logCritter(file_name, fish, bugs)

    # check what is left for the month
    currentTime = datetime.now()
    currentMonth = currentTime.month

    critter_list = set()
    for index, row in df.iterrows():
        if df.loc[index, "Caught"] == "no":
            critter_list.add(index)

    result_list_bug = set()
    result_list_fish = set()
    for critter in critter_list:
        for x in bugs:
            if critter in bugs[x]["name"]["name-USen"]:
                if currentMonth in bugs[x]["availability"]["month-array-northern"]:
                    result_list_bug.add(critter)
        for y in fish:
            if critter in fish[y]["name"]["name-USen"]:
                if currentMonth in fish[y]["availability"]["month-array-northern"]:
                    result_list_fish.add(critter)

    print("Critters That Are Left this Month")
    print("-----------------")
    print("Bug")
    for x in result_list_bug:
        print(x)
    print(" ")
    print("-----------------")
    print(" ")
    print("Fish")
    for x in result_list_fish:
        print(x)
    print("-----------------")
    print(" ")

    userInput = input("Do you have more to log? ")
    if userInput == "Y":
        logCritter(file_name, fish, bugs)
    else:
        menuSelect()


def menuSelect():
    print("Welcome to ACNH Helper!")
    print("What would you like to do?")
    print("1. See What Fish To Catch Right Now")
    print("2. See Fish Information")
    print("3. See What Bugs to Catch Right Now")
    print("4. See Bug Information")
    print("5. Update Caught Fish/Bugs and See What is Left")
    print("6. Close")
    selection = input()
    if selection == "1":
        fish_data = getFishData()
        currentTime = datetime.now()
        getAvailableFish(fish_data, currentTime.hour, currentTime.month)
    if selection == "2":
        fish_data = getFishData()
        name = input("Enter fish name: ")
        fish_name = name.lower()
        currentTime = datetime.now()
        printFishData(fish_data, fish_name, currentTime.hour, currentTime.month)
    if selection == "3":
        bug_data = getBugData()
        currentTime = datetime.now()
        getAvailableBugs(bug_data, currentTime.hour, currentTime.month)
    if selection == "4":
        bug_data = getBugData()
        name = input("Enter Bug name: ")
        bug_name = name.lower()
        currentTime = datetime.now()
        printBugData(bug_data, bug_name, currentTime.hour, currentTime.month)
    if selection == "5":
        fish_data = getFishData()
        bug_data = getBugData()
        checkCSV(fish_data, bug_data)


def main():
    menuSelect()


main()




