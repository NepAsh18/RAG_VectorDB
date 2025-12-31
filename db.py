from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from app.utils import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True)
    filename = Column(String)
    chunks = Column(Integer)

# Create tables if not exist
Base.metadata.create_all(bind=engine)
