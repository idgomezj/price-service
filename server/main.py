import asyncio
import logging
import time
import threading


from exchanges import (
        CoinbasePriceTracker, BinancePriceTracker, 
        DeribitPriceTracker, OKXPriceTracker 
    ) 


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RATE_LIMIT = 750  # Max connections in 10 minutes
RATE_LIMIT_TIME = 600  # 10 minutes in seconds



class PriceTracker:
    def __init__(self, exchanges):
        self.exchanges = exchanges

    def connect_to_all(self):
        threads = []
        for index, exchange in enumerate(self.exchanges):
            threads.append(exchange.run_in_thread(index))
        for thread in threads:
            thread.join()



def main():
    price_tracker = PriceTracker([
        CoinbasePriceTracker(),
        BinancePriceTracker(),
        DeribitPriceTracker(), 
        OKXPriceTracker(),
    ])

    # price_tracker = PriceTracker([
    #     CoinbasePriceTracker()
    # ])

    price_tracker.connect_to_all()

if __name__ == "__main__":
    asyncio.run(main())
