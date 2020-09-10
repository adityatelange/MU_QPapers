import threading

from telegram import ParseMode
from telegram.chataction import ChatAction
from telegram.ext.dispatcher import run_async

from Brain.Utils.dbfuncs import user_collect, get_stats_from_db, command_collect
from Brain.Utils.strings import logger


# do not async
def send_stats(update, text, keyboard=None):
    logger.info("into send_stats")
    if not keyboard:
        pass
    update.effective_message.reply_text(text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)


@run_async
def get_stats(update, context):
    logger.info("into get_stats")
    chat = update.effective_chat

    threading.Thread(target=user_collect, args=(chat,), daemon=True).start()
    threading.Thread(target=command_collect, args=("stats",), daemon=True).start()

    # ONLY send stats in PM
    if chat.type != chat.PRIVATE:
        return
    else:
        context.bot.send_chat_action(chat_id=chat.id, action=ChatAction.TYPING)
        stats = get_stats_from_db()
        text = "*Stats* : \nActive Users = _{}/{}_\nQueries Served = _{}/{}_". \
            format(
                stats['users']['active_users'],
                stats['users']['total_users'],
                stats['queries']['successful_queries'],
                stats['queries']['total_queries']
            )
        send_stats(update=update, text=text, )
