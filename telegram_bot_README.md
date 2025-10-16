# Телеграм-бот - Основа

Простой телеграм-бот с базовой функциональностью на Python.

## Функциональность

### Команды
- `/start` - приветствие и начало работы с ботом
- `/help` - показать справку по командам
- `/test` - тестовая команда для проверки работы бота

### Автоматические ответы
- Бот отвечает на любые сообщения, содержащие слово "Привет"
- На остальные сообщения дает общий информационный ответ

## Установка и настройка

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Получение токена бота

1. Найдите в Telegram бота @BotFather
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания нового бота
4. Скопируйте полученный токен

### 3. Настройка токена

Есть два способа установить токен:

#### Способ 1: Переменная окружения (рекомендуется)
```bash
export BOT_TOKEN="ваш_токен_здесь"
python telegram_bot.py
```

#### Способ 2: Прямо в коде
Откройте файл `telegram_bot.py` и замените:
```python
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
```
на:
```python
BOT_TOKEN = "ваш_токен_здесь"
```

## Запуск

```bash
python telegram_bot.py
```

Для остановки нажмите `Ctrl+C`.

## Структура проекта

```
.
├── telegram_bot.py      # Основной файл бота
├── requirements.txt     # Зависимости Python
└── telegram_bot_README.md  # Этот файл
```

## Возможности расширения

Бот легко расширяется. Вы можете добавить:

### Новые команды
```python
async def new_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Ответ на новую команду")

# Добавить в main():
application.add_handler(CommandHandler("newcommand", new_command))
```

### Новые обработчики сообщений
```python
async def handle_specific_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Ваша логика
    pass

# Добавить в main():
application.add_handler(MessageHandler(
    filters.TEXT & filters.Regex(r'(?i).*ключевое_слово.*'), 
    handle_specific_word
))
```

### Работа с базой данных
Можно добавить SQLite или другую БД для хранения данных пользователей.

### Клавиатуры и кнопки
```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = [[InlineKeyboardButton("Кнопка", callback_data='data')]]
reply_markup = InlineKeyboardMarkup(keyboard)
await update.message.reply_text("Сообщение", reply_markup=reply_markup)
```

## Логирование

Бот ведет логи всех взаимодействий. Логи выводятся в консоль и включают:
- Запуск команд пользователями
- Получение сообщений
- Ошибки

## Безопасность

⚠️ **Важно**: Никогда не публикуйте токен бота в открытом коде! Используйте переменные окружения или конфигурационные файлы, которые не попадают в систему контроля версий.

## Поддержка

Если у вас возникли вопросы или проблемы:
1. Проверьте правильность токена
2. Убедитесь, что установлены все зависимости
3. Проверьте логи на наличие ошибок

## Лицензия

Этот код предоставляется "как есть" для образовательных целей.