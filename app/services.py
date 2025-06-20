import os
import httpx
from dotenv import load_dotenv

load_dotenv()
THECATAPI_API_KEY = os.getenv("THECATAPI_API_KEY")
THECATAPI_URL = "https://api.thecatapi.com/v1/breeds/search"

async def validate_cat_breed(breed_name: str) -> bool:
    """
    Validates if a cat breed exists using TheCatAPI.
    """
    if not THECATAPI_API_KEY:
        return True
        
    headers = {"x-api-key": THECATAPI_API_KEY}
    params = {"q": breed_name}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(THECATAPI_URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            return len(data) > 0 and data[0]['name'].lower() == breed_name.lower()
        except httpx.RequestError:
            return False
