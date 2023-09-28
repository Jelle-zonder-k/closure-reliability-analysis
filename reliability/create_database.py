from data_model import Base
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database credentials from .env
HOST = os.getenv("LOCALHOST")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT")

# Create Database connection
DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/stormSurgeBarrierClosureData"
engine = create_engine(DATABASE_URL, echo=True)

# Import Base from data_models to create tables

# Create tables
Base.metadata.create_all(engine)
