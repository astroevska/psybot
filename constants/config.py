import os
from dotenv import load_dotenv


load_dotenv()

API_TOKEN: str = os.getenv('API_TOKEN')
MONGODB_CONNECTION: str = os.getenv('MONGODB_CONNECTION')
LEGEND_POSITION_Y: float = -0.45
UNFINISHED_SAVE_DELAY = 12000
