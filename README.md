# Steam Discount Notifier Telegram Bot

This Telegram bot periodically notifies user when there are games on sale (50% and more) in user's wishlist on Steam.

Warning: At first, you should create a bot by using BotFather. And you should create a Telegram Bot Authorization Token. When you initialize your bot, you use this token. Don't forget to keep your tokens secret.

# Install requiered packages: 
> pip install requests python-dotenv

# Fill values in .env file
The currency exchange rate is taken from the settings (.env file - CURRENCY_EXCHANGE_RATE)

# Start script
> python bot.py

Add script to cron task
