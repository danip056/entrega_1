from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

bd_uri = os.getenv("BD_URI", "postgresql+psycopg2://postgres:postgres@db/dsc")

engine = create_engine(bd_uri)
Session = sessionmaker(engine)