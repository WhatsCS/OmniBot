import asyncio
import aiohttp

class CoinAPI():
    def __init__(self, api_token, loop):
        self.api_token = api_token
        self.loop = loop
        self.session = aiohttp.ClientSession(loop=loop)
        self.headers = {'X-CMC_PRO_API_KEY': self.api_token}

    async def get_crypto(self, crypto_id,):
        pass