from sqlalchemy import create_engine, text

DATABASE_URL = (
    "postgresql://postgres:postgres@localhost:5432/procurement_db"
)

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(text("SELECT version();"))
    print(result.fetchone())

print("Database Connected Successfully!")