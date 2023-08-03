import os
import speech_recognition as sr
from colorama import Fore, Back, Style
import openai
import time
import json

# 建立Recognizer物件
r = sr.Recognizer()

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

path = 'output.json'

with open(path, 'r') as f:
    json_file = json.load(f)

def speechAssistant():
  # 開啟麥克風並進行錄音
  with sr.Microphone() as source:
      print("\n\033[1;31m 請開始說話... \033[0m")
      audio = r.listen(source)
  # 使用Google語音辨識引擎將錄音轉換為文字
  try:
      text = r.recognize_google(audio, language='zh-TW')
      print(Fore.GREEN + "您說的是：" + text)
      return str(text)
  except sr.UnknownValueError:
      print("無法辨識您的語音")
      return None
  except sr.RequestError as e:
      print("無法連線至Google語音辨識服務：{0}".format(e))
      return None

def checkJSON():
  if "messages" not in json_file:
    json_file["messages"] = []
    json_file["messages"].append({"role": "system", "content": "You are a helpful assistant."})
    return
  elif len(json_file["messages"]) == 0:
    json_file["messages"].append({"role": "system", "content": "You are a helpful assistant."})
    return

def checkTokenUsage(token_usage):
  if token_usage > 4000:
    print("\n\033[1;31m OpenAI API Token Limit Exceeded \033[0m")
    json_file["messages"] = []
    with open(path, 'w') as f:
      json.dump(json_file, f, indent=4)
    return True
  else:
    return False

def Ask():
  global mode
  if mode == "1":
    prompt = input("\n\033[1;34m 請輸入您的問題: \033[0m")
  elif mode == "2":
    prompt = speechAssistant()

  if prompt == "exit" or prompt == "離開" or prompt == None:
    os._exit(0)
  elif prompt == "切換模式" or prompt == "cm":
    if mode == "1":
      mode = "2"
    else:
      mode = "1"
    return

  content = {"role": "user", "content": prompt}
  json_file["messages"].append(content)

  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=json_file["messages"],
    temperature=0.7,
    presence_penalty=0.6,
    frequency_penalty=0.5,
  )
  
  token_usage = completion["usage"]["total_tokens"]
  if checkTokenUsage(token_usage):
    checkJSON()
    return

  print("\n" + completion['choices'][0]['message']['content'] + "\n")
  feedback = {"role": "assistant", "content": completion['choices'][0]['message']['content']}

  json_file["messages"].append(feedback)

  with open(path, 'w') as f:
    json.dump(json_file, f, indent=4)
  
  print("Press any key to continue...")
  input()
  

if __name__ == '__main__':

  checkJSON()
  global mode
  mode = input("請輸入模式 (文字: 1 語音: 2) : ")
  if mode != "1" and mode != "2":
    mode = "1"
    print(Fore.WHITE+Style.BRIGHT+"Using default mode: 1")
  while True:
    Ask()
    time.sleep(1)
