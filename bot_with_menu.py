#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram-бот с меню и интеграцией с API для фото и фактов о животных
"""

import logging
import os
import random
import aiohttp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота (получите его у @BotFather в Telegram)
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# API endpoints
CAT_PHOTO_API = "https://api.thecatapi.com/v1/images/search"
CAT_FACT_API = "https://catfact.ninja/fact"
FOX_PHOTO_API = "https://randomfox.ca/floof/"
DOG_FACT_API = "https://dogapi.dog/api/v2/facts"


def get_main_menu_keyboard():
    """Создает клавиатуру главного меню"""
    keyboard = [
        [
            InlineKeyboardButton("🐱 Фото кота", callback_data='cat_photo'),
            InlineKeyboardButton("🐱 Факт о кошках", callback_data='cat_fact')
        ],
        [
            InlineKeyboardButton("🐶 Факт о собаках", callback_data='dog_fact'),
            InlineKeyboardButton("🦊 Фото лисы", callback_data='fox_photo')
        ],
        [
            InlineKeyboardButton("🔄 Обновить меню", callback_data='menu')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user = update.effective_user
    welcome_message = (
        f"👋 Привет, {user.first_name}!\n\n"
        "Добро пожаловать! Я бот с интересными функциями! 🤖\n\n"
        "Выбери действие в меню ниже, и я покажу тебе фото животных или интересные факты! 🐾\n\n"
        "Доступные команды:\n"
        "/start - начать работу с ботом\n"
        "/menu - показать главное меню\n"
        "/help - показать справку\n"
        "/test - проверить работу бота\n\n"
        "Также я отвечаю на сообщения со словом 'Привет'! 😊"
    )
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=get_main_menu_keyboard()
    )
    logger.info(f"Пользователь {user.first_name} ({user.id}) запустил бота")


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /menu"""
    menu_text = (
        "🎯 Главное меню\n\n"
        "Выберите действие:"
    )
    
    await update.message.reply_text(
        menu_text,
        reply_markup=get_main_menu_keyboard()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    help_text = (
        "🤖 Справка по боту\n\n"
        "Доступные команды:\n"
        "/start - приветствие и главное меню\n"
        "/menu - показать главное меню\n"
        "/help - эта справка\n"
        "/test - тестовая команда\n\n"
        "🎯 Возможности бота:\n"
        "• 🐱 Случайные фото котов\n"
        "• 🐱 Интересные факты о кошках\n"
        "• 🐶 Факты о собаках\n"
        "• 🦊 Фото лисиц\n\n"
        "Особенности:\n"
        "• Отвечаю на сообщения со словом 'Привет'\n"
        "• Использую реальные API для получения данных\n"
        "• Работаю с кнопками для удобной навигации\n\n"
        "Просто нажимайте на кнопки и наслаждайтесь! 🎉"
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
        "🤖 Бот работает корректно!\n\n"
        "Нажмите на кнопку ниже, чтобы вернуться в меню:"
    )
    
    keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(test_message, reply_markup=reply_markup)
    logger.info(f"Тестовая команда выполнена для пользователя {user.first_name} ({user.id})")


async def fetch_cat_photo() -> str:
    """Получить случайное фото кота"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(CAT_PHOTO_API) as response:
                if response.status == 200:
                    data = await response.json()
                    return data[0]['url']
    except Exception as e:
        logger.error(f"Ошибка при получении фото кота: {e}")
    return None


async def fetch_cat_fact() -> str:
    """Получить случайный факт о кошках"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(CAT_FACT_API) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['fact']
    except Exception as e:
        logger.error(f"Ошибка при получении факта о кошках: {e}")
    return None


async def fetch_fox_photo() -> str:
    """Получить случайное фото лисы"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(FOX_PHOTO_API) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['image']
    except Exception as e:
        logger.error(f"Ошибка при получении фото лисы: {e}")
    return None


async def fetch_dog_fact() -> str:
    """Получить случайный факт о собаках"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(DOG_FACT_API) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['data'][0]['attributes']['body']
    except Exception as e:
        logger.error(f"Ошибка при получении факта о собаках: {e}")
    return None


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    logger.info(f"Пользователь {user.first_name} ({user.id}) нажал кнопку: {query.data}")
    
    if query.data == 'menu':
        menu_text = (
            "🎯 Главное меню\n\n"
            "Выберите действие:"
        )
        await query.edit_message_text(
            menu_text,
            reply_markup=get_main_menu_keyboard()
        )
    
    elif query.data == 'cat_photo':
        await query.edit_message_text("🔄 Загружаю фото кота...")
        photo_url = await fetch_cat_photo()
        
        if photo_url:
            keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data='menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_photo(
                photo=photo_url,
                caption="🐱 Вот милый котик для тебя!",
                reply_markup=reply_markup
            )
            await query.message.delete()
        else:
            await query.edit_message_text(
                "😔 Не удалось загрузить фото. Попробуйте еще раз!",
                reply_markup=get_main_menu_keyboard()
            )
    
    elif query.data == 'cat_fact':
        await query.edit_message_text("🔄 Загружаю факт о кошках...")
        fact = await fetch_cat_fact()
        
        if fact:
            keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data='menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                f"🐱 Интересный факт о кошках:\n\n{fact}",
                reply_markup=reply_markup
            )
        else:
            await query.edit_message_text(
                "😔 Не удалось загрузить факт. Попробуйте еще раз!",
                reply_markup=get_main_menu_keyboard()
            )
    
    elif query.data == 'fox_photo':
        await query.edit_message_text("🔄 Загружаю фото лисы...")
        photo_url = await fetch_fox_photo()
        
        if photo_url:
            keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data='menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_photo(
                photo=photo_url,
                caption="🦊 Вот красивая лисичка для тебя!",
                reply_markup=reply_markup
            )
            await query.message.delete()
        else:
            await query.edit_message_text(
                "😔 Не удалось загрузить фото. Попробуйте еще раз!",
                reply_markup=get_main_menu_keyboard()
            )
    
    elif query.data == 'dog_fact':
        await query.edit_message_text("🔄 Загружаю факт о собаках...")
        fact = await fetch_dog_fact()
        
        if fact:
            keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data='menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                f"🐶 Интересный факт о собаках:\n\n{fact}",
                reply_markup=reply_markup
            )
        else:
            await query.edit_message_text(
                "😔 Не удалось загрузить факт. Попробуйте еще раз!",
                reply_markup=get_main_menu_keyboard()
            )


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
        
        response = random.choice(responses)
        keyboard = [[InlineKeyboardButton("🎯 Открыть меню", callback_data='menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(response, reply_markup=reply_markup)
        logger.info(f"Ответил на приветствие от {user.first_name} ({user.id})")


async def handle_other_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик остальных сообщений"""
    user = update.effective_user
    message_text = update.message.text
    
    if 'привет' not in message_text.lower():
        response = (
            f"Спасибо за сообщение, {user.first_name}! 📝\n\n"
            "Я умею многое! Вот что я могу:\n"
            "• Показывать фото котов и лисиц 🐱🦊\n"
            "• Рассказывать факты о кошках и собаках 🐶\n"
            "• Отвечать на команды /start, /menu, /help, /test\n"
            "• Здороваться, когда вы пишете 'Привет'\n\n"
            "Используйте кнопки ниже для навигации! 😊"
        )
        
        await update.message.reply_text(
            response,
            reply_markup=get_main_menu_keyboard()
        )
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
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("test", test_command))
    
    # Добавляем обработчик callback-запросов от кнопок
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Добавляем обработчики сообщений
    application.add_handler(MessageHandler(
        filters.TEXT & filters.Regex(r'(?i).*привет.*'), 
        handle_hello_messages
    ))
    
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, 
        handle_other_messages
    ))
    
    # Добавляем обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    print("🚀 Запускаю бота с меню и API...")
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
