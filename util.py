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

