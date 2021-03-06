from functions import groups,search,logger,config
import re
import discord
import pprint

DESC="Softban member or ID (Ban and unban to clean messages)"
USAGE="softban [member]"

async def init(bot):
    chat=bot.message.channel
    #user=str(bot.message.author.name)
    try:
        if len(bot.args)>0:
            if len(bot.message.raw_mentions)>0:
                user = await search.user(chat, bot.message.raw_mentions[0])
            else:
                user = " ".join(bot.args)
                if user.startswith("@"):
                    user = user[1:]
                user = await search.user(chat, user)
            if user is None:
                uid = ''.join(bot.args)
                if re.match("\d+",uid):
                    user = discord.Object(id=uid)
                    user.server = bot.message.server
                else:
                    await bot.sendMessage( ":x: {} is not a valid User or ID".format(uid))
            try:
                if user is not None:
                    await bot.client.ban(user, delete_message_days=1)
                    await bot.client.unban(bot.message.server, user)
                    await bot.sendMessage( ":white_check_mark: Softbanned <@{0.id}> (**ID:** {0.id})".format(user))

            except discord.Forbidden:
                await bot.sendMessage( ':x: The bot does not have permissions to ban members or this user got higher rank than the bot.')
            except discord.NotFound:
                await bot.sendMessage( ':x: This user doesn\'t exist or (s)he deleted this account.')
            except:
                logger.PrintException(bot.message)
        else:
            await bot.sendMessage( "I can't ban nothing.")
    except Exception:
        logger.PrintException(bot.message)
        return False
