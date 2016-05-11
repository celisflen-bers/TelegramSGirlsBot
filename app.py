#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent
from telegram.ext import Updater, CommandHandler, \
    MessageHandler, Filters, InlineQueryHandler
import logging, requests, urllib2
import json, re
import secrets
from random import randint
from uuid import uuid4

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

headers = {
    'User-Agent': 'sgirlsbot Telegram bot (by /u/rogergonzalez21)',
    'From': 'rogergonzalez21@gmail.com'
    }

def get_data(string):
    r = requests.get(string, headers=headers)

    data = r.json()

    result = []

    for child in data['data']['children']:
        result.append({'title' : child['data']['title'], 'url' : child['data']['url'], 'thumb' : child['data']['thumbnail']})
    return result


def search(bot, update):
    query = update.inline_query.query
    results = list()
    suicide_list = get_data(r'http://www.reddit.com/r/suicidegirls/search.json?q=title:%s+site:imgur.com+nsfw:yes+subreddit:suicidegirls'%(query))

    for suicide in suicide_list:
        if not suicide['url'].endswith('.jpg'):
            suicide['url'] = suicide['url'] + '.jpg'
        results.append(InlineQueryResultArticle(
            id=uuid4(),
            title=suicide['title'],
            thumbs_url=suicide['thumb'],
            url=suicide['url']))

    bot.answerInlineQuery(update.inline_query.id, results=results)


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text="Hi! To get a random suicide girl, type <b>/random</b>. To get a specific Suicide Girl, type /suicide 'name'. For example, <b>/suicide bixton</b>. Enjoy!", parse_mode=telegram.ParseMode.HTML)

def help(bot, update):
    bot.sendMessage(update.message.chat_id, text="To get a random suicide girl, type <b>/random</b>. To get a specific Suicide Girl, type /suicide 'name'. For example, <b>/suicide bixton</b>.", parse_mode=telegram.ParseMode.HTML)

def url_check(url):
    re_url = re.compile(r"^https?:")
    if not re_url.match(url):
        url = url.lstrip()
    re_image = r_image = re.compile(r".*\.(jpg|png|gif)$")
    if not r_image.match(url):
        url = url + '.jpg'
    return url

def file_check(url):
    ret = urllib2.urlopen(url)
    if ret.code == 200:
        return True
    elif ret.code != 200:
        return False

def random(bot, update):
    suicides = get_data(r'https://www.reddit.com/r/suicidegirls/search.json?q=&restrict_sr=on&sort=relevance&t=all&limit=100')#all_suicides()

    while True:
        random_suicide = suicides[randint(0,len(suicides))]

        # URL check
        print 'Title: {title}\n\t URL: {url}\n\t thumb: {thumb}'.format(title=random_suicide['title'], url=random_suicide['url'], thumb=random_suicide['thumb'])
        url = url_check(random_suicide['url'].decode('utf-8'))

        # File check
        fck = file_check(url)
        if fck == False:
            break

    # Error in URL file, cause fail in sendPhoto
    bot.sendPhoto(chat_id=update.message.chat_id, photo=url.encode('utf-8'), caption=random_suicide['title'])
    #bot.sendMessage(chat_id=update.message.chat_id, text="{title}\n {url}".format(title=random_suicide['title'], url=url))

def suicide(bot, update):
    suicide = update.message.text[9:]
    if suicide == '':
        echo(bot, update)
    else:
        suicide_list = get_data(r'http://www.reddit.com/r/suicidegirls/search.json?q=title:%s+site:imgur.com+nsfw:yes+subreddit:suicidegirls'%(suicide))#search_suicides(suicide)
        if len(suicide_list) == 0:
            bot.sendMessage(update.message.chat_id, text="I couldn't find any pictures of %s. Sorry :(" %suicide)
        else:
            random_suicide = suicide_list[randint(0,len(suicide_list)-1)]

        while True:
            random_suicide = suicide_list[randint(0,len(suicides))]

            # URL check
            print 'Title: {title}\n\t URL: {url}\n\t thumb: {thumb}'.format(title=random_suicide['title'], url=random_suicide['url'], thumb=random_suicide['thumb'])
            url = url_check(random_suicide['url'].decode('utf-8'))

            # File check
            fck=file_check(url)
            if fck == False:
                break

            # Error in URL file, cause fail
            bot.sendPhoto(chat_id=update.message.chat_id, photo=url.encode('utf-8'), caption=random_suicide['title'])
            #bot.sendMessage(chat_id=update.message.chat_id, text="{title}\n {url}".format(title=random_suicide['title'], url=url))

def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text="Please, use /random or /suicide 'name'")

def developer(bot, update):
    bot.sendMessage(update.message.chat_id, text='Made by @Rogergonzalez21. GitHub repo: https://github.com/Rogergonzalez21/TelegramSGirlsBot')

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"\n' % (update, error))

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

    # inline query
    dp.addHandler(InlineQueryHandler(search))


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
