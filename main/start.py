from datetime import datetime, timedelta
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMediaVideo
from pyrogram.errors import FloodWait, MessageNotModified

from config import Config, Txt
from helper.database import db
from helper.utils import humanbytes
from .groups import GROUPS

@Client.on_message(filters.private & filters.command("start"))
async def start(c, m): 
    user_id = m.from_user.id
    await db.add_user(user_id)
    btn = []
    for group in range(0, len(GROUPS), 2):
        row = []
        row.append(InlineKeyboardButton(GROUPS[group]['name'], f"grp+{group}"))
        if group+1 < len(GROUPS):
            row.append(InlineKeyboardButton(GROUPS[group+1]['name'], f"grp+{group+1}"))
        btn.append(row)
        
    btn.append([InlineKeyboardButton('How To Buy', 'tutorial')])
    photo="https://graph.org/file/e0f0fec6d0b088c41a644.jpg"   
    return await m.reply_photo(photo, caption=Txt.START_TXT.format(m.from_user.mention), parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup(btn))       
  


@Client.on_callback_query()
async def cb_handler(c, q):
    try:
        await cb_func(c, q)
    except MessageNotModified:
        await q.message.edit('wait...')
        await cb_func(c, q)
    except FloodWait as x:
        await asyncio.sleep(x.value)
        await cb_func(c, q)
    except Exception as e:
        print(e)



async def cb_func(client, query):    
    data = query.data
    user_id = query.from_user.id
    if data == "start":    
        btn = []
        for group in range(0, len(GROUPS), 2):
            row = []
            row.append(InlineKeyboardButton(GROUPS[group]['name'], f"grp+{group}"))
            if group+1 < len(GROUPS):
                row.append(InlineKeyboardButton(GROUPS[group+1]['name'], f"grp+{group+1}"))
            btn.append(row)
            
        btn.append([InlineKeyboardButton('How To Buy', 'tutorial')])
        photo="https://graph.org/file/e0f0fec6d0b088c41a644.jpg"   
        await query.edit_message_media(InputMediaPhoto(photo, Txt.START_TXT.format(query.from_user.mention), enums.ParseMode.HTML), InlineKeyboardMarkup(btn))
          
    elif data == "tutorial":
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("◀️ ʙᴀᴄᴋ", "start")]])
        txt = "👆👆 HOW TO JOIN 😍😍👍\n\nഎങ്ങനെ ഗ്രുപ്പ് ഇൽ കേറാം ✅😃"
        await query.edit_message_media(InputMediaVideo(Config.TUTORIAL, caption=txt, parse_mode=enums.ParseMode.HTML), reply_markup=btn)
        
           
    elif data.startswith("grp"):
        group_id = int(data.split('+', 1)[1])
        grp_data = GROUPS[group_id]
        btn = [[
                InlineKeyboardButton(f"ᴩᴀʏ {grp_data['price']}₹", f"buy+{group_id}"),
                ],[
                InlineKeyboardButton("DEMO ᴩɪᴄꜱ 🫦", f'pics+{group_id}')
                ],[
                InlineKeyboardButton('⭐Contact Admin', user_id=7157859848)
                ],[
                InlineKeyboardButton("✘ ᴄʟᴏꜱᴇ", "close"),
                InlineKeyboardButton("◀️ ʙᴀᴄᴋ", "start")
        ]]
        txt = Txt.GRP_FREE.format(us=query.from_user.mention, grp=grp_data['name'], price=grp_data['price'])       
        await query.message.edit(text=txt, parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup(btn))
     
  
    elif data.startswith('pics'):
        group_id = int(data.split('+', 1)[1])
        grp_data = GROUPS[group_id]
        media = [InputMediaPhoto(pic) for pic in grp_data['pics']]
        send = await client.send_media_group(user_id, media=media)
        await send[0].edit(f"👆 DEMO Of {grp_data['name']}")
       
    elif data.startswith("buy"):
        group_id = int(data.split('+', 1)[1])
        grp_data = GROUPS[group_id]
        payment_url = f"upi://pay?pa=BHARATPE09912974503@yesbankltd&pn={grp_data['paynote']}&cu=INR&am={grp_data['price']}"
        
        btn = InlineKeyboardMarkup([[
            #InlineKeyboardButton('Direct Pay', url=payment_url)
            #],[
            InlineKeyboardButton('⭐Contact Admin', user_id=7157859848)
        ]])
       
        txt = Txt.PAY_TEXT.format(price=grp_data['price'], upi=Config.UPI_ID, link=payment_url)
        await query.edit_message_media(InputMediaPhoto(Config.QR_CODE, txt, enums.ParseMode.HTML), btn)
        proof = await client.listen_message(user_id) #, filters=filters.photo)
        if proof.text:
            if proof.text == '/cancel':
                return await proof.reply("Transaction Cancelled! Tap /start", quote=True)
                return await query.message.delete()
            await proof.reply('This Is Text Message. Please Send Screen Shot Of Your Payment. Try Again', quote=True)
            return await query.message.delete()
            
        user = query.from_user
        button = InlineKeyboardMarkup([[
            InlineKeyboardButton('✔️ Accept', callback_data=f'verify_{user.id}_{group_id}')
            ],[
            InlineKeyboardButton('❌ Reject', callback_data=f'reject+{user.id}')
        ]])
        await proof.copy(
            chat_id=client.log,
            caption=Txt.PAY_VERFY_TXT.format(user.mention, user.id, grp_data['name'], grp_data['price']),
            reply_markup=button,
        )
        await proof.reply('Your Proof Is Submitted ✓ admin will verify within MINUTES', quote=True)
      
     
    elif data.startswith('verify'):
        data, us_id, group_id = data.split('_', 2)
        ch_id = GROUPS[int(group_id)]['id']
        
        try:
            link = await client.create_chat_invite_link(int(ch_id), member_limit=1) 
        except:
            return await query.answer("I Can't Create The Link 🥲 Maybe I am Not Admin In This Group. Make Me Admin", show_alert=True)
           
        try:
            await client.send_message(int(us_id), f"Enjoy 🫦\n\nAdmin Accepted Your Payment\nHere Is Your Link: {link.invite_link}\n⚠️One Time Link")
        except:
            await query.answer('I think This pottan is blocked thr bot 😑 so direct share the link', show_alert=True)
       
        return await query.edit_message_reply_markup(InlineKeyboardMarkup([[InlineKeyboardButton('Verified ✅', 'dummy')]]))
       
    elif data.startswith('reject'):
        uid = int(data.split('+', 1)[1])
        try:
            btn = [[InlineKeyboardButton('⭐Contact Admin', user_id=7157859848)]]
            await client.send_message(uid, "Your Transaction Is Declined! Your Payment Is Not Received. Contact Admin", reply_markup=InlineKeyboardMarkup(btn))
        except:
            await query.answer('He Is Blocked The Bot!')
       
        await query.edit_message_reply_markup(InlineKeyboardMarkup([[InlineKeyboardButton('Rejected ❌', 'dummy')]]))
       
    elif data == "close":
        await query.message.delete()
  
