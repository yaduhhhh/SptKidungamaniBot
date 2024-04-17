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
        await super().start()       
        me = await self.get_me()
        self.id = me.id
        self.mention = me.mention
        self.username = me.username  
        self.uptime = time.time()
        self.log = Config.LOG_CHANNEL
        print(f"{me.first_name} 𝚂𝚃𝙰𝚁𝚃𝙴𝙳 ⚡️⚡️⚡️")
        
    
     

Bot().run()





