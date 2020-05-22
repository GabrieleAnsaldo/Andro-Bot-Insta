import action
import schedule
import random
from time import sleep
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help! The bot stopped!!')

def run(update, context):
    update.message.reply_text("Happy to run!")
    my_hashtags = ["\#beautifuldestinations", "\#travelphotography", "\#capture", "\#photographylovers", "\#lightroom", "\#justgoshoot", "\#wonderful_places", 
                   "\#50mm", "\#35mm", "\#35mmfilm", "\#nakedplanet", "\#letsgoeverywhere", "\#doyoutravel", "\#exploretocreate", "\#photographer", 
                   "\#sunsetphotography", "\#travelblogger", "\#traveltheworld", "\#traveladdict", "\#naturephotography", "\#traveldestination", 
                   "\#peoplescreatives", "\#collectivelycreate", "\#sonya7iii", "\#moodygrams", "\#photographyeveryday", "\#photographysouls", "\#artofvisuals", 
                   "\#globalcapture", "\#visualambassadors", "\#discoverportrait", "\#portraitphotography", "\#portraitmood", "\#pursuitofportrait", 
                   "\#awesome_earthpix", "\#awesomeglobe", "\#beautifullandscape", "\#getlost", "\#architecturephotography"]
    n_likes = 54
    n_hashtags = 3

    def job():
        update.message.reply_text("Starting Instagram")
        print("Starting Instagram")
        action.close_insta()
        action.open_insta()
        
        for x in range (1, n_hashtags +1):
            hashtag = random.choice(my_hashtags)
            update.message.reply_text("[" + hashtag + "] hashtag #" + str(x))
            print("###[" + hashtag + "]###")
            action.hashtag_util(hashtag) 
            [n, n_mis] = action.like(n_likes)
            update.message.reply_text("Liked " + str(n) + " posts,")
            update.message.reply_text(" with " + str(n_mis) + " errors.")
            
        update.message.reply_text("Closing Instagram")
        print("Closing Instagram")
        action.close_insta()

        update.message.reply_text("Sleeping...")

    # Choose your scheduling times
    #schedule.every(5).minutes.at(":50").do(job)
    schedule.every().day.at("20:48").do(job)
    schedule.every().day.at("22:46").do(job)
    schedule.every().day.at("01:23").do(job)
    schedule.every().day.at("03:13").do(job)
    schedule.every().day.at("06:07").do(job)
    schedule.every().day.at("09:29").do(job)
    schedule.every().day.at("11:52").do(job)
    schedule.every().day.at("13:46").do(job)
    
    
    while True:
        schedule.run_pending()
        sleep(1)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("YOUR_TOKEN", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("run", run))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    #dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
