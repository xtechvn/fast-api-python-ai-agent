#Pydantic models
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    """
    Pydantic model đại diện cho 1 user. Các trường dựa trên dữ liệu từ store sp_get_all_user
    """
    id: int
    username: str
    fullname: Optional[str] = None # fullname có thể null
    email: str


    class Config:
        #Cho phép từ ORM model (SQLALchemy) chuyển đổi sang Pydantic model
        from_attributes = True
        # Ví dụ dữ liệu mẫu cho document API
        schema_extra = {
            "user":{
                "username":"cuonglv",
                "fullname":"le van cuong",
                "phone":"0942066299"
            }
        }