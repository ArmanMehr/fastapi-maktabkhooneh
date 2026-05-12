from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configs import get_settings

engine = create_engine(get_settings().DATABASE_URL)

Session = sessionmaker(bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
