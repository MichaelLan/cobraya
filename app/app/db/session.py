from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.app.core.config import settings

# connect_args={"check_same_thread": False} only for sqlite
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI,
                       connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
