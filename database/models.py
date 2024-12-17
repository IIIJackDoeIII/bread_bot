from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Инициализация базы
Base = declarative_base()

# Таблица пользователей
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    language = Column(String, default="Русский")
    name = Column(String, default="Unknown")
    phone = Column(String, nullable=True)

# Таблица корзины
class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bread_type = Column(String, nullable=False)
    quantity = Column(Integer, default=1)

# Таблица заказов
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    details = Column(Text, nullable=False)
    receipt = Column(String, nullable=True)
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.now)

# Создание базы данных
engine = create_engine("sqlite:///bread_bot.db")
Session = sessionmaker(bind=engine)

if __name__ == "__main__":
    print("Пересоздаём таблицы...")
    Base.metadata.create_all(engine)
    print("Таблицы созданы.")
