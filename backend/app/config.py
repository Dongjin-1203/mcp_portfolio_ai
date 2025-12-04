import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    NOTION_TOKEN = os.getenv("NOTION_TOKEN")
    NOTION_PORTFOLIO_PAGE_ID = os.getenv("NOTION_PORTFOLIO_PAGE_ID")