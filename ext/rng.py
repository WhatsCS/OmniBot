import io
from random import randrange, choice

import aiohttp
import discord
import rule34
from discord.ext import commands


class Randoms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.images = rule34.Rule34(self.bot.loop)
        self.img_l = []

    @commands.command(aliases=['rtd', 'd'])
    async def roll_the_dice(self, ctx, roll):
        count, dice = roll.split('d')
        result = []
        count, dice = (int(count), int(dice))
        if count > 20:
            await ctx.send("How many fucking die do you plan on rolling?")
            return

        for x in range(0, count):
            result.append(randrange(1, dice))

        result.sort()
        await ctx.send(f'<@{ctx.author.id}> rolled {result}')

    @commands.command()
    @commands.is_nsfw()
    @commands.cooldown(1, 5)
    async def r34(self, ctx, query, list=False):
        # I have code for requesting a list but no clue if going to properly implement
        self.img_l = await self.images.getImageURLS(query)
        if self.img_l is None:
            ctx.send(f'nothing found for {query}')
            return

        img_blob = b''
        if list is False:
            img_c = choice(self.img_l)
            async with aiohttp.ClientSession() as session:
                async with session.get(img_c) as resp:
                    img_blob = io.BytesIO(await resp.read())
            #file_blob = io.BytesIO(img_blob)
            fmsg = discord.File(fp=img_blob, filename='test_crop.jpg')
            async with ctx.typing():
                await ctx.send(file=fmsg)
        else:
            blob_list = []
            nlist = []
            for x in range(0, 9):
                nlist.append(choice(self.img_l))
            for url in nlist:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        blob_list.append(io.BytesIO(await resp.read()))

def setup(bot):
    bot.add_cog(Randoms(bot))