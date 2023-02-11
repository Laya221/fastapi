from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import time
#import spacy.cli 
time.clock = time.time
import spacy
nlp = spacy.load("en")


app = FastAPI()

templates = Jinja2Templates(directory="")


# Create a ChatBot instance
chatbot = ChatBot(name='MyChatBot', read_only=True, logic_adapters=['chatterbot.logic.BestMatch'])

# Create a ChatterBot trainer
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot using the English corpus
trainer.train("chatterbot.corpus.english")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/getChatBotResponse")
def get_bot_response(msg: str):
    return str(chatbot.get_response(msg))
