import aiohttp
import asyncio
import discord
from discord.ext import commands
from CoinMarketCapAsyncPy import CoinAPI


class Crypto(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.coins = ['BTC', 'ETH', 'ZEN', 'KMD', 'LTC', 'ADA']
        self.api = None

    async def cog_before_invoke(self, ctx):
        self.api = await CoinAPI(api_token=self.bot.crypto_token, loop=self.bot.loop)

    async def _get_price_info(self, currency, coin):
        pass

    @commands.group(aliases=['c', 'co'], invoke_without_command=True)
    async def crypto(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(f'Please use a subcommand or do `{ctx.prefix}help crypto`')

    @crypto.command()
    @commands.cooldown(1, 10)
    async def list(self, ctx: commands.Context, currency: str='USD'):
        """List currently tracked crypto coins in USD. Can specify currency."""
        msg_c = []

        cinfo = await self.api.get_crypto(self.crypto)
        await ctx.send(f'```json\n{cinfo}\n```')
        #     msg_c.append(f'```json{cinfo}````')
        # msg = '\n'.join(msg_c)
        # await ctx.send(f'{msg}')

    @crypto.command(aliases=['add', 'aw'])
    async def add_watched(self, ctx: commands.Context, coin: str):
        """Add a new coin to be watched"""
        # TODO: Check the coin is real
        if len(self.coins) == 10:
            await ctx.send('Too many coins already tracked, either remove some coins or... \U0001F643')
            return
        self.coins.append(coin)
        await ctx.send(f'Success! {coin} has been added, do {ctx.prefix}list to see the new coin.')

    @crypto.command(aliases=['remove', 'r'])
    async def remove_watched(self, ctx: commands.Context, coin: str):
        if len(self.coins) == 0:
            await ctx.send('0 coins on the watch list?! Try adding some rather than removing...')
            return
        try:
            self.coins.remove(coin)
        except KeyError:
            await ctx.send(f'{coin} not found in the watch list!')

    @crypto.command(aliases=['s'])
    async def search(self, ctx: commands.Context, coin: str, currency: str='USD'):
        """
        Search for a specified coin in, if desired, specified currency. Defaults to USD.

        :param coin:
        :param currency:
        """
        cinfo = await self.api.get_crypto(coin)
        await ctx.send(f'```json\n{cinfo}\n```')
        embed = discord.Embed(title=cinfo['name'])


def setup(bot):
    bot.add_cog(Crypto(bot))
