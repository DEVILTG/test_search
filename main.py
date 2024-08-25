import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, Updater

# Replace this with your bot's API key
API_KEY = '1535629893:AAGVZey0Otk_c28NfEw7HDcl99eFmmVutKk'
MONGO_DB_URL = 'https://ap-south-1.aws.data.mongodb-api.com/app/data-xluhn/endpoint/data/v1'

def store_user_details(user):
    url = MONGO_DB_URL
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=user, headers=headers)
    return response.status_code

def get_users_count():
    url = MONGO_DB_URL
    response = requests.get(url)
    data = response.json()
    return data.get('count', 0)

def post_channel_member_ids(api_key, channel_id, log_channel_id):
    url = f'https://api.telegram.org/bot{api_key}/getChatMembers?chat_id={channel_id}'
    response = requests.get(url)
    response_data = response.json()

    if response_data.get('ok'):
        channel_members = response_data.get('result', [])
        member_ids = [member['user']['id'] for member in channel_members]
        log_message = f"Channel Member IDs: {', '.join(map(str, member_ids))}"
        send_message(api_key, log_channel_id, log_message)
    else:
        print('Error fetching channel members:', response_data.get('description'))

def forward_single_file(api_key, target_user_id, message_id):
    url = f'https://api.telegram.org/bot{api_key}/forwardMessage?chat_id={target_user_id}&from_chat_id={-1001884459703}&message_id={message_id}'
    response = requests.get(url)
    response_data = response.json()

    if not response_data.get('ok'):
        print('Error forwarding message:', response_data)

def start(update: Update, context):
    user_firstname = update.message.from_user.first_name
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    log_channel = -1002112825078
    owner_id = 1113520934

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('Add Bot to Group', url='https://t.me/Animelover_Devil_bot?startgroup=true'),
            InlineKeyboardButton('Join Group', url='https://t.me/Devils_Territory'),
        ],
        [
            InlineKeyboardButton('Join Channel', url='https://t.me/Anime_World_Territory'),
            InlineKeyboardButton('Help', callback_data='/help'),
        ],
        [
            InlineKeyboardButton('Cross & Paid Promotions', callback_data='/promotions'),
        ],
    ])

    response = f"🎉 Hello {user_firstname}! Welcome to the Anime Bot adventure! 🌟\n\n" \
               "Immerse yourself in the world of anime with the help of @anime_world_territory. " \
               "Type 'naruto' to get a link to Naruto or explore more by searching other anime titles! 🚀\n\n" \
               "You can also use '/search' to search for a specific anime. Example: '/search naruto'."
    
    context.bot.send_message(chat_id=chat_id, text=response, reply_to_message_id=message_id, reply_markup=keyboard)
    log_message = f"👤 New user started the bot: {user_firstname} (ID: {user_id})"
    context.bot.send_message(chat_id=log_channel, text=log_message)

    user_details = {
        'id': user_id,
        'username': update.message.from_user.username,
        'name': f"{user_firstname} {update.message.from_user.last_name or ''}"
    }
    store_user_details(user_details)

def help_command(update: Update, context):
    response = "ℹ️ **Anime Bot Help**\n\n1. Use '/start' to begin the adventure.\n2. Type the name of an anime (e.g., 'naruto') to get a link on Telegram.\n3. Use '/search' to search for an anime. Example: '/search naruto'."
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def main():
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
