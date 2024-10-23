from typing import Final 
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os 

TOKEN: Final = '7709502643:AAHtbgPqzYvJjkWly3dGhf7zAFKvztfRUYs'
bot_username: Final = '@VirtualTrial_sark42_bot'
DOWNLOAD_PATH: Final = r'./downloads/'
no_of_images_received=0

# Create the directory if it doesn't exist
if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)


# commands
# start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Display options to the user
    await update.message.reply_text('Welcome to Virtual Trial Bot!')
    await update.message.reply_text('Please send an image contianing Garment.')

# text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    processed_text: str = text.lower()
    if 'yes' in processed_text:
        response: str = 'Please send me an image containing Person.'
    else:
        await update.message.reply_text("Please try again")
        await start_command()

    print('Bot: ', response)
    await update.message.reply_text(response)

# image messages
async def handle_photo_or_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # If the message contains a photo
    if update.message.photo:
        photo = update.message.photo[-1]  # Get the highest resolution photo
        file_id = photo.file_id  # Get file ID
        file = await context.bot.get_file(file_id)
        file_path = os.path.join(DOWNLOAD_PATH, f"{file_id}.jpg")
        await file.download_to_drive(file_path)
        # await update.message.reply_text(f"JPEG image received and saved as {file_path}")
        await update.message.reply_text(r"Received Successfully!")
        await update.message.reply_text('Is it final image of garment? (yes/no)')
        no_of_images_received+=1
        if no_of_images_received<2:
                await update.message.reply_text('Please send an image contianing Person.')
        else:
            await update.message.reply_text('Processing...')
    # If the message contains a document (possibly a PNG or other format)
    elif update.message.document:
        document = update.message.document
        if document.mime_type.startswith('image/'):  # Check if the document is an image
            file_id = document.file_id
            file_extension = document.file_name.split('.')[-1]  # Extract the file extension
            file = await context.bot.get_file(file_id)
            file_path = os.path.join(DOWNLOAD_PATH, f"{file_id}.{file_extension}")
            await file.download_to_drive(file_path)
            # await update.message.reply_text(f"{file_extension.upper()} image received and saved as {file_path}")
            await update.message.reply_text(f"Received Successfully!")
            await update.message.reply_text('Is it final image of garment? (yes/no)')
            no_of_images_received+=1
            if no_of_images_received<2:
                await update.message.reply_text('Please send an image contianing Person.')
            else:
                await update.message.reply_text('Processing...')
        else:
            await update.message.reply_text("This is not an image file!, Please try again.")



# error
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler('start', start_command))

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Photo and document handler (for both JPEG and other images like PNG)
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, handle_photo_or_document))

    # errors
    app.add_error_handler(error)

    # pools the bot
    print('Polling...')
    app.run_polling(poll_interval=3, timeout=20)