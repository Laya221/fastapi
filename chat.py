from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/chat/{message}")
def chat(message: str):
    response = "I'm sorry, I don't understand your message."
    if "hello" in message.lower() or "hi" in message.lower():
        response = "Hello! How can I help you with web development today?"
    elif "html" in message.lower():
        response = "HTML stands for Hypertext Markup Language and is used for creating web pages."
    elif "css" in message.lower():
        response = "CSS stands for Cascading Style Sheets and is used for styling web pages."
    elif "javascript" in message.lower():
        response = "JavaScript is a programming language used for creating interactive elements on web pages."
    return {"message": response}
