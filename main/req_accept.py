from pyrogram import filters, Client, errors, enums
from pyrogram.errors import PeerIdInvalid
from config import Config, Txt
from helper.database import db
import random 

    
@Client.on_chat_join_request(filters.channel & filters.chat(Config.REQ_CHATS))
async def approve(c, m):
    user = m.from_user
    chat = m.chat
 
    try:
        await db.add_user(user.id)
        await c.approve_chat_join_request(chat.id, user.id)  
        
        await c.send_message(
            user.id,
            #photo=random.choice(Config.PICS), 
            text=Txt.REQ_ACCEPTED_TXT.format(user.mention, chat.title)
        )

    except PeerIdInvalid as e: print(e)
    except Exception as e: print(e)


