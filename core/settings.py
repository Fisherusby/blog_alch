import os


SECRET_KEY: str = os.getenv("SECRET_KEY", b'_5#y2L"F4Q8z\n\xec]/')

SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///../db.sqlite3"
    )

SQLALCHEMY_TRACK_MODIFICATIONS: bool = bool(
        os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", 1)
    )
