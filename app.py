from datetime import datetime
import csv
import re

results = []
data = []
filename = ""

filename = str(input("Please input the name of the csv file: "))

glCounter = 0
blCounter = 0
studentIDS = ['ast103', 'ast104', 'ast105', 'ast107','ast108','ast111','ast112','ast114','ast115','ast116','ast118','ast125','ast131','ast133','ast134','ast135','ast136','ast138']
goodLogins = []
badLogins = []
totalLogins = []
timeGoodLogins = []
timeBadLogins = []
user_dict = {}
for id in studentIDS:
    user_dict[id] = [[], []] #first is success, second is failure

with open(filename, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    with open('new_names.csv', 'w') as new_file:
        fieldnames = ['date', 'id', 'website','pswdType','idk','submition','progress', 'browser']

        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)

        csv_writer.writeheader()

        for line in csv_reader:
            #print(line)
            data.append(line)

for id in range(len(studentIDS)):
    for line in data:
        if(line.get('id') == studentIDS[id] and line.get('progress') == "success") :
            glCounter +=1
        if(line.get('id') == studentIDS[id] and line.get('progress') == "failure") :
            blCounter +=1

    badLogins.append(blCounter)
    goodLogins.append(glCounter)
    glCounter = 0
    blCounter = 0

for index in range(18):
    sumLogins = goodLogins[index] + badLogins[index]
    totalLogins.append(sumLogins)
    sumLogins = 0

#not averages
#if does not work, put in def and call here
idindex = 1
ids = []
for id in range(len(studentIDS)):
    #print("Index: " + str(idindex) +"ID: " + str(id))
    idindex += 1
    for index, line in enumerate(data):
        if ((index + 2 ) < len(data)):
            nextnextline = data[index + 2]
            if (line.get('id') == studentIDS[id] and line.get('submition') == "enter" and line.get('progress') == "start" and nextnextline.get('submition') == "login" ):
                ids.append(line.get('id'))
                stamp = line.get('date').rsplit(' ', 1)
                stime = stamp[1].rsplit(':',2)
                shour = int(stime[0])
                sminute = int(stime[1])
                ssecond = int(stime[2])
                etamp = nextnextline.get('date').rsplit(' ', 1)
                etime = etamp[1].rsplit(':',2)
                ehour = int(etime[0])
                eminute = int(etime[1])
                esecond = int(etime[2])
                fminute =  eminute - sminute
                fsecond = esecond - ssecond
                ftime = ((fminute * 60) + fsecond) / 60
                ftime = "%0.2f" % ftime
                if(shour == ehour):
                    if(nextnextline.get('progress') == "success"):
                        user_dict[line.get('id')][0].append(ftime)
                        timeGoodLogins.append(ftime)
                    if(nextnextline.get('progress') == "failure"):
                        user_dict[line.get('id')][1].append(ftime)
                        timeBadLogins.append(ftime)
                if(shour < ehour):
                    fhour = ehour - shour
                    ftime = ((fhour * 60) * 60) + ftime
                    ftime = "%0.2f" % ftime
                    if(nextnextline.get('progress') == "success"):
                        user_dict[line.get('id')][0].append(ftime)
                        timeGoodLogins.append(ftime)
                    if(nextnextline.get('progress') == "failure"):
                        user_dict[line.get('id')][1].append(ftime)
                        timeBadLogins.append(ftime)


"""
#averages
for id in range(len(studentIDS)):
    good = []
    bad = []
    for index, line in enumerate(data):
        if((index + 2) > len(data)):
            if(len(good) > 0 and len(bad) > 0):
                totalgood = 0
                totalbad = 0
                for st in good :
                    totalgood += st
                for st in bad:
                    totalbad += st

                timeGoodLogins.append(totalgood / len(good))
                timeBadLogins.append(totalbad / len(bad))

        if ((index + 2 ) < len(data)): #being annoying
            nextnextline = data[index + 2]
            if (line.get('id') == studentIDS[id] and line.get('submition') == "enter" and line.get('progress') == "start" and nextnextline.get('submition') == "login" ):
                stamp = line.get('date').rsplit(' ', 1)
                stime = stamp[1].rsplit(':',2)
                shour = int(stime[0])
                sminute = int(stime[1])
                ssecond = int(stime[2])
                etamp = nextnextline.get('date').rsplit(' ', 1)
                etime = etamp[1].rsplit(':',2)
                ehour = int(etime[0])
                eminute = int(etime[1])
                esecond = int(etime[2])
                fminute =  eminute - sminute
                fsecond = esecond - ssecond
                ftime = (fminute * 60) + fsecond
                if(shour == ehour):
                    if(nextnextline.get('progress') == "success"):
                        good.append(ftime)
                    if(nextnextline.get('progress') == "failure"):
                        bad.append(ftime)
                if(shour < ehour):
                    fhour = ehour - shour
                    ftime = ((fhour * 60) * 60) + ftime
                    if(nextnextline.get('progress') == "success"):
                        good.append(ftime)
                    if(nextnextline.get('progress') == "failure"):
                        bad.append(ftime)
"""

print("\n")
print("timegoodLogins: ")
print(timeGoodLogins)
print("\n")
print("timebadLogins: ")
print(timeBadLogins)
print("\n")
print("totalLogins: ")
print(totalLogins)
print("\n")
print("goodLogins: ")
print((goodLogins))
print("\n")
print("badLogins: ")
print((badLogins))
print("\n")
print("studentIDs: ")
print((studentIDS))
print("\n")
print("Student Dict: ")
for id in user_dict:
    print("-----------------------------------------------------------")
    print('ID: ', id)
    print('Good: ', user_dict[id][0])
    print("\n")
    print('Bad: ', user_dict[id][1])
    print("\n")
        #print("ID: " + id)
        #print("Good: " + list[0])
        #print("Bad: " + list[1])
