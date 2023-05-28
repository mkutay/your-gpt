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

models = [{"model": "babbage:ft-personal-2022-09-18-11-37-47", "temperature": 0.80, "logprobs": 1, "stop": "\n", "top_p": 0.80}]

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  msg = message.content

  if msg[0] == '!'  or message.channel.name == "nobot":
    return
  global stop, info, log
  if len(log) >= 5:
    log.pop(0)
  log.append({"u":message.author.name, "m":message.content})
  if message.author == client.user:
    return
  if "dont stop kutay" in msg:
    await message.channel.send('tamam devam ediom (durdurmak icin "stop kutay" de)')
    stop = 0
  elif "stop kutay" in msg:
    await message.channel.send('tamam duruom (devam ettirmek icin "dont stop kutay" de)')
    stop = 1

  if stop == 1:
    return

  if random.randint(1, 100) > 3:
    return

  prompt = ""

  for l in range(len(log)):
    prompt += log[l]["u"] + ": " + log[l]["m"] + "\n"
  prompt += "kutay:"

  # model = random.choice(models)
  model = models[0]

  response = openai.Completion.create(model=model["model"], prompt=prompt, top_p=model["top_p"], logprobs=model["logprobs"], stop=model["stop"])
  # print(response)
  # print(prompt, "\n")
  response = response["choices"][0]["text"]

  await message.channel.send(response)
  #for s in send:
      #await message.channel.send(s)

client.run(token)
