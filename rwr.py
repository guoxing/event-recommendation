import util, genData, pickle, json

# random walk with restart

with open(genData.USER_HAS_REVIEW) as f:
    users = json.load(f)

userDict = util.getUserIdMapping()
n = len(users)
user_list = [0] * n
count = 0
for user_id, user in users.items():
    friends = []
    for friend_id in user['friends']:
        if friend_id in users:
            friends.append(userDict[friend_id])
            count += 1
    user['friends'] = friends
    user_list[userDict[user_id]] = user

#user_list = [{'friends':[1,2,3]},
             #{'friends':[0]},
             #{'friends':[0]},
             #{'friends':[0,4]},
             #{'friends':[3]}]
#n = 5
#print 'user:', n
#print 'friend:', count

epsilon = 0.01
beta = 0.8
r = []
for start_idx in range(n):
    rs = [1 / float(n) for _ in range(n)]
    error = 1
    print 'start_idx ', start_idx
    while error > epsilon:
        newrs = [0 for _ in range(n)]
        for idx in range(n):
            if idx == start_idx:
                for idx2 in range(n):
                    weight = 1 - beta
                    if idx2 in user_list[idx]['friends']:
                        weight += beta / float(len(user_list[idx2]['friends']))
                    newrs[idx] += weight * rs[idx2]
            else:
                for friend_idx in user_list[idx]['friends']:
                    newrs[idx] += beta / float(len(user_list[friend_idx]['friends'])) * rs[friend_idx]
        error = sum(abs(newrs[idx] - rs[idx]) for idx in range(n))
        #print newrs
        #print error
        rs = newrs[:]
    print rs
    r.append(rs)

#with open('./yelp/user_rwr_matrix.pickle', 'w') as f:
    #pickle.dump(r, f)
