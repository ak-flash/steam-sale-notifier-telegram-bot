import os
import requests
from dotenv import load_dotenv


load_dotenv()

CURRENCY_FROM = os.getenv('CURRENCY_FROM')
CURRENCY_TO = os.getenv('CURRENCY_TO')
CURRENCY_EXCHANGE_RATE = float(os.getenv('CURRENCY_EXCHANGE_RATE'))


def telegram_bot_send_message(bot_message):  
	token = os.getenv('BOT_TOKEN')
	chat_id = os.getenv('CHAT_ID')  
	url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={bot_message}&parse_mode=HTML" # Telegram Bot Authorization Token
	requests.get(url).json()

def notify():
    your_wishlist = get_wishlist(os.getenv("STEAM_USER_ID")) # Steam User ID
    games_on_sale = get_games_on_sale(your_wishlist)
    # If there is a game in Wishlist with discount 50% or more, sends game sale info to user
    if len(games_on_sale) > 0:
        games_on_sale_short = shorten_sale_info(games_on_sale)
        title = "<b>The games on your Steam Wishlist are on sale:</b> \n"
        bot_message = title + "\n".join(games_on_sale_short)   
    if bot_message:
        telegram_bot_send_message(bot_message)

# Gets wishlist with Steam API
def get_wishlist(steam_user_id):
    wishlist_endpoint = f"https://store.steampowered.com/wishlist/profiles/{steam_user_id}/wishlistdata/"
    wishlist = requests.get(wishlist_endpoint).json()
    print("Checking wishlist...")
    return wishlist

# Gets which games are on sale from wishlist
def get_games_on_sale(wishlist):
    country_code = os.getenv('COUNTRY_CODE')    
    games_on_sale = []
    for appid in wishlist:
        app_details_endpoint = f"https://store.steampowered.com/api/appdetails?appids={appid}&json=1&&cc={country_code}"
        app_details = requests.get(app_details_endpoint).json()
		
        if app_details[appid]['success'] == True:
            app = app_details[appid]['data']
            print(f"Checking {app['name']}...")
            discount_filter(app, games_on_sale)
    return games_on_sale

# Applies a discount filter for each game in wishlist
def discount_filter(game, filtered_games):
    if game['is_free'] == False and 'price_overview' in game:
        discount_percent = game['price_overview']['discount_percent']
        if discount_percent >= 50:
            filtered_games.append(game)

# Convert game price to another currency using currency exchange rate setting
def convert_price(price):
	converted_price = (int(price) * CURRENCY_EXCHANGE_RATE)/100
	return round(converted_price, 2)
			
def shorten_sale_info(games_on_sale):
    games_info_short = []
    for count, game in enumerate(games_on_sale, 1):
        name = game['name']
        discount = str(game['price_overview']['discount_percent'])
        price = game['price_overview']['final_formatted']
        converted_price = convert_price(game['price_overview']['final'])
        games_info_short.append(f"{count}) <b>{name}</b> - {price} (<b>{converted_price}</b> {CURRENCY_TO}) -{discount}%")
    return games_info_short


def main():
    notify()

if __name__ == '__main__':
    main()
