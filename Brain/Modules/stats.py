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
        text = "*Stats* : \nTotal Users Served = _{}_\nTotal Queries Served = _{}_". \
            format(
                stats['user_count'],
                stats['queries_count']
            )
        send_stats(update=update, text=text, )
