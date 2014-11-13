import snap
import csv, os, pickle

USER_DICT_F = 'data/userDict.pickle'
EVENT_DICT_F = 'data/eventDict.pickle'

# return a dict that converts userID to integer
def readUserDict():
    if os.path.isfile(USER_DICT_F):
        with open(USER_DICT_F, 'r') as f:
            userDict = pickle.load(f)
        return userDict
    else:
        userDict = {}
        count = 0
        with open('data/users.csv', 'r') as f:
            f.readline()
            csvreader = csv.reader(f)
            for row in csvreader:
                if row[0] not in userDict:
                    userDict[row[0]] = count
                    count += 1
        #with open('data/user_friends.csv') as f:
            #f.readline()
            #csvreader = csv.reader(f)
            #for row in csvreader:
                #for uid in row[1].split():
                    #if uid not in userDict:
                        #userDict[uid] = count
                        #count += 1
        #with open('data/event_attendees.csv') as f:
            #f.readline()
            #csvreader = csv.reader(f)
            #for row in csvreader:
                ## only care people who attend
                #for uid in row[1].split():
                    #if uid not in userDict:
                        #userDict[uid] = count
                        #count += 1
        with open(USER_DICT_F, 'w') as f:
            pickle.dump(userDict, f)
        return userDict

# return a dict that converts eventID to integer
def readEventDict():
    if os.path.isfile(EVENT_DICT_F):
        with open(EVENT_DICT_F, 'r') as f:
            eventDict = pickle.load(f)
        return eventDict
    else:
        eventDict = {}
        with open('data/event_attendees.csv', 'r') as f:
            f.readline()
            csvreader = csv.reader(f)
            count = 40000
            for row in csvreader:
                if row[0] not in eventDict:
                    eventDict[row[0]] = count
                    count += 1
        with open(EVENT_DICT_F, 'w') as f:
            pickle.dump(eventDict, f)
        return eventDict

def readGraph():
    G = snap.TNEANet()
    userDict = readUserDict()
    eventDict = readEventDict()
    with open('data/users.csv', 'r') as f:
        f.readline()
        csvreader = csv.reader(f)
        for row in csvreader:
            nid_u = userDict[row[0]]
            if not G.IsNode(nid_u):
                G.AddNode(nid_u)
                G.AddStrAttrDatN(nid_u, 'user', 'type')

    with open('data/event_attendees.csv', 'r') as f:
        f.readline()
        csvreader = csv.reader(f)
        missed = 0
        add = 0
        for row in csvreader:
            nid_e = eventDict[row[0]]
            if not G.IsNode(nid_e):
                G.AddNode(nid_e)
                G.AddStrAttrDatN(nid_e, 'event', 'type')
            for uid in row[1].split():
                if uid not in userDict:
                    missed += 1
                    continue
                add+=1
                nid_u = userDict[uid]
                G.AddEdge(nid_e, nid_u)
                G.AddEdge(nid_u, nid_e)
    print missed, add
    with open('data/user_friends.csv', 'r') as f:
        f.readline()
        csvreader = csv.reader(f)
        missed = 0
        add = 0
        for row in csvreader:
            nid_u1 = userDict[row[0]]
            for uid in row[1].split():
                if uid not in userDict:
                    missed += 1
                    continue
                add+=1
                nid_u2 = userDict[uid]
                G.AddEdge(nid_u1, nid_u2)
                G.AddEdge(nid_u2, nid_u1)
    print missed, add
    return G

