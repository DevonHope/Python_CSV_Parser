from datetime import datetime as dt
import os, glob
import csv
from pathlib import Path

def parse_the_data(filename, user_dict):

    glCounter = 0
    blCounter = 0
    studentIDS = []
    goodLogins = []
    badLogins = []
    totalLogins = []
    timeGoodLogins = []
    timeBadLogins = []
    data = []

    with open(filename, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        #append to data
        for line in csv_reader:
            data.append(line)
            #print(line)

    for line in data: #get ids
        if line.get('id') not in studentIDS:
            studentIDS.append(line.get('id'))
        #print(studentIDS)

    for id in studentIDS:
        user_dict[id] = [[],[],[],[],[]]
        #timegood[0], timebad[1], totalgood[2], totalbad[3], total[4]

    for id in studentIDS:
        for line in data:
            if(line.get('id') == id and line.get('submition') == "login" and line.get('progress') == "success") :
                glCounter +=1
            if(line.get('id') == id and line.get('submition') == "login" and line.get('progress') == "failure") :
                blCounter +=1

        sumLogins = glCounter + blCounter
        user_dict[id][4].append(sumLogins)
        user_dict[id][2].append(glCounter)
        user_dict[id][3].append(blCounter)
        glCounter = 0
        blCounter = 0

    time_format = '%H:%M:%S'
    #new parser
    #loop through till you find each attempt end and then go back
    for id in studentIDS:
        for index, line in enumerate(data):
            if(line.get('id') == id and line.get('submition') == "enter" and line.get('progress') == "start"):
                linecount = 1;
                attempt = False;
                while(attempt == False):
                    if(linecount > 3):
                        attempt = True;
                    if((index + linecount) < len(data)):
                        newline = data[index + linecount];
                        if(newline.get('id') == id and newline.get('submition') == "login"):
                            stamp = line.get('date').rsplit(' ', 1);
                            etamp = newline.get('date').rsplit(' ', 1);
                            times = [stamp[1], etamp[1]];
                            base_time = dt.strptime(times[0], time_format);
                            seconds = [(dt.strptime(t, time_format)- base_time).total_seconds() for t in times];
                            if(newline.get('progress') == "success"):
                                user_dict[id][0].append(seconds[1]);
                            if(newline.get('progress') == "failure"):
                                user_dict[id][1].append(seconds[1]);

                            linecount += 1;
                        else:
                            linecount += 1
                    else:
                        linecount+=1

    return user_dict;

def addHeader(filename):
    with open(filename,newline='') as f:
        r = csv.reader(f)
        data = [line for line in r]
        if data[0] != ['date', 'id', 'website', 'pswdType', 'idk', 'submition', 'progress', 'browser']:
            #writes header to a csv file
            with open(filename,'w',newline='') as f:
                w = csv.writer(f)
                w.writerow(['date', 'id', 'website', 'pswdType', 'idk', 'submition', 'progress', 'browser'])
                w.writerows(data)
        else:
            print("headers for " + filename + " already added!")

def w_to_r(f_names,ud,result):
    with open(result, 'a') as r_file:
        dash = "------------"
        fieldnames = ['ID','total_logins','tot_good', 'tot_bad','time_good', 'time_bad']
        writer = csv.DictWriter(r_file,fieldnames=fieldnames)

        for index, user in enumerate(ud):
            r_file.write('\n')
            r_file.write(f_names[index] + dash + dash + dash + dash + dash)
            r_file.write('\n')
            for id in user:
                writer.writerow({'ID': id, 'total_logins':user[id][4],
                'tot_good':user[id][2],'tot_bad':user[id][3],
                'time_good':user[id][0],'time_bad':user[id][1]})
            r_file.write('\n')

        print("Data has been parsed and written too file: result.csv")

def main():
    result = "ATS_results.csv"
    f_names = []
    results = Path("results/")
    for file in results.rglob('*.csv'):
        f_names.append(file.name)

    #print(f_names)
    ud = []
    for file in f_names:
        p = "results/"+file
        addHeader(p)
        user_dict = {}
        user_dict = parse_the_data(p, user_dict)
        ud.append(user_dict)

    with open(result, 'w') as r_file:
        fieldnames = ['ID','total_logins','tot_good', 'tot_bad','time_good', 'time_bad']
        writer = csv.DictWriter(r_file, fieldnames=fieldnames)
        writer.writeheader()

    w_to_r(f_names,ud,result)

main()
