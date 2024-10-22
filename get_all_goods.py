import asyncio
import aiohttp
import json
import logging
import logging.config

from logger_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)

# Constants
EVOTOR_API_BASE_URL = "https://api.evotor.ru/"
VERSION = "1.0.0"


def get_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


async def get_all_goods(token: str, store_id: str) -> list[dict]:
    """Retrieve goods from Evotor API"""
    goods = []
    next_cursor = None
    url = f"{EVOTOR_API_BASE_URL}/stores/{store_id}/products"
    params = {}

    async with aiohttp.ClientSession() as session:
        while True:
            if next_cursor:
                params = {"next_cursor": next_cursor}
            async with session.get(
                url, headers=get_headers(token), params=params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    goods.extend(data.get("items", []))

                    next_cursor = data.get("paging", {}).get("next_cursor")
                    if not next_cursor:
                        break
                else:
                    logging.error(
                        f"Error getting goods: {response.status} - {await response.text()}"
                    )
                    raise aiohttp.ClientError(f"Error getting goods: {response.status}")
    return goods


def save_to_file(goods: list[dict], file_name: str) -> None:
    """Save goods to file"""
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(goods, f, ensure_ascii=False, indent=4)


async def main():
    """Main function to run the script"""
    try:
        print(f"\nGetAllGoods v{VERSION}\n")
        token = input("Input token, please: ")
        store_id = input("Input store_id, please: ")
        goods = await get_all_goods(token, store_id)
        print("Saved to goods.json")
        save_to_file(goods, "goods.json")
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
