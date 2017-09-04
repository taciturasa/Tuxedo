# MODERATION FOR TUXEDO
# (c) ry000001 2017
# This code will *only* work on Tuxedo Discord bot.
# This code is free and open source software. Feel free to leak.
import discord
from discord.ext import commands
from discord import utils as dutils
from utils import switches
import asyncio
import random
chars = '!#/()=%&'

alert_disabled = [110373943822540800]

class Moderation:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mute(self, ctx, member : discord.Member):
        """Mutes or unmutes a member"""
        if ctx.author == member:
            return await ctx.send('Why are you trying to mute yourself...?')
        if not ctx.author.permissions_in(ctx.channel).manage_roles:
            return await ctx.send(':no_entry_sign: Not enough permissions. You need Manage Roles.')
        if not ctx.me.permissions_in(ctx.channel).manage_roles:
            return await ctx.send(':no_entry_sign: Grant the bot Manage Roles before doing this.')
        for i in ctx.guild.text_channels:
            await i.set_permissions(member, send_messages=not member.permissions_in(i).send_messages)
        await ctx.send(':ok_hand:')

    @commands.command()
    async def ban(self, ctx, member : discord.Member, *, reason : str = None):
        """Bans a member. You can specify a reason."""
        if ctx.author == member:
            return await ctx.send('Don\'t ban yourself, please.')
        if not ctx.author.permissions_in(ctx.channel).ban_members:
            return await ctx.send(':no_entry_sign: Not enough permissions. You need Ban Members.')
        if not ctx.me.permissions_in(ctx.channel).ban_members:
            return await ctx.send(':no_entry_sign: Grant the bot Ban Members before doing this.')
        if ctx.author.top_role <= member.top_role:
            return await ctx.send(':no_entry_sign: You can\'t ban someone with a higher role than you!')
        if ctx.me.top_role <= member.top_role:
            return await ctx.send(':no_entry_sign: I can\'t ban someone with a higher role than me!')
        await ctx.guild.ban(member, reason=f'[{str(ctx.author)}] {reason}' if reason else f'Ban by {str(ctx.author)}', delete_message_days=7)
        await ctx.send(':ok_hand:')

    @commands.command()
    async def kick(self, ctx, member : discord.Member, *, reason : str = None):
        """Kicks a member. You can specify a reason."""
        if ctx.author == member:
            return await ctx.send('Don\'t kick yourself, please.')
        if not ctx.author.permissions_in(ctx.channel).kick_members:
            return await ctx.send(':no_entry_sign: Not enough permissions. You need Kick Members.')
        if not ctx.me.permissions_in(ctx.channel).kick_members:
            return await ctx.send(':no_entry_sign: Grant the bot Kick Members before doing this.')
        if ctx.author.top_role <= member.top_role:
            return await ctx.send(':no_entry_sign: You can\'t kick someone with a higher role than you!')
        if ctx.me.top_role <= member.top_role:
            return await ctx.send(':no_entry_sign: I can\'t kick someone with a higher role than me!')
        await ctx.guild.kick(member, reason=f'[{str(ctx.author)}] {reason}' if reason else f'Kick by {str(ctx.author)}')
        await ctx.send(':ok_hand:')


    @commands.command()
    async def dehoist(self, ctx, member : discord.Member, *, flags : str = None):
        if not ctx.author.permissions_in(ctx.channel).manage_nicknames:
            return await ctx.send(':no_entry_sign: Not enough permissions. You need Manage Nicknames.')
        if not ctx.me.permissions_in(ctx.channel).manage_nicknames:
            return await ctx.send(':no_entry_sign: Grant the bot Manage Nicknames before doing this.')
        if ctx.author == member:
            return await ctx.send('Nope, can\'t do this.')
        name = member.nick if member.nick else member.name
        if name.startswith(tuple(chars)):
            try:
                await member.edit(nick=f'z {name}') # z is temporary
            except discord.Forbidden:
                await ctx.send('Oops. I can\'t dehoist this member because my privilege is too low. Move my role higher.')
            else:
                await ctx.send(':ok_hand:')
        else:
            await ctx.send('I couldn\'t dehoist this member. Either they weren\'t hoisting or this character isn\'t supported yet.')

    def cleanformat(self, number):
        string = ""
        if number == 1:
            string = "deleted 1 message"
        if number == 0:
            string = "deleted no messages"
        else:
            string = "deleted {} messages".format(number)
        return "Bot cleanup successful, {} (Method A)".format(string)

    def pruneformat(self, number):
        string = ""
        if number == 1:
            string = "Deleted 1 message"
        if number == 0:
            string = "Deleted no messages"
        else:
            string = "Deleted {} messages".format(number)
        return string

    @commands.command(description="Clean up the bot's messages.")
    async def clean(self, ctx, amount : int=50):
        """Clean up the bot's messages."""
        def checc(msg):
            return msg.author == self.bot.user

        if ctx.channel.permissions_for(ctx.guild.me).manage_messages:
            delet = await ctx.channel.purge(limit=amount+1, check=checc, bulk=True)
            eee = await ctx.send(self.cleanformat(len(delet)))
            await asyncio.sleep(3)
            return await eee.delete()
        else:
            async for i in ctx.channel.history(limit=amount): # bugg-o
                if i.author == self.bot.user:
                    await i.delete()
            
            uwu = await ctx.send("Bot cleanup successful (Method B)")
            await asyncio.sleep(3)
            return await uwu.delete()

    @commands.command(description="Purge messages in the channel.", aliases=["prune"])
    async def purge(self, ctx, amount : int=50, *flags):
        if not ctx.author.permissions_in(ctx.channel).manage_messages:
            return await ctx.send(":x: Not enough permissions.")

        if not ctx.me.permissions_in(ctx.channel).manage_messages:
            return await ctx.send(":x: I don't have enough permissions.")
        
        meme = switches.parse(' '.join(flags))
        bots = (lambda: 'bots' in meme[0])()

        if not bots:
            await ctx.message.delete()

        delet = await ctx.channel.purge(limit=amount, check=lambda a: a.author.bot if bots else True, bulk=True) # why is it bugged  
        eee = await ctx.send(self.pruneformat(len(delet)))
        await asyncio.sleep(3)
        return await eee.delete()

    @commands.command(description="Ban a user, even when not in the server.", aliases=['shadowban'])
    async def hackban(self, ctx, user : int, *, reason : str = None):
        'Ban someone, even when not in the server.'
        if not ctx.author.permissions_in(ctx.channel).ban_members:
            return await ctx.send(':no_entry_sign: Not enough permissions. You need Ban Members.')
        if not ctx.me.permissions_in(ctx.channel).ban_members:
            return await ctx.send(':no_entry_sign: Grant the bot Ban Members before doing this.')
        await ctx.guild.ban(user, reason=f'[{str(ctx.author)}] {reason}' if reason else f'Ban by {str(ctx.author)}', delete_message_days=7)


        

def setup(bot):
    bot.add_cog(Moderation(bot))