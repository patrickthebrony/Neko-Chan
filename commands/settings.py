from functions import logger, search, startup
import discord
import asyncio
import os
import aiohttp
import global_vars
import datetime

DESC="Change bots client settings"
USAGE="settings (setting) [new value]"

async def init(bot):
    try:
        if len(bot.args)>0:
            setting = bot.args[0].lower()
            bot.args.pop(0)
            # Setting a new avatar
            if setting=="avatar":
                if len(bot.args)>0:
                    avatar = "%20".join(bot.args)
                    #that doesnt work lol
                    #if name.lower()=="none":
                    #    await bot.client.edit_profile(avatar=None)
                    #else:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(avatar) as r:
                            if r.headers['CONTENT-TYPE'].lower() != "image/jpeg" and r.headers['CONTENT-TYPE'].lower() != "image/png":
                                await bot.sendMessage( "Only jpeg and png images can be used as avatar.")
                                pass
                            await bot.client.edit_profile(avatar=await r.read())
                    await bot.sendMessage( ":white_check_mark: New avatar set.")
                else:
                    await bot.sendMessage( "Avatar: {}\r\nYou can use an url as second argument to set a new avatar.".format(bot.client.user.avatar_url))
            # Sets new default levels
            elif setting=="levels":
                #await bot.sendMessage( ":stopwatch: Reinitiating default access levels.\r\nThis could take a while.")
                await startup.defaultLevels()
                await bot.sendMessage( ":white_check_mark: Re-initiated default access levels.")
            # Changing the name
            elif setting=="name":
                if len(bot.args)>0:
                    name = " ".join(bot.args)
                    myself = bot.message.server.me
                    if myself is not None:
                        if name.casefold() == "none":
                            name = None
                        # Bot needs permissions for this!
                        ###await bot.client.change_nickname(myself, name)
                        await bot.client.edit_profile(username=name) # Changes the actual username
                        await bot.sendMessage( "New name set.")
                else:
                    await bot.sendMessage( "Name: {}\r\nYou can give a new name as second argument.".format(bot.client.user.name))
            # Changing the game playing
            elif setting=="game":
                if len(bot.args)>0:
                    g_name = " ".join(bot.args)
                    if g_name.lower()=="none":
                        g_name = None
                    await bot.client.change_status(game=discord.Game(name=g_name))
                    global_vars.game = g_name
                    cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    contents = "#Auto-Generated by bot on {}\n".format(cur_time)
                    with open("global_vars.py", "rb") as f:
                        for line in f.readlines():
                            line = format(line.decode("ascii"))
                            # Ignore comments
                            if line.startswith("#"):
                                continue;
                            # Re-Write the line if it states the game
                            if line.startswith("game"):
                                if g_name is not None:
                                    line = "game = \"{}\"\n".format(g_name)
                                else:
                                    line = "game = {}\n".format(g_name)
                            # Write everything to a temp var
                            if line != "\n" and line != "\r" and line != "\r\n":
                                contents+=line
                    # Write the temp var to file
                    with open("global_vars.py", "wb") as f:
                        f.write(contents.encode("ascii"))

                    await bot.sendMessage( ":white_check_mark: New game set.")
                else:
                    await bot.sendMessage( "Game: {}\r\nYou can give a new game as second argument.".format(global_vars.game))
            # Changing the game playing
            elif setting=="server":
                if len(bot.args)>0:
                    #something
                    pass
                else:
                    data = "Servers: {}\r\n".format(len(bot.client.servers))
                    limit = 20
                    for server in bot.client.servers:
                        if limit > 0:
                            data += "- {} ({})\r\n".format(server.name, server.id)
                        else:
                            data += "..."
                            break;
                        limit-=1;
                    await bot.sendMessage( "{}".format(data))
            else:
                await bot.sendMessage( ":x: Unknown setting: {}".format(setting))
        else:
            await bot.sendMessage("""Available Settings:
- avatar
- name
- game""")
    except:
        logger.PrintException(bot.message)
