import aiohttp
import asyncio
import datetime
import sys
import json

async def fetch_currency_data(date):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.privatbank.ua/p24api/exchange_rates?date={date}') as response:
            if response.status == 200:
                return await response.json()
            else:
                return None

async def get_currency_rates(days):
    current_date = datetime.datetime.now()

    dates = [(current_date - datetime.timedelta(days=i)).strftime('%d.%m.%Y') for i in range(1, days + 1)]

    tasks = []
    for date in dates:
        tasks.append(fetch_currency_data(date))

    data = await asyncio.gather(*tasks)
    
    return data


def format_currency_data(data):
    formatted_data = []
    for item in data:
        formatted_item = {}
        for currency_data in item['exchangeRate']:
            if currency_data['currency'] in ['USD', 'EUR']:
                date = item['date']
                currency = currency_data['currency']
                sale_rate = currency_data.get('saleRate', currency_data['saleRateNB'])
                purchase_rate = currency_data.get('purchaseRate', currency_data['purchaseRateNB'])
                if date not in formatted_item:
                    formatted_item[date] = {}
                formatted_item[date][currency] = {
                    "sale": sale_rate,
                    "purchase": purchase_rate
                }
        formatted_data.append(formatted_item)
    return formatted_data



async def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <number_of_days>")
        return

    try:
        days = int(sys.argv[1])
        if days > 10:
            print("Error: Number of days cannot exceed 10")
            return

        data = await get_currency_rates(days)
        formatted_data = format_currency_data(data)
        
        with open('currency_rates.json', 'w') as outfile:
            json.dump(formatted_data, outfile, indent=4)

    except ValueError:
        print("Error: Number of days must be an integer")

if __name__ == "__main__":
    asyncio.run(main())
