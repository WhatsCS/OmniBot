import asyncio
import aiohttp
from pprint import pprint


class CoinAPI:
    def __init__(self, api_token, loop):
        self.api_token = api_token
        self.loop = loop
        self.timeout = aiohttp.ClientTimeout(total=60)
        self.headers = {'X-CMC_PRO_API_KEY': self.api_token}
        self.session = None
        self.url = 'https://sandbox-api.coinmarketcap.com/v1'
        self.crypto_map = []

    async def _setup(self):
        self.session = aiohttp.ClientSession(loop=self.loop, headers=self.headers, timeout=self.timeout)
        params = {'listing_status': 'active'}
        async with self.session.get(url=f'{self.url}/cryptocurrency/map', params=params) as resp:
            tmp_map = await resp.json()
            for item in tmp_map['data']:
                tmp_dict = {}
                for key, value in item.items():
                    if key == "id" or key == "name" or key == "symbol":
                        tmp_dict[key] = value
                self.crypto_map.append(tmp_dict)
        await self.session.close()

    async def get_crypto(self, crypto, currency: list):
        query = None
        curr = ','.join(currency)
        result = []
        if self.session.closed:
            self.session = aiohttp.ClientSession(loop=self.loop, headers=self.headers)

        if type(crypto) is str:
            for item in self.crypto_map:
                if crypto == item.get('name') or crypto == item.get('symbol'):
                    query = item.get('id')
                    break
        elif type(crypto) is list:
            n_map = []
            for i in crypto:
                for item in self.crypto_map:
                    if i == item.get('name') or i == item.get('symbol'):
                        n_map.append(str(item.get('id')))
                        break
                    elif i == item.get('id'):
                        n_map.append(str(i))
                        break
            query = ','.join(n_map)
        else:
            return result

        if query is None:
            raise AttributeError

        async with self.session.get(url=f'{self.url}/cryptocurrency/quotes/latest', params={'id': f'{query}', 'convert': f'{curr}'}) as resp:
            data = await resp.json()
            try:
                for key, value in data['data'].items():
                    tmp = {'id': value.get('id'),
                            'name': value.get('name'),
                           'symbol': value.get('symbol'),
                           'currency': value.get('quote')}
                    #del tmp['currency']['market_cap']
                    #del tmp['currency']['volume_24h']
                    result.append(tmp)
            except KeyError:
                result = data['status']

        await self.session.close()
        return result[0] if len(result) == 1 else result

async def main(api_token, loop):
    cobj = CoinAPI(api_token, loop)
    await cobj._setup()
    return cobj

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    coin = loop.run_until_complete(main(api_token='e7266f94-3db8-4a0f-9a5b-90ae14c92dcf', loop=loop))
    coins = ['BTC']
    convert = ['USD']
    rs = loop.run_until_complete(coin.get_crypto(coins, convert))
    pprint(rs)
