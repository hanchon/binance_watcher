import logging

from telegram import Bot
from telegram.ext import CommandHandler
from telegram.ext import Updater

from config import API_KEY_TELEGRAM

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
subscribers = [-507154072]


class Alerter:
    def __init__(self) -> None:
        self.updater = Updater(token=API_KEY_TELEGRAM, use_context=True)
        self.bot = Bot(token=API_KEY_TELEGRAM)
        self.subscribers = []
        # Get the dispatcher to register handlers
        self.dp = self.updater.dispatcher

        # on different commands - answer in Telegram
        self.dp.add_handler(CommandHandler('start', self.start))
        self.dp.add_handler(CommandHandler('stop', self.stop))
        self.dp.add_handler(CommandHandler('help', self.help))

        # # on noncommand i.e message - echo the message on Telegram
        # self.dp.add_handler(MessageHandler(Filters.text, echo))

        # log all errors
        self.dp.add_error_handler(self.error)

    def run_the_bot(self):
        self.updater.start_polling()
        emoji = '\U0001F680'
        self.broadcast(f'Bot reiniciado {emoji}')
        self.updater.idle()

    def start(self, update, context):
        """Send a message when the command /start is issued."""
        self.subscribers.append(update.message.chat_id)
        update.message.reply_text('Te llegarán las alertas kpo!')

    def stop(self, update, context):
        i = 0
        while i < len(self.subscribers):
            if self.subscribers[i] == update.message.chat_id:
                del self.subscribers[i]
                break
            i = i + 1

    def help(self, update, context):
        """Send a message when the command /help is issued."""
        update.message.reply_text('Instrunctions /start to subscribe, /stop to unsubscribe')

    def echo(self, update, context):
        """Echo the user message."""
        update.message.reply_text(update.message.text)

    def error(self, update, context):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    def broadcast(self, msg):
        for id in subscribers:
            self.bot.send_message(id, text=msg)
