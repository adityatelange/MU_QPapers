import os
import sys

import pymongo
import telepot

try:
    MONGOUSER = os.getenv("MONGOUSER")
    MONGOPASS = os.getenv("MONGOPASS")
    MONGOURL = os.getenv("MONGOURL")
    MONGODBNAME = os.getenv("MONGODBNAME")
    TOKEN = os.getenv("TOKEN")
    OWNER_ID = os.getenv("OWNER_ID")

except Exception as e:
    print(e)
    sys.exit()

bot = telepot.Bot(TOKEN)

client = pymongo.MongoClient(
    "mongodb+srv://{}:{}@{}".format(MONGOUSER, MONGOPASS, MONGOURL)
)

if MONGODBNAME in client.list_database_names():
    db = client[MONGODBNAME]
else:
    print("[#] Alert : DB does not exists")
    sys.exit()


def get_user_ids():
    users = db.users.find()
    ids = []
    for user in users:
        ids.append(user['id'])
    return ids


def blocked(idy):
    query = {"id": idy}

    new = {"$set": {"blocked": True, }}
    p = db.users.update_many(query, new)
    return p.acknowledged


def unblock_user(idy):
    query = {"id": idy}

    new = {"$unset": {"blocked": True}}
    p = db.users.update_many(query, new)
    return p.acknowledged


def is_active(data, to, ):
    sent = bot.sendMessage(chat_id=to, text=data,
                           parse_mode='Markdown', disable_notification=True)
    message_id = sent['message_id']
    x = bot.deleteMessage((to, message_id))
    return x


msg = """You shouldn't have seen this. :p, anyways this is a test message"""

users_list = get_user_ids()
users_list = list(dict.fromkeys(users_list))

count = 0
deleted = 0
for user_id in users_list:
    try:
        if is_active(msg, user_id) and unblock_user(user_id):
            count += 1
        else:
            print("ops1")
    except telepot.exception.BotWasBlockedError:
        if blocked(user_id):
            deleted += 1
        else:
            print("ops2")
    except telepot.exception.BotWasKickedError:
        if blocked(user_id):
            deleted += 1
        else:
            print("ops3")
    except telepot.exception.TelegramError as e:
        if e.error_code == 403:
            if blocked(user_id):
                deleted += 1
            else:
                print("ops4")
    except Exception as e:
        print(e)

bot.sendMessage(
    chat_id=OWNER_ID,
    text="Active Keeper Run Successfull\n{} active\n{} deleted".format(
        count, deleted),
    parse_mode='Markdown'
)
