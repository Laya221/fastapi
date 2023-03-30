
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from fastapi import APIRouter, Request, Depends, responses, status
from fastapi.templating import Jinja2Templates

import numpy as np
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain import OpenAI, LLMChain, PromptTemplate
#from langchain.chat_models import ChatOpenAI
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

app = FastAPI()
templates = Jinja2Templates(directory="")

class static:
   template="""You are A2ZBot assistant (Artificial Intelligence Bot) to learn user english,you can learn user  english vocabularies with examples and in a fun way.
    Be kind,be creative , smart,interesting,friendly and funny.
    don't ask questions back! 
    use short questions.
    Use Emojis.
    don't generate chat_history.
    allow to user to leave if he want and say goodbye.
    you must do the folloing steps each seperatly:
    step1:tell user about A2ZBot then ask user how is doing today.
    step2:you must tell user some jokes or advices Especially if it's in a bad mood or doesn't want to learn.
    step3:you must to ask user anout his feedback about A2Zbot "if the bot is helpful".
    step4:finally you must to ask user if he is ready to start english journey for today after you did previous steps.
    step5:create mini study plan for learning vocabulary based on english level and topics and goal.
    Answer: return only A2ZBot response.
    history:
    {chat_history}
    user: {question}
    A2Zbot: generate one response.generate short question.don't generate chat_history.
    """
   memory=ConversationBufferMemory(memory_key="chat_history")
def conversation(msg):
    
   prompt_template = PromptTemplate(input_variables=["chat_history","question"], template=static.template)
   llm_chain = LLMChain(
        llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0.6,
        max_tokens=300, n=1),
        prompt=prompt_template,
        verbose=False,
        memory=static.memory,
   
        )
   result=llm_chain.run(msg)
   time.sleep(0.5)
   return result.replace('A2ZBot:','',-1)



@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/getChatBotResponse")
def get_bot_response(msg: str):
    return str(conversation(msg))


