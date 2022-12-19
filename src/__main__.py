import asyncio
import json
import os
from binance import AsyncClient

api_key, api_secret = os.environ['api_key'], os.environ['secret_key']
async def main():

	client = await AsyncClient.create(api_key, api_secret, testnet = True)
	res = await client.get_all_orders(symbol = 'ETHUSDT')
	print(json.dumps(res, indent=3))

if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
