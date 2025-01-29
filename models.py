from sqlalchemy import Column, String, Enum, BigInteger, DateTime, ForeignKey, func
from database import Base
from database import relationship
import enum

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    alamat = Column(String, nullable=True)

class TransactionCategory(enum.Enum):
    PEMASUKAN = "PEMASUKAN"
    PENGELUARAN = "PENGELUARAN"


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(String(191), primary_key=True, index=True)
    amount = Column(BigInteger, nullable=False)
    description = Column(String(191), nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    userId = Column(String(191), ForeignKey("users.id"), nullable=False)
    category = Column(Enum(TransactionCategory), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship with user
    user = relationship("User", back_populates="transactions")