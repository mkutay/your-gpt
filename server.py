import discord
import openai
import random
from dotenv import load_dotenv
import os

load_dotenv()

client = discord.Client(intents=discord.Intents.all())
token = os.getenv("DISCORD_TOKEN")

openai.api_key = os.getenv("OPENAI_KEY")

stop = 0

info = {}

log = []

user = "User"

models = [{"model": "curie:ft-personal-2023-05-28-11-17-28", "temperature": 0.80, "stop": "\n"}]

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  
  ra = random.randint(0, 20)

  msg = message.content

  if (msg[0] == '!' or message.channel.name != "kutai") and ra != 5:
    return

  if len(log) >= 2:
    log.pop(0)
  log.append({"u": user, "m": message.content})

  if message.author == client.user:
    return

  prompt = ""

  for l in range(len(log)):
    prompt += log[l]["u"] + ": " + log[l]["m"] + "\n"
  prompt += "kutay:"

  model = models[0]

  response = openai.Completion.create(model = model["model"], prompt = prompt, stop = model["stop"], temperature = model["temperature"])

  response = response["choices"][0]["text"]

  log.append({"u": "kutay", "m": response})

  await message.channel.send(response)
  print(log)
client.run(token)
