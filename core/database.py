from core import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)

Base = declarative_base()