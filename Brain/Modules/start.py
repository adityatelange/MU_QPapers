import threading

from telegram import ChatAction, ParseMode
from telegram.utils.helpers import escape_markdown

from Brain.Modules.help import get_help
from Brain.Utils.dbfuncs import user_collect
from Brain.Utils.user_info import get_user_info

PM_START_TEXT = """Hello {}, my name is {}! If you have any questions on how to use me, read /help.
I'm a MU Student Assistant bot ."""


def start(update, context):
    chat = update.effective_chat

    threading.Thread(target=user_collect, args=(chat,), daemon=True).start()
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    if chat.type == "private":
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
                parse_mode=ParseMode.MARKDOWN
            )

    else:
        update.effective_message.reply_text("Hey, {}!".format(escape_markdown(update.effective_user.first_name)))
