from typing import Final 
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import os 

TOKEN: Final = '7709502643:AAHtbgPqzYvJjkWly3dGhf7zAFKvztfRUYs'
bot_username: Final = '@VirtualTrial_sark42_bot'
DOWNLOAD_PATH: Final = r'./downloads/'

# Define states for the conversation
SELECTING_OPTION, GETTING_GARMENT, GETTING_PERSON = range(3)

# Create the directory if it doesn't exist
if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)

# Define options for the user to choose
OPTIONS = [["Garment"], ["Person"]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(OPTIONS, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text('Welcome! Please choose an option:', reply_markup=keyboard)
    return SELECTING_OPTION  # Move to the next state

async def selecting_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()
    
    if 'garment' in user_message:
        await update.message.reply_text("Please send me an image of the garment.")
        return GETTING_GARMENT  # Move to the garment input state
    elif 'person' in user_message:
        await update.message.reply_text("Please send me an image of the person.")
        return GETTING_PERSON  # Move to the person input state
    else:
        await update.message.reply_text("Invalid option. Please choose either 'Garment' or 'Person'.")
        return SELECTING_OPTION  # Stay in the same state

async def handle_garment_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        # Handle photo
        garment_image = update.message.photo[-1]  # Get the highest resolution photo
        await update.message.reply_text("Garment image received! Now please send the image of the person.")
        return GETTING_PERSON  # Move to the person input state
    elif update.message.document:
        # Handle document
        document = update.message.document
        if document.mime_type.startswith('image/'):  # Check if the document is an image
            await update.message.reply_text("Garment image received as a file! Now please send the image of the person.")
            return GETTING_PERSON  # Move to the person input state
        else:
            await update.message.reply_text("This is not an image file! Please send an image.")
            return GETTING_GARMENT  # Stay in the same state
    else:
        await update.message.reply_text("Please send either a photo or a document containing the garment image.")
        return GETTING_GARMENT  # Stay in the same state

async def handle_person_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        # Handle photo
        person_image = update.message.photo[-1]  # Get the highest resolution photo
        await update.message.reply_text("Person image received! Thank you for your submission.")
    elif update.message.document:
        # Handle document
        document = update.message.document
        if document.mime_type.startswith('image/'):  # Check if the document is an image
            await update.message.reply_text("Person image received as a file! Thank you for your submission.")
        else:
            await update.message.reply_text("This is not an image file! Please send an image.")
            return GETTING_PERSON  # Stay in the same state
    else:
        await update.message.reply_text("Please send either a photo or a document containing the person image.")
        return GETTING_PERSON  # Stay in the same state

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Conversation canceled.")
    return ConversationHandler.END  # End the conversation

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    
    # Define the conversation handler with states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECTING_OPTION: [MessageHandler(filters.TEXT, selecting_option)],
            GETTING_GARMENT: [MessageHandler(filters.PHOTO | filters.DOCUMENT, handle_garment_image)],
            GETTING_PERSON: [MessageHandler(filters.PHOTO | filters.DOCUMENT, handle_person_image)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Add the conversation handler to the application
    app.add_handler(conv_handler)

    # Start polling
    app.run_polling()