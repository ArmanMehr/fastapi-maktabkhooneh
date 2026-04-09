from sqlalchemy import CheckConstraint, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
)

DATABASE_URL = "sqlite:///./expenses.db"
engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    amount: Mapped[int] = mapped_column(
        CheckConstraint("amount > 0", name="positive_amount")
    )
    description: Mapped[str | None] = mapped_column(String(250))


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
