import asyncio
from os import getcwd, environ as env
from os.path import dirname, relpath, join

from pyrogram import Client as PyroClient, filters
from pyrogram.handlers import MessageHandler

from .controllers import ai, get_chars, get_models, set_char, set_model, info, gradio, settings
from .services.i18n import get_i18n

allowed_chat = int(env["TELEGRAM_CHAT_ID"])
bot_owner = int(env["TELEGRAM_BOT_OWNER_ID"])

class Client(PyroClient):
  lang = "en"
  t = get_i18n(lang)
  cwd = dirname(relpath(__file__, getcwd()))

  def __init__(self):
    super().__init__(
      join(self.cwd, 'textgen'),
      api_id    = int(env["TELEGRAM_API_ID"]),
      api_hash  = str(env["TELEGRAM_API_HASH"]),
      bot_token = str(env["TELEGRAM_BOT_TOKEN"]),
    )

  async def run(self):
    try:
      await self.start()
      self.set_routes()

      while True:
        await asyncio.sleep(1)

    except Exception as e:
      print(e, flush=True)

  def set_routes(self):
    self.add_handler(MessageHandler(get_chars, filters.command(["characters"])))
    self.add_handler(MessageHandler(set_char,  filters.command(["set_character"])))
    self.add_handler(MessageHandler(get_models,filters.command(["models"])))
    self.add_handler(MessageHandler(set_model, filters.command(["set_model"])))
    self.add_handler(MessageHandler(gradio,    filters.command(["gradio"])))
    self.add_handler(MessageHandler(settings,  filters.command(["settings"])))
    self.add_handler(MessageHandler(info,      filters.command(["info"])))
    self.add_handler(MessageHandler(ai,        filters.chat(allowed_chat)), 100)