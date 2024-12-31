from sqlalchemy import create_engine
from models import Base
import os

def init_database():
    """Initialize database tables."""
    connection_string = os.getenv('DATABASE_URL')
    if not connection_string:
        connection_string = (
            f"postgresql://{os.getenv('PGUSER')}:{os.getenv('PGPASSWORD')}@"
            f"{os.getenv('PGHOST')}:{os.getenv('PGPORT')}/{os.getenv('PGDATABASE')}"
        )
    
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_database()
