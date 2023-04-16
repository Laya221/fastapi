from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import json 
import numpy as np
from fastapi import FastAPI, Request, Form
import random
import time
time.clock = time.time
import openai
import os 


temp='%s%k%-%N%V%b%i%n%T%V%Y%L%a%W%N%T%M%9%I%o%u%x%z%T%3%B%l%b%k%F%J%y%h%0%n%P%X%A%s%J%h%7%8%t%W%h%a%2%f%d%z'
api_key=""
for i in range(1,len(temp),2):
    api_key+=temp[i]
os.environ["OPENAI_API_KEY"] = api_key

openai.api_key = api_key
COMPLETIONS_MODEL = "text-davinci-002"

app = FastAPI()
templates = Jinja2Templates(directory="")
class static:
   user_data=None
   email=None
   step='step1'
   history=[]
   vocabs=[]
   messages=[]
   template="""
   You are A2ZBot  (Artificial Intelligence Bot) to make warmup conversation in english with user,You must chat user in A funy way.
    Be kind,be creative , smart,interesting,friendly and funny.
    user information:user name is {},english level is {},interests and goals are  {}.
    please chat user with his name.
    you must to tell user if his response incorrect based on grammar and spelling.
    don't ask questions back! 
    use short questions.
    Use many Emojis.
    don't generate chat_history.
    you must to suggest topics related to user interests.
    allow to user to leave if he want and say goodbye and please do not ask him about next session.
    tell user about A2Zbot if he ask some thing like "who are you?","what can you do?","what is your goals?".
    you must do the folloing steps each seperatly.
    step1:firstly please resonse to user in smart way then tell user about A2ZBot then ask user "how he is doing?" in the same response.
    step2:after telling user about A2Zbot please ask user "how he is doing?"
    step3:you must tell user some jokes(Questions Jokes) or advices Especially if it's in a bad mood or doesn't want to learn,please choose jokes related to user interests.
    step4:finally you must to ask user if he is ready to start english journey for today after you did previous steps.
    step5:create mini study plan for learning vocabulary based on english level and topics and goal.
    step6:after english session you must to ask user about his feedback about A2Zbot "if the bot is helpful".
    Answer: return only A2ZBot response.
   """
def warmup(text):
    system_role={"role": "system", "content": static.template}
    
    assistant_role={"role": "assistant", "content": "generate one response.generate short question.don't generate chat_history."}

    static.messages.append(system_role)
    static.messages.append(assistant_role)
    if text:
        static.messages.append({"role": "user", "content": text})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=static.messages,temperature=0.9
        )
        reply = chat.choices[0].message.content
        static.messages.append({"role": "assistant", "content": reply})
        return reply
   
def vocabularies(number,domain):
    text='more than {} "{}" vocabularies without duplicating,please return as following:word,word,'.format(number,domain)
    messages=[]
    system_role={"role": "system", "content": """You are smart bot to return specific vocabularies,please do not say anything to user,assistant reply must be like this :word,word,.."""}
    user_role={"role": "user", "content": "more than 3 Travel vocabularies without duplicating"}

    assistant_role={"role": "assistant", "content": "Adventure,Boarding pass,Explorer,Journey"}

    messages.append(system_role)
    messages.append(user_role)
    messages.append(assistant_role)
    if text:
        messages.append({"role": "user", "content": text})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages,temperature=0.9
        )
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply

def A2ZBot(prompt):
  bot_response=openai.Completion.create(
        prompt=prompt,
        temperature=0.9,
        max_tokens=700,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        model=COMPLETIONS_MODEL
    )["choices"][0]["text"].strip(" \n")
  return bot_response
def check(bot_response,user_response,problem):
  #prompt=""""please return "yes" if user response '{}' that is related to bot response: '{}',user response should be '{}' """.format(user_response.strip(),bot_response.strip(),problem)
  prompt="""is User response verify the following condition "{}" in following conversation ? return 'yes' if it is true else return 'no' " .\n Bot: {} \nUser: {}""".format(problem,bot_response.strip(),user_response.strip())
  temp=A2ZBot(prompt)
  if "yes".lower() not in temp.lower():
    prompt="""give user example  response for this 'Bot:{}'  """.format(bot_response)
    print('Correct: ',prompt)
    result=A2ZBot(prompt)
    return result
  else:
    return False
