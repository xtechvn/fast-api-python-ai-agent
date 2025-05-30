from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

# Đường dẫn tuyệt đối đến thư mục gốc dự án
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# File .env nên được đặt trong thư mục gốc dự án
# ENV_FILE = os.path.join(BASE_DIR + "/FastApiProject", ".env")
# if os.path.exists(ENV_FILE):
#     # Load biến môi trường từ file .env
#     load_dotenv(ENV_FILE)
# else:
#     print(".env not found")

load_dotenv()

class Settings(BaseSettings):
    # Cấu hình API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Fast API"

    # Cấu hình SQL Server - KHÔNG sử dụng os.getenv nữa
    # Sử dụng giá trị mặc định trực tiếp
    SQL_SERVER: str = os.getenv("SQL_SERVER")
    SQL_DATABASE: str = os.getenv("SQL_DATABASE")
    SQL_USER: str = os.getenv("SQL_USER")
    SQL_PASSWORD: str = os.getenv("SQL_PASSWORD")  # Hãy thay thế bằng mật khẩu thực tế

    # Chuỗi kết nối SQLAlchemy
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"mssql+pyodbc://{self.SQL_USER}:{self.SQL_PASSWORD}@{self.SQL_SERVER}/{self.SQL_DATABASE}?driver=ODBC+Driver+17+for+SQL+Server"

    # Cấu hình đọc từ file .env - sử dụng model_config thay vì class Config
    # model_config = {
    #     "env_file": ENV_FILE,
    #     "env_file_encoding": "utf-8",
    #     "case_sensitive": True,
    #     "extra": "ignore",
    # }


@lru_cache()
def get_settings():
    """
    Tạo và cache đối tượng Settings để tối ưu hiệu suất.
    """
    settings = Settings()

    return settings
