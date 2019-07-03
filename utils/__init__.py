from .image import create_thumb
try:
    from .CoinMarketCapAsyncPy import CoinAPI
except ImportError:
    pass