def conversation(user_response):
  if user_response=='START_STUDY_PLAN':
    static.step=='step10'
  if user_response=='RESET':
    static.messages=[]
  if static.step=='step1':
        static.step='step2'
        bot_response= "What is your name?"
        static.history.append(bot_response)
        return bot_response
  if static.step=='step2':
    bot_response=check(static.history[-1],user_response,'user must to write his name')
    if bot_response:
      return 'This is an example for good response:\n'+bot_response
    else:
      static.history.append(user_response)
      static.step='step3'
      bot_response= "Nice to meet you.\nHow old are you?"
      static.history.append(bot_response)
      return bot_response
  if static.step=='step3':
    bot_response=check(static.history[-1],user_response,'User must to write his age ')
    if bot_response:
      
      return 'This is an example for good response:\n'+bot_response
    else:
      static.history.append(user_response)
      static.step='step4'
      bot_response="""What is your current english level:
       <ul>
       <li>* A1</li>
       <li>* A2</li>
       <li>* B1</li>
       <li>* B2</li>
       <li>* C1</li>
       <li>* C2</li>
       </ul>
       """
      static.history.append(bot_response)
      return bot_response
  if static.step=='step4':
    bot_response=check(static.history[-1],user_response,'User must to write his English Level from Bot options ')
    if bot_response:
      
      return 'This is an example for good response:\n'+bot_response
    else:
      static.history.append(user_response)
      static.step='step5'
      bot_response="""What is your target english level:
       <ul>
       <li>* A1</li>
       <li>* A2</li>
       <li>* B1</li>
       <li>* B2</li>
       <li>* C1</li>
       <li>* C2</li>
       </ul>
      """
      static.history.append(bot_response)
      return bot_response
  if static.step=='step5':
    bot_response=check(static.history[-1],user_response,'User must to write his English Level from Bot options ')
    if bot_response:
      
      return 'This is an example for good response:\n'+bot_response
    else:
      static.history.append(user_response)
      static.step='step6'
      bot_response="""Please choose one or two paths from the following pathes: 
      <ul>
       <li>* Travel</li>
       <li>* Business</li>
       <li>* Fun/communication</li>
       <li>* Education</li>
       <li>* Default,General English</li> 
       </ul>
      """
      static.history.append(bot_response)
      return bot_response
  
  if static.step=='step6':
    bot_response=check(static.history[-1],user_response,'User must to write his English Path from Bot options')
    if bot_response:
      
      return 'This is an example for good response:\n'+bot_response
    else:
      static.history.append(user_response)
      static.step='step7'
      bot_response="""what are your interests?
      <ul>
         <li> 1. Sport </li> 
        <li>2. Art </li> 
         <li> 3. History </li> 
         <li> 4. Technology </li> 
         <li> 5. Gaming </li> 
         <li> 6. Movies </li> 
         <li> 7. Culture </li> 
         <li> 8. Management </li> 
         <li> 9. Science </li> 
         <li> 10. Adventure </li> 
         <li> 11. Space </li> 
         <li> 12. Cooking </li> 
         <li> 13. Reading </li> 
         <li> 14. Lifestyle </li>
         <li> ... </li> 
       </ul>
      """
      static.history.append(bot_response)
      return bot_response
  if static.step=='step7':
    bot_response=check(static.history[-1],user_response,'User must to write his his interests')
    if bot_response:
      return 'This is an example for good response:\n'+bot_response
    else:
      static.history.append(user_response)
      static.step='step8'
      code_=A2ZBot('Write python code to create dict called "user_details" with following keys "name,age,current_english_level,path,target_english_level,path,interests" and store user data from following history:\n {}'.format(static.history))
      exec('static.'+code_)
      time.sleep(3)  
      return """Let's start our journey in English.<br><span style="color:green">Type <b>OK</b> to continue..</span>"""
  if static.step=='step8':
 
    temp1=A2ZBot("""return more than 100 {} vocabularies  for {} english level as following:
                word,word,word
                """.format(static.user_details['path'],static.user_details['current_english_level']))
    temp1=vocabularies(100,static.user_details['path'])
    temp2=vocabularies(50,static.user_details['interests'])
    static.vocabs=temp1.split(',')+temp2.split(',')
    with open("user_data.json", "r") as read_file:
      data = json.load(read_file)
    data[static.email]["user_details"]=static.user_details
    data[static.email]["vocabs"]=static.vocabs
    with open("user_data.json", "w") as write_file:
      json.dump(data, write_file)
    static.step='step9'
    return """Thanks for your time, your information has been successfully collected and you can start your journey with A2ZBot.<br><span style="color:green">Type <b>Hello</b> to start warmup conversation</span>"""
  
  if static.step=='step9':
    with open("user_data.json", "r") as read_file:
      data = json.load(read_file)
    static.user_data=data[static.email]
    static.template=static.template.format(static.user_data['user_details']['name'],static.user_data['user_details']['current_english_level'],static.user_data['user_details']['interests']+' '+static.user_data['user_details']['path'])
    try:
      return warmup(user_response)
    except:
      return """I'm Sory!!, warmup Conversation size exceeds available limits,let's move to your study plan.or type 'RESET' to restart"""

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/SignUp")
async def form_post(request: Request, username: str = Form(...),email: str = Form(...),password: str = Form(...)):
    with open("user_data.json", "r") as read_file:
      data = json.load(read_file)
    data[email]={'username':username,'password':password}
    with open("user_data.json", "w") as write_file:
      json.dump(data, write_file)
    return templates.TemplateResponse("login.html", {"request": request})
@app.post("/Login")
async def form_post(request: Request,email: str = Form(...),password: str = Form(...)):
    with open("user_data.json", "r") as read_file:
      data = json.load(read_file)
    try:
       
      static.email=email
      static.user_data=data[email]
      if static.user_data['password']==password:
        if 'user_details' in data[email].keys():
          static.step='step9'

        return templates.TemplateResponse("index.html", {"request": request})
      else:
        return templates.TemplateResponse("login.html", {"request": request})
    except:
      pass
@app.get("/getChatBotResponse")
def get_bot_response(msg: str):
      return str(conversation(msg))
    


if __name__ == "__main__":
    uvicorn.run("chat:app")
