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
    print("Plain text: " + str(text))
    words = parse(text)
    print("ASL as text: " + str(words))
    aslRenderer.renderASL(words)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$ashleyStart'):
        speechEngine.start(processText)

    
    if message.content.startswith('$ashleyStop'):
        speechEngine.stop()

token = os.getenv('TOKEN')
client.run(token)