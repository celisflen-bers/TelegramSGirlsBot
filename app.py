from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests
import json
import secrets
from random import randint

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

headers = {
    'User-Agent': 'sgirlsbot Telegram bot (by /u/rogergonzalez21)',
    'From': 'rogergonzalez21@gmail.com'
    }

def all_suicides():
    r = requests.get(r'https://www.reddit.com/r/suicidegirls/search.json?q=&restrict_sr=on&sort=relevance&t=all&limit=100', headers=headers)

    data = r.json()

    suicides = []

    for child in data['data']['children']:
        suicides.append({'title' : child['data']['title'], 'url' : child['data']['url']})
    return suicides

def search_suicides(suicide):
    r = requests.get(r'http://www.reddit.com/r/suicidegirls/search.json?q=title:%s+site:imgur.com+nsfw:yes+subreddit:suicidegirls'%(suicide), headers=headers) 

    data = r.json()
    suicide = []
    for child in data['data']['children']:
        suicide.append({'title' : child['data']['title'], 'url' : child['data']['url']})

    return suicide

def start(bot, update):
    bot.sendMessage(update.message.chat_id, text="Hi! To get a random suicide girl, type <b>/random</b>. To get a specific Suicide Girl, type /suicide 'name'. For example, <b>/suicide bixton</b>. Enjoy!", parse_mode=telegram.ParseMode.HTML)

def help(bot, update):
    bot.sendMessage(update.message.chat_id, text="To get a random suicide girl, type <b>/random</b>. To get a specific Suicide Girl, type /suicide 'name'. For example, <b>/suicide bixton</b>.", parse_mode=telegram.ParseMode.HTML)

def random(bot, update):
    suicides = all_suicides()
    random_suicide = suicides[randint(0,len(suicides))]
    if random_suicide['url'].endswith('.jpg'):
            url = random_suicide['url']
    else:
        url = random_suicide['url'] + '.jpg'
    bot.sendMessage(chat_id=update.message.chat_id, text="{title}\n {url}".format(title=random_suicide['title'], url=url))
    #bot.sendPhoto(chat_id=update.message.chat_id, photo=url, caption=random_suicide['title'])

def suicide(bot, update):
    suicide = update.message.text[9:]
    if suicide == '':
        echo(bot, update)
    else:
        suicide_list = search_suicides(suicide)
        if len(suicide_list) == 0:
            bot.sendMessage(update.message.chat_id, text="I couldn't find any pictures of %s. Sorry :(" %suicide)
        else:
            random_suicide = suicide_list[randint(0,len(suicide_list)-1)]
            if random_suicide['url'].endswith('.jpg'):
                url = random_suicide['url']
            else:
                url = random_suicide['url'] + '.jpg'
            bot.sendMessage(chat_id=update.message.chat_id, text="{title}\n {url}".format(title=random_suicide['title'], url=url))
            #bot.sendPhoto(chat_id=update.message.chat_id, photo=url, caption=random_suicide['title'])

def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text="Please, use /random or /suicide 'name'")

def developer(bot, update):
    bot.sendMessage(update.message.chat_id, text='Made by @Rogergonzalez21. GitHub repo: https://github.com/Rogergonzalez21/TelegramSGirlsBot')

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(secrets.bot_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addHandler(CommandHandler("start", start))
    dp.addHandler(CommandHandler("help", help))
    dp.addHandler(CommandHandler("random", random))
    dp.addHandler(CommandHandler("suicide", suicide))
    dp.addHandler(CommandHandler("developer", developer))


    # on noncommand i.e message - echo the message on Telegram
    dp.addHandler(MessageHandler([Filters.text], echo))

    # log all errors
    dp.addErrorHandler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
