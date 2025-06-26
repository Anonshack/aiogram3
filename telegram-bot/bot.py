from aiogram import Bot, Dispatcher, types
from aiohttp import web
import os

API_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_cmd(msg: types.Message):
    await msg.answer("✅ Bot Renderda ishlayapti!")

async def on_startup(app):
    webhook_url = f"{os.getenv('RENDER_EXTERNAL_URL')}/webhook"
    await bot.set_webhook(webhook_url)

async def on_shutdown(app):
    await bot.delete_webhook()

async def handle_webhook(request):
    data = await request.json()
    update = types.Update(**data)
    await dp.process_update(update)
    return web.Response()

app = web.Application()
app.router.add_post('/webhook', handle_webhook)

app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
8126529160:AAGNxgB0sFJLB5T6mVGEp8fYALlTRB7US1U