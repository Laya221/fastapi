from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

import time
time.clock = time.time
import openai

temp='%s%k%-%N%V%b%i%n%T%V%Y%L%a%W%N%T%M%9%I%o%u%x%z%T%3%B%l%b%k%F%J%y%h%0%n%P%X%A%s%J%h%7%8%t%W%h%a%2%f%d%z'
api_key=""
for i in range(1,len(temp),2):
    api_key+=temp[i]

openai.api_key = api_key
COMPLETIONS_MODEL = "text-davinci-002"

app = FastAPI()
templates = Jinja2Templates(directory="")
class static:
   first_login=True
   user_info={}
   step='step1'
   history=[]
   my_set=set()
   my_set1=set()
   my_set2=set()
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
  print(prompt)
  print(temp)
  if "no".lower() in temp.lower():
    prompt="""give user example  response for this 'Bot:{}'  """.format(bot_response)
    print('Correct: ',prompt)
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
    bot_response=check(static.history[-1],user_response,'user must to write his name')
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
      bot_response="""select your English Level:
       A1
       A2
       B1
       B2
       C1
       C2?"""
      static.history.append(bot_response)
      return bot_response
  if static.step=='step4':
    bot_response=check(static.history[-1],user_response,'User must to write his English Level from Bot options ')
    if bot_response:
      
      return 'This is Example for Good Response:\n'+bot_response
    else:
      static.history.append(user_response)
      static.step='step5'
      bot_response="""Please choose one or two paths from the following pathes: Travel,Business,Fun/communication,Education,Default / General English """
      static.history.append(bot_response)
      return bot_response
  if static.step=='step5':
    bot_response=check(static.history[-1],user_response,'User must to write his English Path from Bot options')
    if bot_response:
      return 'This is Example for Good Response:\n'+bot_response
    else:
      static.history.append(user_response)
      static.step='step6'
      bot_response="""What are your interests?for example:Sport,Art,History,Technology,Gaming,Movies,...."""
      static.history.append(bot_response)
      return bot_response
  if static.step=='step6':
    bot_response=check(static.history[-1],user_response,'User must to write his his interests')
    if bot_response:
      return 'This is Example for Good Response:\n'+bot_response
    else:
      static.history.append(user_response)
      static.step='step7'
      code_=A2ZBot('Write python code to create dict called "user_info" with following keys "name,age,level,path,interests" and store user data from following history:\n {}'.format(static.history))
      exec('static.'+code_)
      return "Great !!!"
  if static.step=='step7':
    code=A2ZBot("""write python code to create set called my_set2 contain 20 vocabularies (no name) related to user interests '{}' """.format(static.user_info['path']))
    exec('static.'+code)
    code=A2ZBot("""write python code to create set called my_set1 contain 20 vocabularies (no name) related to user interests '{}' """.format(static.user_info['interests']))
    exec('static.'+code)
    static.step='step8'
    
  if static.step=='step8':
    static.my_set=static.my_set1. union(static.my_set2)
    prompt="""say 'Hello {}! ,You will learn following vocabularies {}' """.format(static.user_info['name'],static.my_set)
    bot_response=A2ZBot(prompt)
    static.step='step1'
    static.history=[]  
    return bot_response
  
      



@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/getChatBotResponse")
def get_bot_response(msg: str):
    return str(conversation(msg))

if __name__ == "__main__":
    uvicorn.run("chat:app")
