import threading

from telegram import ParseMode
from telegram.chataction import ChatAction
from telegram.ext.dispatcher import run_async

from Brain.Modules.help import get_help
from Brain.Utils.dbfuncs import user_collect, feedback_collect, command_collect
from Brain.Utils.strings import HELPER_SCRIPTS
from server import logger

feedback_info_help = \
    """
        - /feedback <Type your feedback here>
    """
HELPER_SCRIPTS['feedback'] = feedback_info_help


# do not async
def send_feedback(update, text, keyboard=None):
    logger.info("into send_feedback")
    if not keyboard:
        pass
    update.effective_message.reply_text(text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)


@run_async
def get_feedback(update, context):
    logger.info("into get_feedback")
    chat = update.effective_chat

    threading.Thread(target=user_collect, args=(chat,), daemon=True).start()
    threading.Thread(target=command_collect, args=("feedback",), daemon=True).start()

    context.bot.send_chat_action(chat_id=chat.id, action=ChatAction.TYPING)
    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        context.args = ['feedback']
        get_help(update, context)
    else:
        # checks if command has arguments
        if context.args:
            feedback = " ".join(context.args)
            try:
                feedback_collect(chat, feedback)
                msg = "ThankYou for Feedback \U0001F4E9"
                send_feedback(
                    update=update,
                    text=msg,
                    keyboard=None
                )
            except Exception as e:
                pass
        else:
            context.args = ['feedback']
            get_help(update, context)
