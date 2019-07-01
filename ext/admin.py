from discord.ext import commands
class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello_world(self, ctx):
        await ctx.send("hello world")

    # @commands.command(name='role_react', aliases=['rr'])
    # async def _role_reaction(self, ctx, ):

def setup(bot):
    bot.add_cog(Administration(bot))
