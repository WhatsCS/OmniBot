from random import randrange

from discord.ext import commands
import rule34


class Randoms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.images = rule34.Rule34(self.bot.loop)

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
    async def r34(self, ctx, query, list=None):
        await ctx.send(f'{query}; {list}')
        img_l = await self.images.getImageURLS(query)

def setup(bot):
    bot.add_cog(Randoms(bot))