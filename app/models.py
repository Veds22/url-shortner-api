from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime as dt

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Url(db.Model):
    __tablename__ = 'URL_db'
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    shortCode: Mapped[str] = mapped_column(String(12), unique=True, nullable=False)
    createdAt: Mapped[DateTime] = mapped_column(DateTime, default=dt.datetime.now())
    updatedAt: Mapped[DateTime] = mapped_column(DateTime, default=dt.datetime.now(), onupdate=dt.datetime.now())
    accessCount: Mapped[int] = mapped_column(Integer, default=0)
    
    def to_json(self):
        return {
            "id": self.id,
            "url": self.url,
            "short_code": self.shortCode,
            "created_at": self.createdAt,
            "updated_at": self.updatedAt,
        }
