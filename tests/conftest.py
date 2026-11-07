import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test-ideabox.db")
os.environ.setdefault("JWT_SECRET", "test-only-secret")
