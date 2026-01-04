from sqlalchemy import create_engine, Table, Column, String, Integer, MetaData
from sqlalchemy.orm import sessionmaker
from app.utils import DATABASE_URL

engine = create_engine(DATABASE_URL)
metadata = MetaData()

documents = Table(
    "documents",
    metadata,
    Column("id", String, primary_key=True),
    Column("filename", String),
    Column("file_type", String),
    Column("author", String),
    Column("chunk_count", Integer),
)

metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
