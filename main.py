# pip install python-telegram-bot sqlalchemy

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError
import os

# Настройка базы данных SQLite
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    username = Column(String)


# Создаем базу данных
engine = create_engine("sqlite:///users.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Настройка логгирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Конфигурация
TOKEN = os.getenv(
    "TELEGRAM_TOKEN", "7916282553:AAEPdjBuj6m4lXvSn6IQVyUqiplV7U6LKOw"
)  # Замените на свой токен


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = Session()
    user = update.effective_user
    new_user = User(
        user_id=user.id, username=f"@{user.username}" if user.username else None
    )

    try:
        session.add(new_user)
        session.commit()
        await update.message.reply_text("Добро пожаловать!")
        logging.info(f"Новый пользователь: {user.id}")
    except IntegrityError:
        session.rollback()
        await update.message.reply_text("С возвращением!")
    finally:
        session.close()


if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.run_polling()
