import os
from datetime import date
from dotenv import load_dotenv

load_dotenv()

API_TOKEN: str = os.getenv('API_TOKEN')
MONGODB_CONNECTION: str = os.getenv('MONGODB_CONNECTION')
LEGEND_POSITION_Y: float = -0.45
TODAY_DATE = date.today()