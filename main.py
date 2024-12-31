#pip install python-telegram-bot
#pip install telebot

from typing import Final
import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackContext
import requests as req
from random import randint, choice
Token : Final = ""
bot_username : Final = "@hardness_quality_bot"
app = Application.builder().token(Token).build()
bot = telegram.Bot(token=Token)

channel_ids = [-1002079726025]
waifu_pics_categoires = ["waifu", "neko", "trap", "blowjob"]
waifu_im_categories = ["ero","ass","hentai","milf","oral","paizuri","ecchi"]
hmtai_categories = ["ass","anal","bdsm","classic","cum","creampie","manga","femdom","hentai","incest","masturbation","public","ero","orgy","elves","yuri","pantsu","pussy","glasses","cuckold","blowjob","boobjob","handjob","footjob","boobs","thighs","ahegao","uniform","gangbang","tentacles","gif","nsfwneko","nsfwmobilewallpaper","zettairyouiki"]
nekos_bot_categories = ["hass","4k","hentai","hneko","hkitsune","hanal","hthigh","tentacle","hboobs","yaoi","paizuri"]
nekos_bot_categories_irl = ["anal", "gonewild", "ass", "pussy", "thigh", "boobs", "pgif"]
# def
def check_online():
    global Token
    url = f"https://api.telegram.org/bot{Token}/getWebhookInfo"
    response = req.get(url)
    return response.json()["ok"]

async def channel_joined(user_id, channel_ids):
    counter = 0
    not_joined_channels = []
    for i in channel_ids:
        is_member = await bot.get_chat_member(chat_id = i, user_id = user_id)
        if is_member.status in ["member", "creator", "administrator"]:
            counter += 1
        else :
            not_joined_channels.append(i)
    if counter == len(channel_ids) :
        return 1
    else :
        return not_joined_channels
    
def channel_not_joined(channel_names):
    channel_names = []
    for i in channel_ids:
        if i == -1002079726025:
            channel_names.append("@hardness_quality")
    channels = ""
    for i in channel_names:
        channels = channels + i + "\n"
    return f"Join the channels below to be able to excute this command :\n{channels}"

def anime_safe():
    url = "https://api.waifu.pics/sfw/waifu"
    res = req.get(url)
    data = res.json()
    if "url" in data:
        return data['url']
    return None

async def delete_command(context : CallbackContext):
    chat_id, msg_id = context.job.data
    await bot.delete_message(chat_id = chat_id, message_id = msg_id)

def store_user(user_id):
    with open("users.txt", 'r') as f:
        if str(user_id) in f.read():
            return
    with open("users.txt", 'a') as f:
        f.write(f"{user_id}\n")

def waifu_pics(category):
    url = f"https://api.waifu.pics/nsfw/{category}"
    res = req.get(url)
    data = res.json()
    if "url" in data:
        return data['url']
    return None

def waifu_im(category):
    params = {
        'included_tags': [f'{category}']
    }
    url = 'https://api.waifu.im/search'
    res = req.get(url, params=params)
    data = res.json()
    return data['images'][0]['url']

def hmtai(category):
    res = req.get(f"https://hmtai.hatsunia.cfd/nsfw/{category}")
    if res.json()['url']:
        return res.json()['url']

def nekos_bot(category):
    params = {'type' : f'{category}'}
    res = req.get("https://nekobot.xyz/api/image", params = params)
    if res.json()['message']:
        return res.json()['message']

def api_detect(category):
    global waifu_pics_categoires, waifu_im_categories, hmtai_categories, nekos_bot_categories
    List = []
    for i in waifu_pics_categoires:
        if category == i:
            List.append(waifu_pics)
            break
    for i in waifu_im_categories:
        if category == i:
            List.append(waifu_im)
            break
    for i in hmtai_categories:
        if category == i:
            List.append(hmtai)
            break
    for i in nekos_bot_categories:
        if category == i:
            List.append(nekos_bot)
            break
    return choice(List)

async def sender(up : telegram.Update, category):
    store_user(up.effective_user.id)
    check = await channel_joined(up.effective_user.id, channel_ids)
    if check == 1:
        url = api_detect(category)(category)
        if '.gif' in url:
            msg = await up.message.reply_animation(animation = url)
        else :
            msg = await up.message.reply_photo(photo = url)
        await up.message.reply_text("deleting after 20 secs, save it before you lose it..")
        with open('total.txt', 'a') as f:
            f.write('.')
        app.job_queue.run_once(delete_command, 20, data = (up.message.chat_id, msg.id))
    else :
        await up.message.reply_text(channel_not_joined(check))

