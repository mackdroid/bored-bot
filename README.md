## boredbot
just another discord bot made to learn python
this bots main function is to cache teams meeting links and send them right before the classes start
to setup the bot you need a `settings.py` which contains the token and other stuff as follows
* the discord token `disc_token`
* `guild_id` for slash commands
* `scanchannelid` to specify where to look for the meeting links
* `webhooklink` to send the daily class links (will change later over to discord.py tasks)
* `statusreact` emote to react after successfully changing status through status command.
<details>
<summary>sample settings.py</summary>
```
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_commands import create_permission
vardb = {
    "status_react":  "👌",
    "webhooklink": "https://discord.com/api/webhooks/XXXXXXXXXXXXXXXX/XXXXXXXXXX",
    "prefix": ".",
    "disc_token": "xxxxxxxxxxxxxxxxxxx",
    "guildid": 1234567890,
    "scanchannelid": "1234567890",
}
# refer to https://discord-py-slash-command.readthedocs.io/en/latest/gettingstarted.html?highlight=permission#want-to-restrict-access-setup-permissions for this
permissions={
            vardb["guildid"]: [
                    create_permission(1234567890, SlashCommandPermissionType.ROLE, True),
                    create_permission(1234567890, SlashCommandPermissionType.ROLE, False)
                  ]
}
```
</details>

and dont forget to install the requirements using `pip install -r requirements.txt`

# credits
* [itspacchu](https://github.com/itspacchu) for help with various stuff
* [NoiceNoiceBaby](https://github.com/NoiceNoiceBaby) for the mute command
* and others
