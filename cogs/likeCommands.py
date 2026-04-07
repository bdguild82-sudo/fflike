import aiohttp
import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

api_host = "https://ff-like-api-dun.vercel.app/"
headers = {}
if RAPIDAPI_KEY:
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': "free-fire-like1.p.rapidapi.com"
    }

async def send_like(uid):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{api_host}/like?uid={uid}", headers=headers) as response:
            if response.status == 404:
                return {"status": 0, "error": "Player not found"}
            if response.status == 429:
                return {"status": 0, "error": "API rate limit reached"}
            if response.status != 200:
                return {"status": 0, "error": f"API error {response.status}"}
            data = await response.json()
            return data

# Example usage
if __name__ == "__main__":
    uid = input("Enter UID to like: ")
    result = asyncio.run(send_like(uid))
    print(result)
