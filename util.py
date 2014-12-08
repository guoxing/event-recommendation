import json, pickle, os
import genData

USER_DICT_F = './yelp/userDict.pickle'
BUZ_DICT_F = './yelp/buzDict.pickle'

def getUserIdMapping():
    userDict = {}
    if os.path.isfile(USER_DICT_F):
        with open(USER_DICT_F) as f:
            userDict = pickle.load(f)
        return userDict
    else:
        with open(genData.USER_HAS_REVIEW) as f:
            users = json.load(f)
        count = 0
        for user_id, user in users.items():
            if user['user_id'] not in userDict:
                userDict[user['user_id']] = count
                count += 1
        with open(USER_DICT_F, 'w') as f:
            pickle.dump(userDict, f)
    return userDict

def getBuzIdMapping():
    buzDict = {}
    if os.path.isfile(BUZ_DICT_F):
        with open(BUZ_DICT_F) as f:
            buzDict = pickle.load(f)
    else:
        with open(genData.BUSINESS_PHX) as f:
            buzs = json.load(f)
        count = 0
        for buz_id, buz in buzs.items():
            if buz['business_id'] not in buzDict:
                buzDict[buz['business_id']] = count
                count += 1
        with open(BUZ_DICT_F, 'w') as f:
            pickle.dump(buzDict, f)
    return buzDict

def genUserBuzMatrix(train=1):
    userDict = getUserIdMapping()
    buzDict = getBuzIdMapping()
    matrix = []
    for i in range(len(userDict)):
        matrix.append([])
        for j in range(len(buzDict)):
            matrix[i].append(0)

    if train:
        with open(genData.REVIEW_PHX_TRAIN) as f:
            reviews = json.load(f)
    else:
        with open(genData.REVIEW_PHX_TEST) as f:
            reviews = json.load(f)
    for review in reviews:
        matrix[userDict[review['user_id']]][buzDict[review['business_id']]] = 1
    return matrix

def predict(matrix):
    with open(genData.REVIEW_PHX_TRAIN) as f:
        train = json.load(f)

    with open(genData.REVIEW_PHX_TEST) as f:
        test = json.load(f)

    userDict = getUserIdMapping()

    train_dict = {}
    for review in train:
        buz_id = review['business_id']
        if buz_id not in train_dict:
            train_dict[buz_id] = []
        train_dict[buz_id].append(review)

    error = 0
    count = 0
    average = 0
    for review in test:
        user_idx_1 = userDict[review['user_id']]
        business_id = review['business_id']
        temp = []
        if business_id not in train_dict:
            continue
        for train_review in train_dict[business_id]:
            temp.append(matrix[user_idx_1][userDict[train_review['user_id']]])
        sum_t = sum(temp)
        if sum_t == 0:
            average += 1
            weight = [1 / len(temp) for _ in temp]
        else:
            weight = [w / sum_t for w in temp]
        count += 1
        predict = 0
        for idx, train_review in enumerate(train_dict[business_id]):
            predict += weight[idx] * train_review['stars']
        error += (predict - review['stars']) ** 2

    print 'count:', count, 'average:', average, 'total:', len(test)
    print (error / count) ** 0.5
    
