import json
import math
from datetime import datetime, timedelta

name = "kutay"

user = "User"

chat_n = 5

train_data = []

for chat_num in range(1, chat_n + 1):
  chat = []
  with open("./refactored-chats/chat-{}.jsonl".format(chat_num), "r") as f:
    last_j = {"name": "", "microseconds": 0, "message": ""}
    tot_message = ""
    for line in f.readlines():
      j = json.loads(line)
      if last_j["name"] == j["name"]:
        tot_message += " " + j["message"]
      else:
        bol = j["message"]
        last_j["message"] = tot_message
        chat.append(last_j)
        tot_message = bol
      last_j = j

  def get_log(m):
    prompt = ""
    completion = " " + chat[m]["message"] + "\n"
    last_ms = chat[m - 5]["microseconds"]
    for i in range(m - 5, m):
      if chat[i]["name"] == name:
        prompt += name + ": " + chat[i]["message"] + "\n"
      else:
        prompt += user + ": " + chat[i]["message"] + "\n"
    prompt += name + ":"
    if len(prompt) > 1000 or len(completion) > 1000:
      return -1
    return {"prompt": prompt, "completion": completion}

  for m in range(len(chat)):
    if chat[m]["name"] == name:
      pc = get_log(m)
      if pc == -1:
        continue
      train_data.append(pc)

with open('./train_data.jsonl', 'w') as f:
  for i in range(len(train_data)):
    if i % 20 == 0:
      f.write(json.dumps(train_data[i]) + "\n")