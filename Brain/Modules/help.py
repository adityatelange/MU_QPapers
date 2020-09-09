import re
import threading

from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.chataction import ChatAction
from telegram.error import BadRequest
from telegram.ext.dispatcher import run_async

from Brain.Utils import button_menu
from Brain.Utils.dbfuncs import user_collect, command_collect
from Brain.Utils.strings import logger, HELPER_SCRIPTS

HELP_STRINGS = \
    """*Main* commands available:
 - /start: start the bot
 - /help: send you this message.
And the following:
"""


@run_async
def help_button(update, context):
    query = update.callback_query
    suggestion_match = re.match(r"help_action=(.+?)", query.data)
    back_button = re.match(r"help_back", query.data)
    try:
        if suggestion_match:
            text = query.data.split('=', 1)[1]
            context.args = text.split(' ')  # update context.args
            get_help(update, context)
        elif back_button:
            context.args = []
            get_help(update, context)

        # to ensure no spinning white circle
        context.bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as e:
        if e.message == "Message is not modified":
            pass
        elif e.message == "Query_id_invalid":
            pass
        elif e.message == "Message can't be deleted":
            pass
        else:
            logger.exception("Exception in help buttons. %s", str(query.data))


# do not async
def send_help(update, text, keyboard=None):
    logger.info("into send_help")
    if not keyboard:
        pass
    update.effective_message.reply_text(text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)


@run_async
def get_help(update, context):
    logger.info("into get_help")
    chat = update.effective_chat

    threading.Thread(target=user_collect, args=(chat,), daemon=True).start()
    threading.Thread(target=command_collect, args=("help",), daemon=True).start()

    context.bot.send_chat_action(chat_id=chat.id, action=ChatAction.TYPING)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(context.args) >= 1 and any(context.args[0].lower() == x for x in HELPER_SCRIPTS):
            module = context.args[0].lower()
            send_help(
                update,
                "Contact me in PM to get the list of possible commands.",
                InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton(text="Help for {}".format(module),
                                             url="t.me/{}?start={}".format(
                                                 context.bot.username, module))
                    ]]
                )
            )
        else:
            send_help(
                update,
                "Contact me in PM to get the list of possible commands.",
                InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton(text="Help",
                                             url="t.me/{}?start=help".format(
                                                 context.bot.username))
                    ]]
                )
            )
        return
    elif len(context.args) >= 1 and any(context.args[0].lower() == x for x in HELPER_SCRIPTS):
        module = context.args[0].lower()
        text = "Here is the available help for the *{}* module:\n".format(module) + HELPER_SCRIPTS[module]
        send_help(
            update,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Back", callback_data="help_back")]]
            )
        )

    else:
        button_list = []
        for module in HELPER_SCRIPTS:
            button_list.append(
                InlineKeyboardButton(
                    text="/{}".format(module),
                    callback_data="help_action={}".format(module),
                )
            )

        reply_markup_keyboard = InlineKeyboardMarkup(button_menu.build_menu(button_list, n_cols=2))

        send_help(
            update=update,
            text=HELP_STRINGS,
            keyboard=reply_markup_keyboard
        )
