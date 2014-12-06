import json, pickle, os, random
from collections import Counter

USER = './yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_user.json'
USER_WITH_FRIENDS = './yelp_dataset_challenge_academic_dataset/user_with_friends.json'
USER_HAS_REVIEW = './yelp/user_has_review.json' # has review on buz in phoenix
BUSINESS = './yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json'
BUSINESS_PHX = './yelp/business_phx.json'
REVIEW = './yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json'
REVIEW_PHX = './yelp/review_phx.json'
REVIEW_PHX_TRAIN = './yelp/review_phx_train.json'
REVIEW_PHX_TEST = './yelp/review_phx_test.json'

user_review_threshold = 4
buz_review_threshold = 4

def pickUserWithFriends():
    with open(USER) as f:
        users = []
        user_ids = set([])
        for line in f:
            user = json.loads(line)
            if len(user['friends']) != 0:
                users.append(user)
                user_ids.add(user['user_id'])
        new_users = []
        link_count = 0
        for user in users:
            remove = True
            for friend in user['friends']:
                if friend in user_ids:
                    remove = False
                    link_count += 1
            if not remove:
                new_users.append(user)
        with open(USER_WITH_FRIENDS, 'w') as w:
            json.dump(new_users, w)

def pickUserHasReview():
    user_ids = set([])
    with open(USER_WITH_FRIENDS) as f:
        users = json.load(f)
        for user in users:
            user_ids.add(user['user_id'])
    with open(BUSINESS_PHX) as f:
        buzs = json.load(f)
    buz_ids = buzs.keys()
    reviewed_user_count = Counter()
    with open(REVIEW) as f:
        reviews = []
        for line in f:
            review = json.loads(line)
            if review['user_id'] in user_ids and review['business_id'] in buz_ids:
                reviews.append(review)
                reviewed_user_count[review['user_id']] += 1
    less_users = {}
    for user in users:
        if reviewed_user_count[user['user_id']] > user_review_threshold:
            less_users[user['user_id']] = user
    print '#users: ', len(less_users)
    with open(USER_HAS_REVIEW, 'w') as f:
        json.dump(less_users, f)
    less_reviews = []
    for review in reviews:
        if review['user_id'] in less_users and review['business_id'] in buzs:
            less_reviews.append(review)
    print '#reviews: ', len(less_reviews)
    with open(REVIEW_PHX, 'w') as f:
        json.dump(less_reviews, f)

def pickBusiness():
    with open(BUSINESS) as f:
        buz_cities = {}
        for line in f:
            buz = json.loads(line)
            if buz['city'] not in buz_cities:
                buz_cities[buz['city']] = []
            buz_cities[buz['city']].append(buz)
    buzs = buz_cities['Phoenix']
    buz_counts = {}
    for buz in buzs:
        buz_counts[buz['business_id']] = 0
    with open(REVIEW) as f:
        for line in f:
            review = json.loads(line)
            if review['business_id'] in buz_counts:
                buz_counts[review['business_id']] += 1
    less_buzs = {}
    for buz in buzs:
        if buz_counts[buz['business_id']] > buz_review_threshold:
            less_buzs[buz['business_id']] = buz
    print '#buzs ', len(less_buzs)
    with open(BUSINESS_PHX, 'w') as w:
        json.dump(less_buzs, w)

def genTrainAndTest():
    train = []
    test = []
    with open(REVIEW_PHX) as f:
        reviews = json.load(f)
    for review in reviews:
        if random.random() < 0.7:
            train.append(review)
        else:
            test.append(review)
    with open(REVIEW_PHX_TRAIN, 'w') as f:
        json.dump(train, f)
    with open(REVIEW_PHX_TEST, 'w') as f:
        json.dump(test, f)

#pickBusiness()
#pickUserHasReview()
#genTrainAndTest()
