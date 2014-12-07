import pickle, json, random
import genData, util

with open('./yelp/user_rwr_matrix.pickle') as f:
    matrix = pickle.load(f)

with open(genData.REVIEW_PHX_TRAIN) as f:
    train = json.load(f)

with open(genData.REVIEW_PHX_TEST) as f:
    test = json.load(f)

userDict = util.getUserIdMapping()

train_dict = {}
for review in train:
    buz_id = review['business_id']
    if buz_id not in train_dict:
        train_dict[buz_id] = []
    train_dict[buz_id].append(review)

error = 0
count = 0
for review in test:
    user_idx_1 = userDict[review['user_id']]
    business_id = review['business_id']
    temp = []
    if business_id not in train_dict:
        continue
    count += 1
    for train_review in train_dict[business_id]:
        temp.append(matrix[user_idx_1][userDict[train_review['user_id']]])
    sum_t = sum(temp)
    if sum_t == 0:
        weight = [1 / len(temp) for _ in temp]
    else:
        weight = [w / sum_t for w in temp]
    predict = 0
    for idx, train_review in enumerate(train_dict[business_id]):
        predict += weight[idx] * train_review['stars']
    error += (predict - review['stars']) ** 2

print 'count:', count, 'total:', len(test)
print (error / count) ** 0.5
