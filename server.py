import threading

from telegram.ext import (CommandHandler, Updater, CallbackQueryHandler)
import os
import sys
from Brain.Utils.strings import logger

import Brain.Modules.start
import Brain.Modules.help
import Brain.Modules.qpapers
import Brain.Modules.stats
import Brain.Modules.feedback
from Brain.Utils.logger import initialize_logger


class Main:
    def __init__(self):
        self.mode = os.getenv("MODE")
        self.TOKEN = os.getenv("TOKEN")
        self.APP_NAME = os.environ.get("APP_NAME")
        self.domain = os.getenv("DOMAIN")
        self.PORT = int(os.environ.get("PORT", "8443"))

        self.updater = Updater(token=self.TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher

        threading.Thread(name='background', target=self.background).start()
        self.handlers()  # set handlers
        self.run()

    @staticmethod
    def background():
        initialize_logger(r'.data')

    def handlers(self):
        # simple handlers
        start_handler = CommandHandler(command="start", callback=Brain.Modules.start, pass_args=True)
        help_handler = CommandHandler(command="help", callback=Brain.Modules.help.get_help, pass_args=True)
        qpapers_handler = CommandHandler(command="qpapers", callback=Brain.Modules.qpapers.get_qpapers)
        stats_handler = CommandHandler(command="stats", callback=Brain.Modules.stats.get_stats)
        feeback_handler = CommandHandler(command="feedback", callback=Brain.Modules.feedback.get_feedback)

        # callback handlers
        help_callback_handler = CallbackQueryHandler(callback=Brain.Modules.help.help_button, pattern=r"help_", )
        qpapers_callback_handler = CallbackQueryHandler(callback=Brain.Modules.qpapers.qpapers_button, pattern=r"qa")

        # set dispatchers
        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(help_handler)
        self.dispatcher.add_handler(stats_handler)
        self.dispatcher.add_handler(feeback_handler)
        self.dispatcher.add_handler(help_callback_handler)
        self.dispatcher.add_handler(qpapers_handler)
        self.dispatcher.add_handler(qpapers_callback_handler)

    def run(self):
        if self.mode == "dev":
            logger.info("Starting Polling Method...")
            self.updater.start_polling(timeout=15, read_latency=4)
        elif self.mode == "prod":
            webhook_url = "https://{}.{}/{}".format(self.APP_NAME, self.domain, self.TOKEN)
            self.updater.start_webhook(listen="0.0.0.0", port=self.PORT, url_path=self.TOKEN)
            self.updater.bot.set_webhook(webhook_url)

            logger.info("Webhook set on {}".format(webhook_url))
        else:
            logger.error("No MODE specified!")
            sys.exit(1)
        self.updater.idle()


if __name__ == '__main__':
    Main()
