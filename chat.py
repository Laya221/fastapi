from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import json 
import numpy as np

import random
import time
time.clock = time.time
import openai
import pandas as pd
import numpy as np

openai.api_key = "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"
COMPLETIONS_MODEL = "text-davinci-002"

app = FastAPI()
templates = Jinja2Templates(directory="")
class static:
   first_login=True
   user_data={}
   step='step1'
   history=[]
def A2ZBot(prompt):
  bot_response=openai.Completion.create(
        prompt=prompt,
        temperature=0.9,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        model=COMPLETIONS_MODEL
    )["choices"][0]["text"].strip(" \n")
  return bot_response
def check(bot_response,user_response,problem):
  prompt="""is User response verify the following condition "{}" in following conversation ? return 'yes' if it is true else return 'no' " .\n Bot: {} \nUser: {}""".format(problem,bot_response.strip(),user_response.strip())
  temp=A2ZBot(prompt)
  if "no".lower() in temp.lower():
    prompt="""give user example  response for this 'Bot:{}'  """.format(bot_response)
    result=A2ZBot(prompt)
    return result
  else:
    return False

def conversation(user_response):
  if static.step=='step1':
        static.step='step2'
        bot_response= "What is your name?"
        static.history.append(bot_response)
        return bot_response
  if static.step=='step2':
    bot_response=check(static.history[-1],user_response,'say his name!!!')
    if bot_response:
      return 'This is Example for Good Response:\n'+bot_response
    else:
      static.history.append(user_response)
      static.step='step3'
      bot_response= "Nice to meet you.\nHow old are you?"
      static.history.append(bot_response)
      return bot_response
  if static.step=='step3':
    bot_response=check(static.history[-1],user_response,'User must to write his age ')
    if bot_response:
      
      return 'This is Example for Good Response:\n'+bot_response
    else:
      static.history.append(user_response)
      static.step='step4'
      bot_response="""select your English Level: A1,A2,B1,B2,C1,C2?"""
      static.history.append(bot_response)
      return bot_response
  if static.step=='step4':
    bot_response=check(static.history[-1],user_response,'User must to write his English Level from Bot options ')
    if bot_response:
      
      return 'This is Example for Good Response:\n'+bot_response
    else:
      static.history.append(user_response)
      static.step='step5'
      bot_response="""Great,choose one or two paths: Travel,Business,Fun/communication,Education,Default / General English """
      static.history.append(bot_response)
      return bot_response
  if static.step=='step5':
    bot_response=check(static.history[-1],user_response,'User must to write his English Path from Bot options')
    if bot_response:
      return 'This is Example for Good Response:\n'+bot_response
    else:
      static.history.append(user_response)
      static.step='step1'
      bot_response="""well done,"""
      return bot_response




      



@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/getChatBotResponse")
def get_bot_response(msg: str):
    return str(conversation(msg))

if __name__ == "__main__":
    uvicorn.run("chat:app")
