import logging, logging.config, os, sys, asyncio, time
from pyropatch import flood_handler, listen  
from pyrogram import Client
from config import Config                     


# Get logging configurations
#logging.config.fileConfig('logging.conf')
#logging.getLogger().setLevel(logging.INFO)
#logging.getLogger("pyrogram").setLevel(logging.DEBUG)


class Bot(Client):
    def __init__(self):
        super().__init__(
            name="PayBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={"root": "main"}            
        )

    async def start(self):
        try:
            await super().start()       
            me = await self.get_me()
            self.id = me.id
            self.mention = me.mention
            self.username = me.username  
            self.uptime = time.time()
            self.log = Config.LOG_CHANNEL
            print(f"{me.first_name} 𝚂𝚃𝙰𝚁𝚃𝙴𝙳 ⚡️⚡️⚡️")
            try: [await self.send_message(id, "Bot Restarted ✓") for id in Config.ADMINS ]                   
            except: pass
        except Exception as e:
            await self.send_message(1896730469, e)
            await asyncio.sleep(5)
            os.system('git pull')
            os.execl(sys.executable, sys.executable, "bot.py")
    
     

Bot().run()





