import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    
    # 1. Lấy chuỗi kết nối từ biến môi trường DATABASE_URL (nếu chạy trên Render)
    # 2. Nếu không có biến môi trường, mặc định dùng URI PostgreSQL của Supabase
    db_url = os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres:[Nguyentienhuy10]@db.xfwmvvykzgjkrujjkjdq.supabase.co:5432/postgres'
    )

    # Đảm bảo tiền tố là postgresql:// (tương thích với SQLAlchemy)
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False