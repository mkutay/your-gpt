import json
from datetime import datetime, timedelta

def timestamp_microsecond(utc_time):
  epoch = datetime(1970, 1, 1)
  td = utc_time - epoch
  assert td.resolution == timedelta(microseconds = 1)
  return (td.days * 86400 + td.seconds) * 10 ** 6 + td.microseconds


chat_n = 5 # number of chats to be processed 

chats = []

for chat_num in range(1, chat_n + 1):
  with open("./original-chats/chat-{}.txt".format(chat_num), "r") as f:
    chat = []
    for line in f.readlines():
      if "‎" in line:
        continue
      if line[0] != "[" or (line[20] != "]" and line[19] != "]"):
        continue
      if line[6] == ",": # if there are any more exceptions than i am going to explode
        continue

      date = ""
      for i in range(1, 21):
        if line[i] == "]":
          break
        date += line[i]
      microseconds = timestamp_microsecond(datetime.strptime(date, "%d.%m.%Y %H:%M:%S"))

      if line[20] == "]":
        start = 20
      elif line[19] == "]":
        start = 19
      else:
        assert False # FUCK
      
      semicolon = -1

      name = ""
      for i in range(start + 2, len(line)):
        if line[i] == ":":
          semicolon = i
          break
        name += line[i]

      assert semicolon != -1

      message = line[semicolon + 2:len(line) - 1]

      chat.append({"microseconds": microseconds, "name": name, "message": message})
    chats.append(chat)
    print(len(chat))

for chat_num in range(len(chats)):
  with open("./refactored-chats/chat-{}.jsonl".format(chat_num + 1), "w") as f:
    for chat_line in chats[chat_num]:
      f.write(json.dumps(chat_line) + "\n")

