#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Основа телеграм-бота с базовой функциональностью
"""

import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота (получите его у @BotFather в Telegram)
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user = update.effective_user
    welcome_message = (
        f"👋 Привет, {user.first_name}!\n\n"
        "Добро пожаловать! Я простой телеграм-бот.\n\n"
        "Доступные команды:\n"
        "/start - начать работу с ботом\n"
        "/help - показать справку\n"
        "/test - проверить работу бота\n\n"
        "Также я отвечаю на сообщения со словом 'Привет'! 😊"
    )
    
    await update.message.reply_text(welcome_message)
    logger.info(f"Пользователь {user.first_name} ({user.id}) запустил бота")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    help_text = (
        "🤖 Справка по боту\n\n"
        "Доступные команды:\n"
        "/start - приветствие и начало работы\n"
        "/help - эта справка\n"
        "/test - тестовая команда\n\n"
        "Особенности:\n"
        "• Отвечаю на сообщения со словом 'Привет'\n"
        "• Веду лог всех взаимодействий\n"
        "• Работаю 24/7 (при правильной настройке)\n\n"
        "Если есть вопросы - просто напишите!"
    )
    
    await update.message.reply_text(help_text)


async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Тестовая команда для проверки работы бота"""
    user = update.effective_user
    test_message = (
        f"✅ Тест пройден успешно!\n\n"
        f"👤 Пользователь: {user.first_name}\n"
        f"🆔 ID: {user.id}\n"
        f"📝 Username: @{user.username if user.username else 'не указан'}\n\n"
        "🤖 Бот работает корректно!"
    )
    
    await update.message.reply_text(test_message)
    logger.info(f"Тестовая команда выполнена для пользователя {user.first_name} ({user.id})")


async def handle_hello_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик сообщений со словом 'Привет'"""
    user = update.effective_user
    message_text = update.message.text.lower()
    
    if 'привет' in message_text:
        responses = [
            f"Привет, {user.first_name}! 👋",
            f"И тебе привет, {user.first_name}! 😊",
            f"Здравствуй, {user.first_name}! Как дела?",
            f"Привет-привет, {user.first_name}! 🎉",
        ]
        
        # Выбираем случайный ответ
        import random
        response = random.choice(responses)
        
        await update.message.reply_text(response)
        logger.info(f"Ответил на приветствие от {user.first_name} ({user.id})")


async def handle_other_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик остальных сообщений"""
    user = update.effective_user
    message_text = update.message.text
    
    # Если сообщение не содержит 'привет', отвечаем общим сообщением
    if 'привет' not in message_text.lower():
        response = (
            f"Спасибо за сообщение, {user.first_name}! 📝\n\n"
            "Я пока умею немного, но вот что могу:\n"
            "• Отвечать на команды /start, /help, /test\n"
            "• Здороваться, когда вы пишете 'Привет'\n\n"
            "Попробуйте написать 'Привет' или используйте команды! 😊"
        )
        
        await update.message.reply_text(response)
        logger.info(f"Получено сообщение от {user.first_name} ({user.id}): {message_text}")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    logger.error(f"Произошла ошибка: {context.error}")
    
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "😔 Извините, произошла ошибка. Попробуйте еще раз или обратитесь к администратору."
        )


def main() -> None:
    """Основная функция запуска бота"""
    # Проверяем наличие токена
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("❌ Ошибка: Необходимо установить токен бота!")
        print("Получите токен у @BotFather и установите переменную окружения BOT_TOKEN")
        print("Или замените YOUR_BOT_TOKEN_HERE в коде на ваш токен")
        return
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("test", test_command))
    
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
    print("🚀 Запускаю бота...")
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