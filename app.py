import os
import aiohttp
import asyncio
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

app = Flask(__name__)
api_host = "https://ff-like-api-dun.vercel.app/"

headers = {}
if RAPIDAPI_KEY:
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': "free-fire-like1.p.rapidapi.com"
    }

# Flask home
@app.route("/")
def home():
    return f"Free Fire Like API is running at {datetime.now()}"

# Like endpoint
@app.route("/like", methods=["POST"])
def like_user():
    data = request.json
    uid = data.get("uid")
    if not uid or not uid.isdigit() or len(uid) < 6:
        return jsonify({"status": 0, "error": "Invalid UID"}), 400

    result = asyncio.run(send_like(uid))
    return jsonify(result)

# Core like function
async def send_like(uid):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{api_host}/like?uid={uid}", headers=headers) as response:
                if response.status == 404:
                    return {"status": 0, "error": "Player not found"}
                if response.status == 429:
                    return {"status": 0, "error": "API rate limit reached"}
                if response.status != 200:
                    return {"status": 0, "error": f"API error {response.status}"}
                data = await response.json()
                return data
        except Exception as e:
            return {"status": 0, "error": f"Unexpected error: {e}"}

# Run Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
