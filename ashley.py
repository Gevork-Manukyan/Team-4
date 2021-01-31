import discord
import os
from AslRenderer import AslRenderer
from convert import SpeechEngine
from textParser import parse 
import time

client = discord.Client()

speechEngine = SpeechEngine()
aslRenderer = AslRenderer()

def processText(text):

    words = parse(text)
    aslRenderer.renderASL(words)

speechEngine.start(processText)
time.sleep(50)
speechEngine.stop()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

token = os.getenv('TOKEN')
client.run(token)