#! /usr/bin/python3
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, RegexHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from convertFuncs import *
import logging

REQUEST_KWARGS={
    #set proxy (here we used tor as default)
    'proxy_url': 'socks5://localhost:9050',
    'urllib3_proxy_kwargs': {
        'username': '',
        'password': '',
    }
}
bot_token = 'Your Token Bot'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
GET_PHOTO, CHOOSE_EFFECT = range(2)

updater = Updater(token=bot_token, request_kwargs=REQUEST_KWARGS)
dispatcher = updater.dispatcher

def switcher(choosed_effect, img_addr, uid):
    switch = {
        '1': black_and_white(img_addr, uid),
        '2': gaussian_blur(img_addr, uid),
        '3': sobel_filter(img_addr, uid),
        '4': cartoon_effect(img_addr, uid),
        '5': edges_effect(img_addr, uid)
    }

def just_little_helper(bot, update):
    update.message.reply_text('Send Photo Dude')
    return GET_PHOTO

def get_photo(bot, update):
    user = update.message.from_user
    chat_id = str(update.message.chat_id)
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    photo_file.download('{}.jpg'.format(chat_id))
    logger.info('Get photo from user')
    update.message.reply_text('OKAY, Sexy.\nNow Choose an effect number to make your image.\n1: black and white\n2: gaussian blur\n3: sobel filter\n4: cartoon effect\n5: edges effect')

    return CHOOSE_EFFECT

def choose_effect(bot, update):
    user = update.message.from_user
    chat_id = str(update.message.chat_id)

    effect_number = update.message.text
    logger.info('get effect number from user', effect_number, type(effect_number))
    switcher(effect_number, './{}.jpg'.format(chat_id), chat_id)
    bot.send_document(update.message.chat_id, document=open('{}_effect.png'.format(chat_id), 'rb'))

    return ConversationHandler.END

def start(bot, update):
    user = update.message.from_user
    update.message.reply_text('Start button pushed!')

def cancel(bot, update):
    user = user.message.from_user
    update.message.reply_text('Hope to see ya again.')
    return ConversationHandler.END

updater.dispatcher.add_handler(CommandHandler('start', start))

conv_handler = ConversationHandler(
    entry_points = [CommandHandler('go', just_little_helper)],

    states = {
        GET_PHOTO: [MessageHandler(Filters.photo, get_photo)],
        CHOOSE_EFFECT: [MessageHandler(Filters.text, choose_effect)]
    },
    fallbacks = [CommandHandler('cancel', cancel)]
)

dispatcher.add_handler(conv_handler)


updater.start_polling()
print('Bot started...')
updater.idle()
updater.stop()
