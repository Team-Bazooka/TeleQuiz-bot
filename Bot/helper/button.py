from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def main_menu(lang):
    button = [ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(
        KeyboardButton("Start Quiz"),
    ).add(
        KeyboardButton("Ranking"),
        KeyboardButton("My Points"),
        KeyboardButton("Invite"),
        KeyboardButton("Help"),
        KeyboardButton("Language")
    ),
        ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(
            KeyboardButton("አካውንቴ"),
        ).add(
            KeyboardButton("ተግባራት"),
            KeyboardButton("ማውጣት"),
            KeyboardButton("ማጣቀሻዎች"),
            KeyboardButton("እገዛ"),
            KeyboardButton("ቋንቋ")
        )]
    return button[lang]


def select_language(lang):
    TEXT = ["Please select language", "እባክዎ ቋንቋ ይምረጡ"]
    mainBtn = InlineKeyboardMarkup().add(
        InlineKeyboardButton("English 🇺🇸", callback_data="lang_english"),
        InlineKeyboardButton("Amharic 🇪🇹", callback_data="lang_amharic"))
    return TEXT[lang], mainBtn


def category_btn(lang=0):
    button = [InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("History", callback_data="category_history"),
        InlineKeyboardButton("Science", callback_data="category_science"),
        InlineKeyboardButton("Math", callback_data="category_math"),
        InlineKeyboardButton("Biology", callback_data="category_biology"),
        InlineKeyboardButton("English", callback_data="category_english"),
        InlineKeyboardButton("General", callback_data="category_general")
    ),
        InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("History", callback_data="category_history"),
            InlineKeyboardButton("Science", callback_data="category_science"),
            InlineKeyboardButton("Math", callback_data="category_math"),
            InlineKeyboardButton("Biology", callback_data="category_biology"),
            InlineKeyboardButton("English", callback_data="category_english"),
            InlineKeyboardButton("General", callback_data="category_general")
        )]
    return button[lang]


def start_btn(lang=0):
    button = [InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("Start Now", callback_data="quiz_start"),
        InlineKeyboardButton("Cancel", callback_data="quiz_cancel")
    ),
        InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("Start Now", callback_data="category_history"),
            InlineKeyboardButton("Cancel", callback_data="category_science")
        )]
    return button[lang]
