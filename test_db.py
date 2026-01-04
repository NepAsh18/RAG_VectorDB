
from sqlalchemy import create_engine, text
from app.utils import DATABASE_URL

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Database connected successfully:", result.scalar())
except Exception as e:
    print("❌ Database connection failed")
    print(e)
