## boredbot
just another discord bot made to learn python
this bots main function is to cache teams meeting links and send them right before the classes start
to setup the bot you need a `settings.py` which contains the token and other stuff
* the discord token `disc_token`
* `guild_id` and `admin_role` for mute and unmute command
* `scanchannelid` to specify where to look for the meeting links
* `webhooklink` to send the daily class links (will change later over to discord.py tasks)
* `statusreact` emote to react after successfully changing status through status command.

and dont forget to install the requirements using `pip install -r requirements.txt`

# credits
* [itspacchu](https://github.com/itspacchu) for help with various stuff
* [NoiceNoiceBaby](https://github.com/NoiceNoiceBaby) for the mute command
* and others