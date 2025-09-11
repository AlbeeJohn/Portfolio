import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def update_tagline():
    """Update the tagline to 'Data Analysis & Science Enthusiast'"""
    
    # Update the tagline in the portfolio document
    result = await db.portfolio.update_one(
        {},  # Match the first (and should be only) portfolio document
        {"$set": {"personal.tagline": "Data Analysis & Science Enthusiast"}}
    )
    
    if result.modified_count > 0:
        print("✅ Tagline updated successfully to: 'Data Analysis & Science Enthusiast'")
    else:
        print("❌ Failed to update tagline")

async def main():
    await update_tagline()
    client.close()

if __name__ == "__main__":
    asyncio.run(main())