# command
async def start_command(up: telegram.Update, ctx:    ContextTypes.DEFAULT_TYPE):
    ctx_param = ctx.args[0] if ctx.args else None
    if ctx_param == 'ASAPASAP':
        await up.message.reply_text("Hey what the hell are you doing in my house?")
    else :
        await up.message.reply_text("Oh Hello! You are looking for some sus stuff here?\nIf you are, then use the command /help to get started")
    store_user(up.effective_user.id)

async def help_command(up: telegram.Update, ctx:    ContextTypes.DEFAULT_TYPE):
    store_user(up.effective_user.id)
    await up.message.reply_text("/premium : to check if you are a premium member\n/support_channel : get the support channel\n/anime : get sfw waifu pics\n/hnsfw <category> : get nsfw waifu pics\n/nsfw <category> : get nsfw irl pics\n\nmade by nwf")
async def prem_command(up: telegram.Update, ctx:    ContextTypes.DEFAULT_TYPE):
    store_user(up.effective_user.id)
    user_id = up.effective_user.id
    file = "premium.txt"
    with open(file, 'r') as f:
        text = f.read()
        if str(user_id) in text :
            await up.message.reply_text("you are a premium member, here is the owner's username : @noobwhofound")
        else :
            await up.message.reply_text("you are not a premium member")
        await up.message.reply_text("What abilities premium members have?\nprobably nothing... but wait, they can contact the owner and talk with him, for some reasons\n \n how to be a premium member?\nyou cant be one yet but we will see..")

async def anime_command(up: telegram.Update, ctx:    ContextTypes.DEFAULT_TYPE):
    store_user(up.effective_user.id)
    get_anime = anime_safe()
    await up.message.reply_photo(photo = get_anime)


async def hq_channel_command(up: Update, ctx: ContextTypes.DEFAULT_TYPE):
    store_user(up.effective_user.id)
    user = up.effective_user.id
    channel = -1002079726025
    is_member = await bot.get_chat_member(chat_id = channel, user_id = user)
    if is_member.status == "member" or "creator" or "administrator":
        await up.message.reply_text("you are joined, @hardness_quality")
    else :
        await up.message.reply_text("you are not joined, join right now!!! @hardness_quality")

async def hnsfw(up : Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx_param = ctx.args[0].lower() if ctx.args else None
    if (ctx_param in waifu_pics_categoires) or (ctx_param in waifu_im_categories) or (ctx_param in hmtai_categories) or (ctx_param in nekos_bot_categories):
        await sender(up, ctx_param)
    else :
        category = choice(choice([waifu_pics_categoires, waifu_im_categories, hmtai_categories, nekos_bot_categories]))
        await sender(up, category)
        await up.message.reply_text(f"Categories : \n{waifu_pics_categoires}\n{waifu_im_categories}\n{hmtai_categories}\n{nekos_bot_categories}")

async def nsfw(up : Update, ctx: ContextTypes.DEFAULT_TYPE):
    store_user(up.effective_user.id)
    check = await channel_joined(up.effective_user.id, channel_ids)
    if check == 1:
        ctx_param = ctx.args[0].lower() if ctx.args else None
        txt = ""
        if ctx_param in nekos_bot_categories_irl:
            url = nekos_bot(ctx_param)
        else :
            url = nekos_bot(choice(nekos_bot_categories_irl))
            txt = txt + f"Categories : \n{nekos_bot_categories_irl}"
        if '.gif' in url:
            msg = await up.message.reply_animation(animation = url)
        else :
            msg = await up.message.reply_photo(photo = url)
        await up.message.reply_text("deleting after 20 secs, save it before you lose it..")
        app.job_queue.run_once(delete_command, 20, data = (up.message.chat_id, msg.id))
        if txt != "":
            await up.message.reply_text(txt)
    else :
        await up.message.reply_text(channel_not_joined(check))

#error
async def error(up: telegram.Update, ctx:    ContextTypes.DEFAULT_TYPE):
    print(f"update {up} caused error {ctx.error}")

#all in all
if __name__ == "__main__":
    print("starting...")

    #commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("anime", anime_command))
    app.add_handler(CommandHandler("premium", prem_command))
    app.add_handler(CommandHandler("support_channel", hq_channel_command))
    app.add_handler(CommandHandler("hnsfw", hnsfw))
    app.add_handler(CommandHandler("nsfw", nsfw))

    app.add_error_handler(error)
    print("polling")
    app.run_polling(poll_interval=1)

    if check_online():
            print("online message sent")
            bot.send_message(chat_id=-1002079726025, text="Bot is online!\n You can go and do your thing if you know what it means..")
