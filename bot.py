import os, requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
AI_KEY = os.getenv("AI_API_KEY")

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=AI_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bhai bot online hai! Kuch bhi likh, code ya image - sab bana dunga.")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    # Image generate
    if text.lower().startswith("image") or text.lower().startswith("/image"):
        prompt = text.replace("/image","").replace("image","")
        url = f"https://image.pollinations.ai/prompt/{prompt}"
        await update.message.reply_photo(photo=url, caption=f"Ban gaya: {prompt}")
        return

    # Text / Code unlimited
    response = client.chat.completions.create(
        model="meta-llama/llama-3.3-70b-instruct:free",
        messages=[{"role":"user","content":text}]
    )
    await update.message.reply_text(response.choices[0].message.content)

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
app.run_polling()
