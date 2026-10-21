import os
import sys
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Read the token from Railway Variables
TOKEN = os.environ.get("TOKEN")

if not TOKEN or TOKEN == "YOUR_BOT_TOKEN_HERE":
    print("ERROR: TOKEN is missing! Please add it in Railway Variables.")
    sys.exit(1)

# --- CONTENT DATA ---
NEWS = {
    "news_1": "🔥 *Latest Drop*\n\nThe new Air Max series just released this week. They feature upgraded cushioning and a breathable mesh upper. Perfect for daily wear.",
    "news_2": "🔥 *Trend Alert*\n\nRetro running sneakers are making a huge comeback this season. Look for classic silhouettes in bold colors like green and orange.",
    "news_3": "🔥 *Restock Info*\n\nPopular white low-top sneakers are back in stock at major retailers. Sizes are limited, so check your local stores soon."
}

STYLES = {
    "running": "👟 *Running Sneakers*\n\nBuilt for performance. Features thick foam soles and breathable fabric.\nBest for: Jogging, gym, marathons.",
    "basketball": "👟 *Basketball Shoes*\n\nHigh-tops with ankle support and strong grip.\nBest for: Court sports, ankle protection.",
    "casual": "👟 *Casual Sneakers*\n\nClassic low-tops like Converse or Vans. Simple and versatile.\nBest for: Everyday wear, street style.",
    "skate": "👟 *Skate Shoes*\n\nFlat soles with reinforced toes for durability.\nBest for: Skateboarding, casual wear."
}

SIZING = {
    "size_guide": "📏 *Sizing Guide*\n\n• Running shoes: Go half a size up for toe room.\n• Basketball shoes: True to size, they fit snug.\n• Casual canvas: True to size, but can be tight at first.",
    "width": "📏 *Width Guide*\n\nIf you have wide feet, look for 'Wide' or '2E' tags. Brands like New Balance offer great wide options."
}

CARE_TIPS = (
    "🧼 *Sneaker Care Tips*\n\n"
    "• Clean mesh with a soft brush and mild soap.\n"
    "• Do not put sneakers in the washing machine (it ruins the glue).\n"
    "• Air dry them in the shade, never in direct sunlight.\n"
    "• Use shoe trees to keep the shape."
)

WELCOME_TEXT = (
    "Welcome to Sneaker Updates! 👋\n\n"
    "I provide the latest sneaker news, style guides, sizing help, and care tips.\n\n"
    "Choose an option below:"
)

# --- KEYBOARDS ---
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔥 Latest Sneaker News", callback_data="menu_news")],
        [InlineKeyboardButton("👟 Sneaker Styles", callback_data="menu_styles")],
        [InlineKeyboardButton("📏 Sizing Help", callback_data="menu_sizing")],
        [InlineKeyboardButton("🧼 Care & Cleaning", callback_data="menu_care")],
    ])

def news_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Latest Drop", callback_data="news_1")],
        [InlineKeyboardButton("Trend Alert", callback_data="news_2")],
        [InlineKeyboardButton("Restock Info", callback_data="news_3")],
        [InlineKeyboardButton("⬅️ Back", callback_data="back_main")],
    ])

def styles_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Running", callback_data="style_running")],
        [InlineKeyboardButton("Basketball", callback_data="style_basketball")],
        [InlineKeyboardButton("Casual", callback_data="style_casual")],
        [InlineKeyboardButton("Skate", callback_data="style_skate")],
        [InlineKeyboardButton("⬅️ Back", callback_data="back_main")],
    ])

def sizing_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Size Guide", callback_data="size_size_guide")],
        [InlineKeyboardButton("Width Guide", callback_data="size_width")],
        [InlineKeyboardButton("⬅️ Back", callback_data="back_main")],
    ])

def back_menu():
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back to menu", callback_data="back_main")]])

# --- HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_TEXT, reply_markup=main_menu())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu_news":
        await query.edit_message_text("Select a news topic:", reply_markup=news_menu())
    elif data == "menu_styles":
        await query.edit_message_text("Choose a sneaker style:", reply_markup=styles_menu())
    elif data == "menu_sizing":
        await query.edit_message_text("Choose a sizing guide:", reply_markup=sizing_menu())
    elif data == "menu_care":
        await query.edit_message_text(CARE_TIPS, parse_mode="Markdown", reply_markup=back_menu())
    
    elif data.startswith("news_"):
        await query.edit_message_text(NEWS[data], parse_mode="Markdown", reply_markup=back_menu())
    elif data.startswith("style_"):
        await query.edit_message_text(STYLES[data.replace("style_", "")], parse_mode="Markdown", reply_markup=back_menu())
    elif data.startswith("size_"):
        await query.edit_message_text(SIZING[data.replace("size_", "")], parse_mode="Markdown", reply_markup=back_menu())
    
    elif data == "back_main":
        await query.edit_message_text(WELCOME_TEXT, reply_markup=main_menu())

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Sneaker Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
