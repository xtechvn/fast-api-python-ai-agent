# Điểm khởi đầu ứng dụng
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import router
from app.api.routes import user
from app.config import get_settings

settings = get_settings()

# Tạo ứng dụng Fast API
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Api để quản lý thông tin dữ liệu cho dự án",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc"
)

# Thêm CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép all orgins trong mt ptrien
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# THêm các router
app.include_router(user.router, prefix=f"{settings.API_V1_STR}/user", tags=["user"])

# Root Endpoint
@app.get("/", include_in_schema=False)
async def root():
    """
    Root Endpoint trả về thông tin cơ bản về API

    """

    return {
        "mess": "Chào bạn đến với project " + settings.PROJECT_NAME,
        "docs": f"{settings.API_V1_STR}/docs"
    }

# Khởi động ứng dụng
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8002, reload=True)
