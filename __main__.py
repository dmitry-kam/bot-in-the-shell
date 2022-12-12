import asyncio
import json
from binance import AsyncClient

api_key, api_secret = None, None
variables = {}

with open('init.config', 'r') as _file:
	lines = _file.readlines()
	for line in lines:
		line = (line.strip()).split(' ')
		variables[line[0]] = line[1]

api_key, api_secret = variables['api_key'], variables['secret_key']

async def main():

	client = await AsyncClient.create(api_key, api_secret, testnet = True)
	res = await client.get_all_orders(symbol = 'ETHUSDT')
	print(json.dumps(res, indent=3))

if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
