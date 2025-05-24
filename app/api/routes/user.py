# app/api/routes/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

# Import các module cần thiết
from app.sql_conn import get_db, get_pyodbc_connection,execute_store_not_param
# Import schema từ file schemas (Pydantic model)
from app.schemas.user_view_model import User as UserSchema

# Import model từ file models (SQLAlchemy model)
from app.models.user_model import User as UserModel

router = APIRouter()


# Sửa lại route detail để sử dụng UserSchema làm response_model
# @router.get("/detail/{email}", response_model=UserSchema)
# def get_user_by_id(email: str, db: Session = Depends(get_db)):


# Sửa lại route get_all_user để không sử dụng response_model với List[User]
# Thay vào đó, chúng ta sẽ sử dụng List[Dict[str, Any]]
@router.get("/")
async def get_all_user(db: Session = Depends(get_db)):
    """
    Lấy ds all các user bằng cách gọi store procedure
    return: ds user
    """

    try:

        user_list = execute_store_not_param("SP_GetAllUser")
       # print(user_list.count())
        return (
            {
                "error": 0,
                "data": user_list,
                "total":len(user_list)
            })


    except Exception as e:
        # Đóng kết nối nếu có lỗi
        if 'cursor' in locals():
            cursor.close()
        conn.close()
    raise e
