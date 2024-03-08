import collections
import os
from json import loads, dumps

from abstractions import *

DATA_DIRECTORY = '/Users/sadiatasnim/Desktop/2130_project/code/datafolder'



def load(fp, **kw):
    return [loads(obj, **kw) for obj in fp]


def dump(objs, fp, **kw):
    for obj in objs:
        fp.write(dumps(obj, **kw))
        fp.write('\n')


def load_data(user_dataset, review_dataset, restaurant_dataset):
    with open(os.path.join(DATA_DIRECTORY, user_dataset)) as f:
        user_data = load(f)
    with open(os.path.join(DATA_DIRECTORY, review_dataset)) as f:
        review_data = load(f)
    with open(os.path.join(DATA_DIRECTORY, restaurant_dataset)) as f:
        restaurant_data = load(f)

    # Load users.
    userid_to_user = {}
    for user in user_data:
        name = user['name']
        _user_id = user['user_id']
        user = User(name, [])
        if user is not None:
            userid_to_user[_user_id] = user

    # Load restaurants.
    busid_to_restaurant = {}
    for restaurant in restaurant_data:
        name = restaurant['name']
        location = [float(restaurant['latitude']), float(restaurant['longitude'])]
        categories = restaurant['categories']
        price = restaurant['price']
        if price is not None:
            price = int(price)
        # num_reviews = int(restaurant['review_count'])

        _business_id = restaurant['business_id']
        restaurant = Restaurant(name, location, categories, price, [])  # MISSING: reviews
        if restaurant is not None:
            busid_to_restaurant[_business_id] = restaurant

    # Load reviews.
    reviews = []
    busid_to_reviews = collections.defaultdict(list)
    userid_to_reviews = collections.defaultdict(list)
    for review in review_data:
        _user_id = review['user_id']
        _business_id = review['business_id']

        restaurant = busid_to_restaurant[_business_id].get_name()
        rating = float(review['stars'])

        review = Review(restaurant, rating)
        if review is not None:
            reviews.append(review)
        busid_to_reviews[_business_id].append(review)
        userid_to_reviews[_user_id].append(review)
    # Reviews done.

    restaurants = {}
    for busid, restaurant in busid_to_restaurant.items():
        name = restaurant.get_name()
        location = []
        if restaurant.get_location() is not None:
            location = list(restaurant.get_location())
        categories = restaurant.get_categories()
        price = restaurant.get_price()
        restaurant_reviews = busid_to_reviews[busid]

        restaurant = Restaurant(name, location, categories, price, restaurant_reviews)
        restaurants[name] = restaurant
    # Restaurants done.

    users = []
    for userid, user in userid_to_user.items():
        name = user.get_name()
        user_reviews = userid_to_reviews[userid]
        user = User(name, user_reviews)
        users.append(user)
    # Users done.

    return users, reviews, list(restaurants.values())


USERS, REVIEWS, ALL_RESTAURANTS = load_data('users.json', 'reviews.json', 'restaurants.json')

if len(ALL_RESTAURANTS) > 1:
    CATEGORIES = {c for r in ALL_RESTAURANTS for c in r.get_categories()}
else:  # There are no restaurants!  We'll just set CATEGORIES to the empty set.
    CATEGORIES = set()
