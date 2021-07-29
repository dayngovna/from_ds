import discord
import datetime
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from pymongo import MongoClient
import datetime
from asyncio import sleep
import pytz
bot = commands.Bot(command_prefix=">",intents=discord.Intents.all())

vk_session = vk_api.VkApi(os.environ['token'])
session_api = vk_session.get_api()
longpool = VkLongPoll(vk_session)

cluster = MongoClient(os.environ['mongo'] )
bd = cluster["bd"]
collection = bd["vk"]

mass2 = []
@bot.event
async def on_ready():
    while True:
        Emos = pytz.timezone("Europe/Moscow")
        Emos2 = datetime.datetime.now(Emos)
        ekfar = Emos2.strftime("%S")
        await bot.change_presence(status=discord.Status.online,
            activity=discord.Game(ekfar))
        data = collection.find()
        await sleep(5)

        x = collection.find({"new":"yes"})
        for xx in x:
            #print(xx)
            if not xx['super'] in mass2:
                user = bot.get_user(475741103132377101)
                await user.send('['+str(xx['id'])+']''['+str(xx['super'])+'] '+xx['message'])
                mass2.append(xx['super'])       
        print("next")


        
def send_some_msg(id, some_text):
    vk_session.method("messages.send", {"user_id":id, "message":some_text,"random_id":0})


@bot.command()
async def send_vk(ctx,id,super,delete='yes',*,some_text):
    global flag
    if some_text == 'null':
        pass
    else:
        send_some_msg(int(id),some_text)
    if delete == 'yes':
        collection.delete_one({'super':int(super)})
    print(mass2)
    mass2.remove(int(super)) #remove значение #pop индекс

bot.run(os.environ['dstoken'] )


