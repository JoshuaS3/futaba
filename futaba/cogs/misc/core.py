#
# cogs/misc/core.py
#
# futaba - A Discord Mod bot for the Programming server
# Copyright (c) 2017-2018 Jake Richardson, Ammon Smith, jackylam5
#
# futaba is available free of charge under the terms of the MIT
# License. You are free to redistribute and/or modify it under those
# terms. It is distributed in the hopes that it will be useful, but
# WITHOUT ANY WARRANTY. See the LICENSE file for more details.
#

'''
Cog for misceallaneous commands that don't really belong anywhere else.
'''

import asyncio
import logging
from datetime import datetime

import discord
from discord.ext import commands

from futaba import permissions
from futaba.enums import Reactions

logger = logging.getLogger(__name__)

__all__ = [
    'Miscellaneous',
]

class Miscellaneous:
    __slots__ = (
        'bot',
        'journal',
    )

    def __init__(self, bot):
        self.bot = bot
        self.journal = bot.get_broadcaster('/misc')

    @commands.command(name='ping')
    async def ping(self, ctx):
        '''
        Determines the bot's current latency.
        '''

        duration = datetime.now() - discord.utils.snowflake_time(ctx.message.id)
        ms = duration.microseconds / 1000

        await asyncio.gather(
            Reactions.SUCCESS.add(ctx.message),
            ctx.send(content=f"Pong! (`{ms} ms`)")
        )

    @commands.command(name='shutdown', aliases=['halt'])
    @permissions.check_owner()
    async def shutdown(self, ctx):
        '''
        Shuts down the bot. Only able to be run by an owner.
        '''

        self.journal.send('admin/shutdown', ctx.guild, 'Shutting down bot', icon='shutdown')
        await Reactions.SUCCESS.add(ctx.message)
        exit()
