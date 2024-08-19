#!/usr/bin/env python3

import spacy
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler


nlp = spacy.load('en_core_web_md')

with open('hELO_Support.txt', 'r', encoding='utf-8') as file:
    Support_text = file.read()
Support_doc = nlp(Support_text)


def train_bot(user_doc, Support_doc):
    """Find a relevant section in the document based on the user's input."""
    most_similar_section = None
    highest_similarity = 0

    for sent in Support_doc.sents:
        similarity = user_doc.similarity(sent)
        if similarity > highest_similarity:
            highest_similarity = similarity
            most_similar_section = sent.text
    return most_similar_section


async def state0_handler(update, context):
    """Handle user input in state0 using SpaCy."""
    user_text = update.message.text
    user_doc = nlp(user_text)
    reply = train_bot(user_doc, Support_doc)
    if reply:
        await update.message.reply_text(reply)
    return 'STATE0'


async def start(update, context):
    """Start the conversation with a welcome message."""
    await update.message.reply_text("Hi! I am your bot. How may I be of service?")
    return 'STATE0'


async def cancel(update, context):
    """Gracefully exit the conversation."""
    await update.message.reply_text("Thanks for the chat. I'll be off then!")
    return ConversationHandler.END


async def help(update, context):
    """Provide help information."""
    await update.message.reply_text("The help needs to go here.")
    return


def main():
    """Set up and run the bot."""
    application = Application.builder().token('7483517597:AAHhZ2kMTstPBJ9GUGUBNodZUYlldwYwDtE').build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            'STATE0': [MessageHandler(filters.TEXT & ~filters.COMMAND, state0_handler)],
        },
        fallbacks=[CommandHandler('cancel', cancel), CommandHandler('help', help)]
    )
    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
