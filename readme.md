# TGTG-discord-bot 

Too Good To Go is an app that serves to avoid waste.
With the help of an api, you can find a discord bot allowing you to buy sushi for cheap!

## Make it work ! 

Clone the repo:
``` git clone https://github.com/Momollax/TGTG-discord-bot.git```
create a discord bot, and add his key here:``` BOT_TOKEN = 'xxxxx'```
create a Too Good To Go account, and past your email here:
``` client = TgtgClient(email="exemple@gmail.com")```

add your city, add the lagitude, longitude with google map
and add the chanel where the bot whant to speak
radius is for kilometer arount the point.

``` "Rennes": {
            "latitude": 48.118437,
            "longitude": -1.689145,
            "channel_id": 1114550983364706354,
            "radius": 6
        },
```
you can modify the wordlist, if you whant pizza, panini, burger, ect ect ...
