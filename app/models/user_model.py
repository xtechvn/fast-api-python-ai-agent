# app/models/user_model.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.sql_conn import Base


class User(Base):
    __tablename__ = "User"  # Tên bảng trong database

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, index=True)
    fullname = Column(String)
    # Thêm các trường khác nếu cần

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())