from datetime import datetime as dt
import csv

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

    for line in data: #get ids
        if line.get('id') not in studentIDS:
            studentIDS.append(line.get('id'))
        #print(studentIDS)

    for id in studentIDS:
        user_dict[id] = [[],[],[],[],[]] #timegood[0], timebad[1], totalgood[2], totalbad[3], total[4]

    for id in studentIDS:
        for line in data:
            if(line.get('id') == id and line.get('progress') == "success") :
                glCounter +=1
            if(line.get('id') == id and line.get('progress') == "failure") :
                blCounter +=1

        sumLogins = glCounter + blCounter
        user_dict[id][4].append(sumLogins)
        user_dict[id][2].append(glCounter)
        user_dict[id][3].append(blCounter)
        glCounter = 0
        blCounter = 0

    time_format = '%H:%M:%S'

    for id in studentIDS:
        for index, line in enumerate(data):
            if ((index + 2 ) < len(data) and (index + 3) < len(data)):
                nextnextline = data[index + 2]
                nexttripleline = data[index + 3]
                if (line.get('id') == id and line.get('submition') == "enter" and line.get('progress') == "start" and nextnextline.get('submition') == "login" ):
                    #get array of times
                    stamp = line.get('date').rsplit(' ', 1)
                    etamp = nextnextline.get('date').rsplit(' ', 1)
                    times = [stamp[1], etamp[1]]
                    base_time = dt.strptime(times[0], time_format)
                    seconds = [(dt.strptime(t, time_format)- base_time).total_seconds() for t in times]

                    if(nextnextline.get('progress') == "success"):
                        user_dict[id][0].append(seconds[1])
                    if(nextnextline.get('progress') == "failure"):
                        user_dict[id][1].append(seconds[1])

                elif (line.get('id') == id and line.get('submition') == "enter" and line.get('progress') == "start" and nexttripleline.get('submition') == "login" ):
                    #get array of times
                    stamp = line.get('date').rsplit(' ', 1)
                    etamp = nexttripleline.get('date').rsplit(' ', 1)
                    times = [stamp[1], etamp[1]]
                    base_time = dt.strptime(times[0], time_format)
                    seconds = [(dt.strptime(t, time_format)- base_time).total_seconds() for t in times]
                    if(nexttripleline.get('progress') == "success"):
                        user_dict[id][0].append(seconds[1])
                    if(nexttripleline.get('progress') == "failure"):
                        user_dict[id][1].append(seconds[1])

    return user_dict

def addHeader(filename):
    with open(filename,newline='') as f:
        r = csv.reader(f)
        data = [line for line in r]
        if data[0] != ['date', 'id', 'website', 'pswdType', 'idk', 'submition', 'progress', 'browser']:
            #writes header to text21 file
            with open(filename,newline='') as f:
                r = csv.reader(f)
                data = [line for line in r]
            with open(filename,'w',newline='') as f:
                w = csv.writer(f)
                w.writerow(['date', 'id', 'website', 'pswdType', 'idk', 'submition', 'progress', 'browser'])
                w.writerows(data)
        else:
            print("headers for " + filename + " already added!")

addHeader('text21.csv')
addHeader('imagept21.csv')

f_names = ['text21.csv','imagept21.csv']

with open('results.csv', 'w') as r_file:
    fieldnames = ['ID','total_logins','tot_good', 'tot_bad','time_good', 'time_bad']
    writer = csv.DictWriter(r_file, fieldnames=fieldnames)
    writer.writeheader()

user_dict_txt = {}
user_dict_img = {}

user_dict_txt = parse_the_data(f_names[0], user_dict_txt)
user_dict_img = parse_the_data(f_names[1], user_dict_img)

with open('results.csv', 'a') as r_file:
    dash = "------------"
    r_file.write('\n')
    r_file.write(f_names[0] + dash + dash + dash + dash + dash)
    r_file.write('\n')
    fieldnames = ['ID','total_logins','tot_good', 'tot_bad','time_good', 'time_bad']
    writer = csv.DictWriter(r_file,fieldnames=fieldnames)
    for id in user_dict_txt:
        writer.writerow({'ID': id, 'total_logins':user_dict_txt[id][4],
        'tot_good':user_dict_txt[id][2],'tot_bad':user_dict_txt[id][3],
        'time_good':user_dict_txt[id][0],'time_bad':user_dict_txt[id][1]})
    r_file.write('\n')

    dash = "------------"
    r_file.write('\n')
    r_file.write(f_names[1] + dash + dash + dash + dash + dash)
    r_file.write('\n')
    for id in user_dict_img:
        writer.writerow({'ID': id, 'total_logins':user_dict_img[id][4],
        'tot_good':user_dict_img[id][2],'tot_bad':user_dict_img[id][3],
        'time_good':user_dict_img[id][0],'time_bad':user_dict_img[id][1]})
    print("Data has been parsed and written too file: results.csv")
