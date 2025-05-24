from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pyodbc
from app.config import get_settings
from fastapi import HTTPException, status

# Lấy cấu hình
settings = get_settings()
try:
    # Sử dụng ODBC Driver 18: sudo nano /opt/homebrew/etc/odbcinst.ini
    connection_string = (
        f"mssql+pyodbc://{settings.SQL_USER}:{settings.SQL_PASSWORD}@"
        f"{settings.SQL_SERVER}/{settings.SQL_DATABASE}?"
        f"driver=ODBC+Driver+18+for+SQL+Server"
    )
    engine = create_engine(connection_string)
    # print("SQLAlchemy đã được khởi tạo thành công")
except Exception as e:
    print(f"Lỗi khi khởi tạo SQLAlchemy engine: {str(e)}")
    raise

# Tạo session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class cho các model
# Base là lớp cơ sở cho tất cả các model SQLAlchemy trong ứng dụng của bạn. Nó sử dụng "Declarative" pattern của SQLAlchemy.
Base = declarative_base()


def get_pyodbc_connection():
    """
    Tạo kết nối pyodbc trực tiếp đến SQL Server.
    """

    # Thử kết nối với Driver 18 trước
    try:
        conn_str = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={settings.SQL_SERVER};"
            f"DATABASE={settings.SQL_DATABASE};"
            f"UID={settings.SQL_USER};"
            f"PWD={settings.SQL_PASSWORD};"
            "TrustServerCertificate=yes;"
        )

        conn = pyodbc.connect(conn_str)
        print("Kết nối thành công với ODBC Driver 18")
        return conn
    except Exception as e:
        print(f"Lỗi khi kết nối với Driver 18: {str(e)}. Kiểm tra laị đường truyền")


# Dependency để inject database session vào endpoint
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Gọi dữ liệu từ store trong SQL. Output return ra 1 array
def execute_store_not_param(store_name: str):
    array_list = []
    try:
        # Lấy kết nối trực tiếp SQL
        conn = get_pyodbc_connection()
        if not conn:
            print("Không thể kết nối đến SQL Server")

        # Thực hiện truy vấn dữ liệu
        cursor = conn.cursor()

        # Thực thi stored procedure
        cursor.execute("{CALL [dbo].[" + store_name + "]}")

        # Lấy kết quả
        rows = cursor.fetchall()

        # Lấy tên các cột từ mô tả cursor
        columns = [column[0] for column in cursor.description]

        # Chuyển đổi kết quả thành danh sách từ điển
        data_list = []
        for row in rows:
            # Tạo từ điển với key là tên cột và value là giá trị tương ứng
            obj_data_table = {}
            for i, column in enumerate(columns):
                obj_data_table[column] = row[i]
            data_list.append(obj_data_table)

        # Đóng cursor và kết nối
        cursor.close()
        conn.close()

        return data_list

    except Exception as e:
        print(f"error with func execute_store_not_param: {str(e)}")
