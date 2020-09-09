import os
import sys

import pymongo

from Brain.Utils.strings import logger
from Brain.Utils.user_info import get_user_info


def db():
    db_name = os.getenv("MONGODBNAME")
    db_user = os.getenv("MONGOUSER")
    db_pass = os.getenv("MONGOPASS")
    db_url = os.getenv("MONGOURL")
    client = pymongo.MongoClient(
        "mongodb+srv://{}:{}@{}".format(db_user, db_pass, db_url))
    if db_name in client.list_database_names():
        db = client[db_name]
    else:
        logger.error("[#] Alert : DB does not exists")
        sys.exit()
    return db


def user_collect(chat):
    user = get_user_info(chat)
    db_users = db().users

    query = {"id": user['id']}
    new = {"$set": user}

    # if user exists update user object else create a new object
    db_users.update_one(query, new, upsert=True)
    logger.info("[+] USer collect {}".format(query))


def query_collect(query_as_dict):
    queries = db().queries
    res = queries.insert_one(query_as_dict)
    logger.info("[+] Query collect {}{}".format(res, query_as_dict))


def feedback_collect(user, feedback_str):
    feedback = db().feedback
    feedback_obj = {
        'user': user,
        'feedback': feedback_str
    }
    res = feedback.insert_one(feedback_obj)
    logger.info("[+] Feedback collect {}{}".format(res, feedback_str))


def unavailable_collect(query_as_dict):
    unavailables = db().unavailables
    res = unavailables.insert_one(query_as_dict)
    logger.info("[+] Unavailable collect {}{}".format(res, query_as_dict))


def get_stats_from_db():
    users = db().users.find().count()
    queries = db().queries.find().count()
    stats = {
        'user_count': users,
        'queries_count': queries
    }
    return stats
