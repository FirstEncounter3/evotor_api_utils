import asyncio
import aiohttp
import json
import logging

from logger_config import LOGGING_CONFIG

# Constants
EVOTOR_API_BASE_URL = "https://api.evotor.ru/"
VERSION = "1.0.0"


# Type hints
StoresData = list[dict]
DevicesData = list[dict]


def get_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


async def get_stores(token: str) -> StoresData:
    """Retrieve stores from Evotor API"""
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{EVOTOR_API_BASE_URL}/stores", headers=get_headers(token)
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                logging.error(
                    f"Error getting stores: {response.status} - {await response.text()}"
                )
                raise aiohttp.ClientError(f"Error getting stores: {response.status}")


async def get_devices(token: str) -> DevicesData:
    """Retrieve devices from Evotor API"""
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{EVOTOR_API_BASE_URL}/devices", headers=get_headers(token)
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                logging.error(
                    f"Error getting devices: {response.status} - {await response.text()}"
                )
                raise aiohttp.ClientError(f"Error getting devices: {response.status}")


def format_stores_and_devices(stores: StoresData, devices: DevicesData) -> list[dict]:
    """Format stores and devices data"""
    formatted_data = []
    for store in stores["items"]:
        store_dict = {"id": store["id"], "name": store["name"], "devices": []}
        for device in devices["items"]:
            if device["store_id"] == store["id"]:
                store_dict["devices"].append(
                    {"id": device["id"], "name": device["name"]}
                )
        formatted_data.append(store_dict)
    return formatted_data


async def main():
    """Main function to run the script"""
    try:
        print(f"\nGetStoresAndDevices v{VERSION}\n")
        token = input("Input token, please: ")
        stores = await get_stores(token)
        devices = await get_devices(token)
        result = format_stores_and_devices(stores, devices)
        print("\nResult:\n")
        print(json.dumps(result, indent=4, ensure_ascii=False))
        input("\nPress Enter to exit...")
    except aiohttp.ClientError as e:
        logging.error(f"Error: {e}")
        retry = input("An error occurred. Retry? (y/n): ")
        if retry.lower() == "y":
            await main()
        else:
            logging.info("Exiting...")
            exit(1)
    except KeyboardInterrupt:
        logging.info("Exiting...")
        exit(0)


if __name__ == "__main__":
    asyncio.run(main())
