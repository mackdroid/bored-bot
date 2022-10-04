## bored-bot
just another discord bot made to learn python
this bots main function is to cache teams meeting links and send them right before the classes start
to setup the bot you need a `settings.py` which contains the token and other stuff as follows
* the discord token `disc_token`
* `prefix` for commands
<details>
<summary>sample settings.json</summary>

```json
{
    "prefix": ".",
    "disc_token": "xxxxxxxxxxxxxxxxxxx",
}
```

</details>

This project uses [poetry](https://python-poetry.org/) to manage dependencies, run
```poetry install```
to install required dependencies

# credits
* [itspacchu](https://github.com/itspacchu) for help with various stuff
* and others
