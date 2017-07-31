import discord
from discord.ext import commands
import importlib
import inspect
from utils.dataIO import dataIO
from utils import permissions
import time

class Core:
    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json('settings')
        self.post_task = self.bot.loop.create_task(self.post())

    def __unload(self):
        self.post_task.cancel()

    async def post(self):
        if 'extensions' not in self.settings:
            self.settings['extensions'] = []
        else:
            for extension in self.settings['extensions']:
                if extension not in list(self.bot.extensions):
                    try:
                        self.bot.load_extension(extension)
                    except:
                        self.settings['extensions'].remove(extension)
                        print("An extension failed to load.")


    @commands.command(aliases=['le'])
    @permissions.owner()
    async def load(self, ctx, name: str):
        """Loads an extension."""
        try:
            extension_name = 'extensions.{0}'.format(name)
            if extension_name not in list(self.bot.extensions):
                plugin = importlib.import_module(extension_name)
                importlib.reload(plugin)
                self.bot.load_extension(plugin.__name__)
                self.settings['extensions'].append(extension_name)
                await ctx.send('Extension loaded.')
            else:
                await ctx.send('Extension already loaded.')
        except Exception as e:
            await ctx.send(":x: An error occurred.\n\n```\n{}: {}```".format(type(e).__name__, e))

    @commands.command(aliases=['ule'])
    @permissions.owner()
    async def unload(self, ctx, name: str):
        """Unloads an extension."""
        extension_name = 'extensions.{0}'.format(name)
        if extension_name in list(self.bot.extensions):
            plugin = importlib.import_module(extension_name)
            importlib.reload(plugin)
            self.bot.unload_extension(plugin.__name__)
            self.settings['extensions'].remove(extension_name)
            await ctx.send('Extension unloaded.')
        else:
            await ctx.send('Extension not found or not loaded.')

    @commands.command(aliases=['rle', 'reloady'])
    @permissions.owner()
    async def reload(self, ctx, name: str):
        try:
            """Reloads an extension."""
            extension_name = 'extensions.{0}'.format(name)
            if extension_name in list(self.bot.extensions):
                plugin = importlib.import_module(extension_name)
                importlib.reload(plugin)
                self.bot.unload_extension(plugin.__name__)
                self.bot.load_extension(plugin.__name__)
                await ctx.send('Extension reloaded.')
            else:
                await ctx.send('Extension not loaded.')
        except Exception as e:
            await ctx.send(":x: An error occurred.\n\n```\n{}: {}```".format(type(e).__name__, e))

    @commands.command(aliases=['kys'])
    @permissions.owner()
    async def shutdown(self, ctx):
        """Shuts down the bot.... Duh."""
        await ctx.send("Logging out...")
        await self.bot.logout()

    @commands.command(aliases=["reboot"])
    @permissions.owner()
    async def restart(self, ctx):
        """Restarts the bot... Duh."""
        await ctx.send("Restarting...")
        quit()

    @commands.command(description="Pong.")
    async def ping(self, ctx):
        before = time.monotonic()
        pong = await ctx.send("...")
        after = time.monotonic()
        ping = (after - before) * 1000
        await pong.edit(content="Pong to you. {}ms".format(int(ping)))


def setup(bot):
    bot.add_cog(Core(bot))