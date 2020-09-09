import threading

from telegram.ext.dispatcher import run_async

from Brain.Modules.help import get_help
from Brain.Utils.dbfuncs import user_collect, command_collect
from Brain.Utils.strings import logger


@run_async
def text_handler(update, context):
    logger.info("into get_stats")
    chat = update.effective_chat

    threading.Thread(target=user_collect, args=(chat,), daemon=True).start()
    threading.Thread(target=command_collect, args=("text",), daemon=True).start()

    # ONLY send in PM
    if chat.type != chat.PRIVATE:
        return
    else:
        context.args = []
        get_help(update, context)
