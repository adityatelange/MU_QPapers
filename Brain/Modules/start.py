import threading

from telegram import ChatAction, ParseMode
from telegram.utils.helpers import escape_markdown

from Brain.Modules.help import get_help
from Brain.Utils.strings import PM_START_TEXT
from Brain.Utils.dbfuncs import user_collect
from Brain.Utils.user_info import get_user_info


def start(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    threading.Thread(target=user_collect, args=(get_user_info(update.effective_chat),), daemon=True).start()

    if update.effective_chat.type == "private":
        if len(context.args) >= 1:
            if context.args[0].lower() == "help":
                get_help(update, context)
        else:
            first_name = update.effective_user.first_name
            reply = PM_START_TEXT.format(
                escape_markdown(first_name),
                escape_markdown(context.bot.first_name),
            )
            update.effective_message.reply_text(
                reply,
                parse_mode=ParseMode.MARKDOWN)

    else:
        update.effective_message.reply_text("Hey, {}!".format(escape_markdown(update.effective_user.first_name)))