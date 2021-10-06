import discord

def retclasslinks(title,desc,cl):
    classlinkembed = discord.Embed(title=title, description = desc)
    if len(cl) == 0:
        classlinkembed.add_field(name="Ive got no links, no classes i guess", value="¯\_(ツ)_/¯")
    else:
        for i in cl:
            mytitle = i[:i.find('http')]
            print(len(mytitle))
            if(len(mytitle) == 0):
               mytitle = "Class Link(no title found)"
            classlinkembed.add_field(name='> ' + mytitle ,value=i[i.find('http'):] + '\n\n', inline=False)
    return classlinkembed
    