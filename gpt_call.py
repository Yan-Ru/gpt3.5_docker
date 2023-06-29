import os
import openai
import time
import json

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

path = 'output.json'

with open(path, 'r') as f:
    json_file = json.load(f)

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
  prompt = input("\n\033[1;34m 請輸入您的問題: \033[0m")
  if prompt == "exit":
    os._exit(0)

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

if __name__ == '__main__':

  checkJSON()
  while True:
    Ask()
    time.sleep(1)
