from time import sleep
import discord
from discord.ext import commands
from datetime import datetime
from tgtg import TgtgClient
import json
import time

BOT_TOKEN = 'xxx'

client = TgtgClient(email="aaa@aaa.aaa")
credentials = client.get_credentials()

wordlist = ["sushi", "maki", "sashimi", "japan", "japon", "thai"]

url = "https://share.toogoodtogo.com/item/"

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

message_entete = "@here \nNouveau TGTG disponible !\n\n"

messages_envoyes = []

def reload(latitude, longitude, radius):
    items = client.get_items(
        favorites_only=False,
        latitude=latitude,
        longitude=longitude,
        radius=radius,
        page_size=300
    )
    return items

def find_tgtg(items):
    tgtg_items = []
    for item in items:
        if any(word in item["item"]["description"].lower() for word in wordlist) or any(
                word in item["store"]["store_name"].lower() for word in wordlist):
            if item["items_available"] != 0:
                tgtg_items.append(item)
    return tgtg_items

def create_message(item, city_mention):
    msg = message_entete.format(city_mention=city_mention)
    fields = {
        "item_id": ["item", "item_id"],
        "description": ["item", "description"],
        "store_name": ["store", "store_name"],
        "store_id": ["store", "store_id"],
        "address_line": ["store", "store_location", "address", "address_line"],
        "items_available": ["items_available"]
    }
    url = "https://share.toogoodtogo.com/item/" + item["item"]["item_id"] + "\n"
    msg += url
    for field, keys in fields.items():
        try:
            value = item
            for key in keys:
                value = value[key]
            msg += str(value) + "\n"
        except KeyError as e:
            print(f"Error adding {field} to message: {repr(e)}")

    return msg

async def send_message(msg, channel_id):
    channel = bot.get_channel(channel_id)
    await channel.send(msg)

@bot.event
async def on_ready():
    print("Bot is ready")

    cities = {
        #"Rennes": {
        #    "latitude": 48.118437,
        #    "longitude": -1.689145,
        #    "channel_id": 1114550983364706354,
        #    "radius": 6
        #},
        "Paris": {
            "latitude": 48.847869,
            "longitude": 2.373815,
            "channel_id": 1114675342779629578,
            "radius": 4
        },
        "Courbevoie": {
            "latitude": 48.89576456441312,
            "longitude": 2.260528711634343,
            "channel_id": 1173548593366437968,
            "radius": 4
        }
        #"Carpentia": {
        #    "latitude": 44.054847,
        #    "longitude": 5.047753,
        #    "channel_id": 1114684315910017085,
        #    "radius": 10
        #},
        #"Combs-la-ville": {
        #    "latitude": 48.663035, 
        #    "longitude": 2.558027,
        #    "channel_id": 1114847499329474590,
        #    "radius": 10
        #},
        #"Nimes" : {
        #    "latitude": 43.833652,
        #    "longitude": 4.359932, 
        #    "channel_id": 1114850650459746324,
        #    "radius": 5
        #},
        #"Montpellier" : {
        #    "latitude": 43.608237,
        #    "longitude": 3.872608,
        #    "channel_id": 1114850914130477116,
        #    "radius": 5
        #},
        #"Nantes" : {
        #    "latitude": 47.219060,
        #    "longitude": -1.556572,
        #    "channel_id": 1114851672175419496,
        #    "radius": 5
        #},
        #"La Chapelle saint Luc" : {
        #    "latitude": 48.312175,
        #    "longitude": 4.047492,
        #    "channel_id": 1114979545397854248,
        #    "radius": 5
        #},
        #"Aubenas" : {
        #    "latitude": 44.620313,
        #    "longitude": 4.389409,
        #    "channel_id": 1115019806832349204,
        #    "radius": 5
        #},
        #"valences" : {
        #    "latitude": 44.932419,
        #    "longitude": 4.892558,
        #    "channel_id": 1115019899136385076,
        #    "radius": 5
        #},
        #"avignion" : {
        #    "latitude": 43.950071,
        #    "longitude": 4.806296,
        #    "channel_id": 1114851089452372068,
        #    "radius": 6
        #},
        #"Troyes" : {
        #    "latitude": 48.296310,
        #    "longitude": 4.072851,
        #    "channel_id": 1115377811180498944,
        #    "radius": 6
        #},
    }

    while True:
        try:
            for city, city_data in cities.items():
                latitude = city_data["latitude"]
                longitude = city_data["longitude"]
                channel_id = city_data["channel_id"]
                radius = city_data["radius"]
                items = reload(latitude, longitude, radius)
                message = find_tgtg(items)
                if message:
                    for item in message:
                        city_mention = f"<@&{city_data['channel_id']}>"
                        msg = create_message(item, city_mention)
                        if msg not in messages_envoyes:
                            print("new TGTG available in " + city + " !")
                            messages_envoyes.append(msg)
                            await send_message(msg, channel_id)
                    time.sleep(40)
                else:
                    print(f"No TGTG available in {city}")
                time.sleep(40)

        except Exception as e:
            print("Error in on_ready:", repr(e))

bot.run(BOT_TOKEN)
