from pyrogram import filters, Client, enums
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, UsernameInvalid, UsernameNotModified
from config import Config 
from helper.utils import unpack_new_file_id
import re, os, json, base64



@Client.on_message(filters.command('batch') & filters.user(Config.ADMINS))
async def gen_link_batch(bot, message):
    if " " not in message.text: return await message.reply("Use correct format.\nExample <code>/batch https://t.me/****/10 https://t.me/****/20</code>.")
    links = message.text.strip().split(" ")
    if len(links) != 3: return await message.reply("Use correct format.\nExample <code>/batch https://t.me/****/10 https://t.me/***/20</code>.")
    cmd, first, last = links
    
    regex = re.compile("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
    match = regex.match(first)
    if not match: return await message.reply('Invalid link')
        
    f_chat_id = match.group(4)
    f_msg_id = int(match.group(5))
    if f_chat_id.isnumeric():
        f_chat_id = int(("-100" + f_chat_id))

    match = regex.match(last)
    if not match: return await message.reply('Invalid link')
    l_chat_id = match.group(4)
    l_msg_id = int(match.group(5))
    if l_chat_id.isnumeric(): l_chat_id  = int(("-100" + l_chat_id))
    if f_chat_id != l_chat_id: return await message.reply("Chat ids not matched.")
    
    try:
        chat_id = (await bot.get_chat(f_chat_id)).id
    except ChannelInvalid:
        return await message.reply('This may be a private channel / group. Make me an admin over there to index the files.')
    except (UsernameInvalid, UsernameNotModified):
        return await message.reply('Invalid Link specified.')
    except Exception as e:
        return await message.reply(f'Errors - {e}')

    sts = await message.reply("Generating link for your message.\nThis may take time depending upon number of messages")
    string = f"{f_msg_id}_{l_msg_id}_{chat_id}_{cmd.lower().strip()}"
    b_64 = base64.urlsafe_b64encode(string.encode("ascii")).decode().strip("=")
    return await sts.edit(f"Here is your link https://t.me/{bot.username}?start=DSTORE-{b_64}")
