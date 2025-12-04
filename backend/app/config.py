import os
import dotenv

class Config:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")