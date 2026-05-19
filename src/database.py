from sqlalchemy import CheckConstraint, ForeignKey, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)

DATABASE_URL = "sqlite:///./expenses.db"
engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))

    expenses: Mapped[list[Expense]] = relationship("Expense", back_populates="user")


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    amount: Mapped[int] = mapped_column(
        CheckConstraint("amount > 0", name="positive_amount")
    )
    description: Mapped[str | None] = mapped_column(String(250))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship("User", back_populates="expenses")


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
