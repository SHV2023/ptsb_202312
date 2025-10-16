#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Улучшенная версия телеграм-бота с конфигурацией
"""

import logging
import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Попытка импорта конфигурации
try:
    from config import *
except ImportError:
    # Если config.py не найден, используем значения по умолчанию
    BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
    LOG_LEVEL = "INFO"
    ADMIN_IDS = []
    GREETING_RESPONSES = [
        "Привет! 👋",
        "Здравствуй! 😊", 
        "И тебе привет! 🎉",
        "Привет-привет! 👋",
    ]
    MESSAGES = {
        "start": """👋 Привет, {name}!

Добро пожаловать! Я простой телеграм-бот.

Доступные команды:
/start - начать работу с ботом
/help - показать справку
/test - проверить работу бота

Также я отвечаю на сообщения со словом 'Привет'! 😊""",
        
        "help": """🤖 Справка по боту

Доступные команды:
/start - приветствие и начало работы
/help - эта справка
/test - тестовая команда

Особенности:
• Отвечаю на сообщения со словом 'Привет'
• Веду лог всех взаимодействий
• Работаю 24/7 (при правильной настройке)

Если есть вопросы - просто напишите!""",
        
        "test": """✅ Тест пройден успешно!

👤 Пользователь: {name}
🆔 ID: {user_id}
📝 Username: @{username}

🤖 Бот работает корректно!""",
        
        "default": """Спасибо за сообщение, {name}! 📝

Я пока умею немного, но вот что могу:
• Отвечать на команды /start, /help, /test
• Здороваться, когда вы пишете 'Привет'

Попробуйте написать 'Привет' или используйте команды! 😊""",
        
        "error": "😔 Извините, произошла ошибка. Попробуйте еще раз или обратитесь к администратору."
    }

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, LOG_LEVEL, logging.INFO)
)
logger = logging.getLogger(__name__)


def is_admin(user_id: int) -> bool:
    """Проверка, является ли пользователь администратором"""
    return user_id in ADMIN_IDS


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user = update.effective_user
    message = MESSAGES["start"].format(name=user.first_name)
    
    await update.message.reply_text(message)
    logger.info(f"Пользователь {user.first_name} ({user.id}) запустил бота")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    await update.message.reply_text(MESSAGES["help"])


async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Тестовая команда для проверки работы бота"""
    user = update.effective_user
    message = MESSAGES["test"].format(
        name=user.first_name,
        user_id=user.id,
        username=user.username if user.username else 'не указан'
    )
    
    await update.message.reply_text(message)
    logger.info(f"Тестовая команда выполнена для пользователя {user.first_name} ({user.id})")


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда статистики (только для администраторов)"""
    user = update.effective_user
    
    if not is_admin(user.id):
        await update.message.reply_text("❌ У вас нет прав для выполнения этой команды.")
        return
    
    # Здесь можно добавить реальную статистику
    stats_message = """📊 Статистика бота

🤖 Статус: Работает
⏰ Время работы: Активен
👥 Администраторы: {admin_count}

Для получения подробной статистики добавьте базу данных.""".format(
        admin_count=len(ADMIN_IDS)
    )
    
    await update.message.reply_text(stats_message)


async def handle_hello_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик сообщений со словом 'Привет'"""
    user = update.effective_user
    response = random.choice(GREETING_RESPONSES)
    
    # Персонализируем ответ
    if "{name}" in response:
        response = response.format(name=user.first_name)
    else:
        response = f"{response} {user.first_name}!"
    
    await update.message.reply_text(response)
    logger.info(f"Ответил на приветствие от {user.first_name} ({user.id})")


async def handle_other_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик остальных сообщений"""
    user = update.effective_user
    message_text = update.message.text
    
    # Если сообщение не содержит 'привет', отвечаем общим сообщением
    if 'привет' not in message_text.lower():
        response = MESSAGES["default"].format(name=user.first_name)
        await update.message.reply_text(response)
        logger.info(f"Получено сообщение от {user.first_name} ({user.id}): {message_text}")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    logger.error(f"Произошла ошибка: {context.error}")
    
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(MESSAGES["error"])


def main() -> None:
    """Основная функция запуска бота"""
    # Проверяем наличие токена
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("❌ Ошибка: Необходимо установить токен бота!")
        print("Способы установки токена:")
        print("1. Создайте файл config.py на основе config_example.py")
        print("2. Установите переменную окружения: export BOT_TOKEN='ваш_токен'")
        print("3. Получите токен у @BotFather в Telegram")
        return
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("test", test_command))
    
    # Команда статистики (только для админов)
    if ADMIN_IDS:
        application.add_handler(CommandHandler("stats", stats_command))
    
    # Добавляем обработчики сообщений
    # Сначала обработчик приветствий (более специфичный)
    application.add_handler(MessageHandler(
        filters.TEXT & filters.Regex(r'(?i).*привет.*'), 
        handle_hello_messages
    ))
    
    # Затем обработчик остальных текстовых сообщений
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, 
        handle_other_messages
    ))
    
    # Добавляем обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    print("🚀 Запускаю улучшенного бота...")
    print(f"📊 Уровень логирования: {LOG_LEVEL}")
    print(f"👥 Администраторов: {len(ADMIN_IDS)}")
    print("Нажмите Ctrl+C для остановки")
    
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        print(f"❌ Критическая ошибка: {e}")


if __name__ == '__main__':
    main()