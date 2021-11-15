# ElfBot [![CodeFactor](https://www.codefactor.io/repository/github/elfein7night/elfbot/badge)](https://www.codefactor.io/repository/github/elfein7night/elfbot)
A simple Discord bot for handling Music Bots' spam, built using [`discord.py`](https://discordpy.readthedocs.io/en/stable/), and deployed to [`Heroku`](https://www.heroku.com/).

#### Core Implementation:

- All music related messages are redirected to the server's dedicated music channel.
- All the servers' music channels & prefixes are saved in an online [`Redis`](https://redis.io/) database, which the bot communicates with.


## Usage:

  - Use My Deployed Instance:
    - https://tinyurl.com/GetElfBot
  - Or Deploy Your Own Instance:
    - Self Hosted:
      - Add a file named ```token``` to the utils folder with your bot user token
      - Add a file named ```db_url``` to the utils folder with a ```redis://...``` redis DB URL
      - Run ```elfbot.py```
      - Invite the bot to a server you manage
    - Using `Heroku`:
      - Fork this repo
      - Create a new ```heroku``` app, link it to your fork and enable automatic deploys
      - Under the app's settings add a config var ```DISCORD_BOT_TOKEN``` and give it your bot user token as a value
      - Under the app's resources tab search for and install the ```Redis To Go``` add-on
      - Under the app's resources tab enable the worker
      - Invite the bot to a server you manage
  
  - Go into the designated music spam text channel and enter the command ```?setmusic```
  - Enjoy cleaner text channels without all the spam from music bots related messages :)


###### Quick Demo Of The Filtering Feature:
https://user-images.githubusercontent.com/39451680/117056924-844d8480-ad25-11eb-8e40-e42b9343c0f7.mp4






