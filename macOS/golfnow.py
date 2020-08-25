import urllib.request
import requests
from bs4 import BeautifulSoup
import json
import os
import argparse
from tabulate import tabulate
import random
from datetime import datetime, date, time, timedelta


def main():
    filename = 'settings.json'
    with open(filename, 'r+') as f:
        courselist = json.load(f)

    parser = argparse.ArgumentParser()
    parser.add_argument('-C', '--config', action='store_true')
    parser.add_argument('-E', '--enable')
    parser.add_argument('-D', '--disable')
    parser.add_argument('-P', '--players', help='Set number of players')
    args = parser.parse_args()

    if args.config:
        print('\n-- SETTINGS --')
        table1 = []
        for (key, val) in courselist['settings'].items():
            table1.append([key, val])
        print(tabulate(table1))

        print('\n-- NEW SOURCES --')
        table2 = []
        headers = ["Course", "ID", "Enabled?"]
        for course in courselist['sources']:
            if courselist['sources'][course]['enabled'] == 0:
                table2.append(
                    [courselist['sources'][course]['name'], courselist['sources'][course]['id'], "Disabled"])
            else:
                table2.append(
                    [courselist['sources'][course]['name'], courselist['sources'][course]['id'], "Enabled"])
        print(tabulate(table2, headers=headers))

    elif args.enable:
        if args.enable == "all":
            for course in courselist['sources']:
                courselist['sources'][course]['enabled'] = 1
            print("All courses have been enabled.")
        elif args.enable == "pcc":
            for course in courselist['sources']:
                if courselist['sources'][course]['pcc'] == 1:
                    courselist['sources'][course]['enabled'] = 1
            print("All PCC courses have been enabled.")
        else:
            try:
                courselist['sources'][args.enable]['enabled'] = 1
                print(courselist['sources'][args.enable]
                      ['name'], "has been enabled.")
            except:
                print(args.enable + "is not on course list.")

    elif args.disable:
        if args.disable == "all":
            for course in courselist['sources']:
                courselist['sources'][course]['enabled'] = 0
            print("All courses have been disabled.")
        elif args.disable == "pcc":
            for course in courselist['sources']:
                if courselist['sources'][course]['pcc'] == 1:
                    courselist['sources'][course]['enabled'] = 0
            print("All PCC courses have been disabled.")
        else:
            try:
                courselist['sources'][args.disable]['enabled'] = 0
                print(courselist['sources'][args.disable]
                      ['name'], "has been disabled.")
            except:
                print(args.disable + "is not on course list")
    elif args.players:
        courselist['settings']['Players'] = int(args.players)
        print('Number of players set to %s' % args.players)
    else:
        # Begin Parsing
        # Start with all that require beaufitul soup
        teeTimes = {}
        teetimeinfo = []
        keys = []
        timesArray = []
        playersArray = []
        num = 0
        errmsg = ""

        inp = input(
            "\nEnter 1 for today, 2 for tomorrow, or any day after following the format yyyy-mm-dd. If months or days are single digit, do not enter a 0.\n")
        for course in courselist['sources']:
            if courselist['sources'][course]['soup'] == 1 and courselist['sources'][course]['enabled'] == 1:

                # get todays date
                today = datetime.today().strftime('%Y-%m-%d')
                tomorrow = datetime.today() + timedelta(days=1)
                tomorrow = tomorrow.strftime('%Y-%m-%d')
                if today[5] == "0":
                    today = today[:5] + today[6:]
                if today[7] == "0":
                    today = today[:7] + today[8:]
                if tomorrow[5] == "0":
                    tomorrow = tomorrow[:5] + tomorrow[6:]
                if tomorrow[7] == "0":
                    tomorrow = tomorrow[:7] + tomorrow[8:]

                thisurl = courselist['sources'][course]['url']
                if inp == '1':
                    thisurl = thisurl.replace(
                        courselist['sources'][course]['datetag'], today)
                elif inp == '2':
                    thisurl = thisurl.replace(
                        courselist['sources'][course]['datetag'], tomorrow)
                else:
                    thisurl = thisurl.replace(
                        courselist['sources'][course]['datetag'], inp)

                html = urllib.request.urlopen(thisurl).read()
                soup = BeautifulSoup(html, features='lxml')

                # Check number of players first
                skiplist = []
                skip = 0
                playercheck = 0
                for players in soup.findAll(attrs={'class': 'xs-align-right'}):
                    playersString = str(players).replace(
                        "<p class=\"xs-align-right\">", "")
                    playersString = playersString.replace("</p>", "")

                    if playersString == "Single Only":
                        playercheck = 1
                    elif playersString == "1 to 2 Players":
                        playercheck = 2
                    elif playersString == "1 to 3 Players":
                        playercheck = 3
                    else:
                        playercheck = 4

                    if playercheck < courselist['settings']['Players']:
                        skiplist.append(skip)
                        skip += 1
                    else:
                        skip += 1
                        if playersString == "Single Only":
                            playersArray.append("1 Player      ")
                        else:
                            playersArray.append(playersString)
                # Reset Skip counter
                skip = 0
                for times in soup.findAll(attrs={'class': 'timeDiv timeDisplay'}):
                    if skip in skiplist:
                        skip += 1
                    else:
                        timesString = str(
                            times.contents[1]).replace("</span>", "")
                        timesString = str(timesString).replace("<span>", "")
                        timesArray.append(timesString)
                        num += 1
                        skip += 1

                for i in range(num):
                    teetimeinfo.append(
                        [timesArray[i], playersArray[i], courselist['sources'][course]['name']])
                    numstring = "key" + \
                        courselist['sources'][course]['id'] + "-" + str(i)
                    keys.append(numstring)

            # Search Les Bolstad
            elif courselist['sources'][course]['id'] == "4" and courselist['sources'][course]['enabled'] == 1:

                # get todays date in dd-mm-yyyy
                today = datetime.today().strftime('%m-%d-%Y')
                tomorrow = datetime.today() + timedelta(days=1)
                tomorrow = tomorrow.strftime('%m-%d-%Y')

                thisurl = courselist['sources'][course]['url']
                if inp == '1':
                    thisurl = thisurl.replace(
                        courselist['sources'][course]['datetag'], today)
                elif inp == '2':
                    thisurl = thisurl.replace(
                        courselist['sources'][course]['datetag'], tomorrow)
                else:
                    thisurl = thisurl.replace(
                        courselist['sources'][course]['datetag'], inp)

                r = requests.get(thisurl)

                # Check number of players first
                skiplist = []
                skip = 0
                playercheck = 0
                addString = ''
                for teetime in r.json():

                    # Create text for number of available spots
                    if str(teetime['available_spots']) == "1":
                        playercheck = 1
                        addString = str(teetime['available_spots']) + ' Player'
                    elif str(teetime['available_spots']) == "2":
                        playercheck = 2
                        addString = '1 to 2 Players'
                    elif str(teetime['available_spots']) == "3":
                        playercheck = 3
                        addString = '1 to 3 Players'
                    elif str(teetime['available_spots']) == "4":
                        playercheck = 4
                        addString = '1 to 4 Players'
                    if playercheck >= courselist['settings']['Players']:
                        playersArray.append(addString)
                        # split time from 24hr to 12 hr
                        time = teetime['time'].partition(' ')
                        d = datetime.strptime(time[2], "%H:%M")
                        d = d.strftime("%I:%M %p")
                        if d[0] == "0":
                            d = d[1:]
                        timesArray.append(d)
                        num += 1

                for i in range(num):
                    teetimeinfo.append(
                        [timesArray[i], playersArray[i], courselist['sources'][course]['name']])
                    numstring = "key" + \
                        courselist['sources'][course]['id'] + "-" + str(i)
                    keys.append(numstring)

            # Search Chomonix for single times
            elif courselist['sources'][course]['id'] == "8" and courselist['sources'][course]['enabled'] == 1:
                # get todays date in yyyy-mm-dd
                today = datetime.today().strftime('%Y-%m-%d')
                tomorrow = datetime.today() + timedelta(days=1)
                tomorrow = tomorrow.strftime('%Y-%m-%d')

                thisurl = courselist['sources'][course]['singlesurl']
                if inp == '1':
                    thisurl = thisurl.replace(
                        courselist['sources'][course]['datetag'], today)
                elif inp == '2':
                    thisurl = thisurl.replace(
                        courselist['sources'][course]['datetag'], tomorrow)
                else:
                    thisurl = thisurl.replace(
                        courselist['sources'][course]['datetag'], inp)

                r = requests.get(thisurl)

                # Create disclaimer for Chomonix data
                errmsg = "* Chomonix will not allow singles to book a time if a foursome is available. Check the following website for more booking information: \n" + thisurl

                # Chomonix will not allow singles to book times unless a 2some or 3some has booked already. Mark these with asterisk
                for teetime in r.json():
                    if not teetime['restrictions'] and not teetime['out_of_capacity'] == True:
                        # split time from 24hr to 12 hr
                        time = teetime['start_time']
                        d = datetime.strptime(time, "%H:%M")
                        d = d.strftime("%I:%M %p")
                        if d[0] == "0":
                            d = d[1:]
                            timesArray.append(d)
                            if len(teetime['green_fees']) == 1:
                                playersArray.append('>= 1 Players  ')
                        else:
                            timesArray.append(d)
                            if len(teetime['green_fees']) == 1:
                                playersArray.append('>= 1 Players  ')
                        num += 1

                for i in range(num):
                    teetimeinfo.append(
                        [timesArray[i], playersArray[i], courselist['sources'][course]['name']+' *'])
                    numstring = "key" + \
                        courselist['sources'][course]['id'] + "-" + str(i)
                    keys.append(numstring)

        teetimeinfo = sorted(teetimeinfo, key=lambda x: datetime.strptime(
            x[0], '%I:%M %p'))
        bookingInfo = ["Time", "Players", "Course"]

        ikey = 0
        for eachTime in teetimeinfo:
            tempdict = {
                "Time": eachTime[0], "Players": eachTime[1], "Course": eachTime[2]}
            teeTimes[ikey] = tempdict
            ikey += 1

        headers = ["Course", "Time", "Players"]
        timestr = "00"
        print('\n')
        for key, value in teeTimes.items():
            if type(value) == dict:
                if value["Time"][:2] != timestr:
                    print("--------")
                print(value["Time"] + "   ---   " +
                      value["Players"] + "   ---   " + value["Course"])
                timestr = value["Time"][:2]

        print('\n' + errmsg + '\n')

    os.remove(filename)
    with open(filename, 'w') as f:
        json.dump(courselist, f, indent=4)


if __name__ == "__main__":
    main()
