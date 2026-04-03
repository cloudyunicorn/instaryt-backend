import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

    IG_ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN")
    IG_USER_ID = os.getenv("IG_USER_ID")
    PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
    PAGE_ID = os.getenv("PageID")

settings = Settings()