import asyncio

import logging
import time

from exchanges import (
        CoinbasePriceTracker, BinancePriceTracker, 
        DeribitPriceTracker, OKXPriceTracker 
    ) 


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RATE_LIMIT = 750  # Max connections in 10 minutes
RATE_LIMIT_TIME = 600  # 10 minutes in seconds

class Throttler:
    def __init__(self, rate_limit, time_limit):
        self.rate_limit = rate_limit
        self.time_limit = time_limit
        self.requests = []
    
    async def throttle(self):
        current_time = time.time()
        self.requests = [t for t in self.requests if t > current_time - self.time_limit]

        if len(self.requests) >= self.rate_limit:
            wait_time = self.time_limit - (current_time - self.requests[0])
            logger.info(f"Rate limit reached. Waiting for {wait_time:.2f} seconds before next request.")
            await asyncio.sleep(wait_time)

        self.requests.append(time.time())

class PriceTracker:
    def __init__(self, exchanges, throttler):
        self.exchanges = exchanges
        self.throttler = throttler

    async def connect_to_all(self):
        tasks = [self.throttled_connect(exchange) for exchange in self.exchanges]
        await asyncio.gather(*tasks)

    async def throttled_connect(self, exchange):
        await self.throttler.throttle()
        await exchange.connect()



async def main():
    symbols = ["BTC", "ETH", "LTC"]
    throttler = Throttler(RATE_LIMIT, RATE_LIMIT_TIME)

    coinbase_tracker = CoinbasePriceTracker(symbols)
    binance_tracker = BinancePriceTracker(symbols)
    deribit_tracker = DeribitPriceTracker(symbols)
    okx_tracker = OKXPriceTracker(symbols)

    price_tracker = PriceTracker([coinbase_tracker, binance_tracker, deribit_tracker, okx_tracker], throttler)
    await price_tracker.connect_to_all()

if __name__ == "__main__":
    asyncio.run(main())
