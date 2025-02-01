import os

from fastapi import FastAPI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from pydantic import BaseModel

from prompts import final_prompt

load_dotenv()

app = FastAPI()

model = ChatGroq(
    model_name="mixtral-8x7b-32768", api_key=os.environ.get("GROQ_API_KEY")
)
chain = final_prompt | model


class Item(BaseModel):
    user_input: str


@app.post("/chat")
def chat(item: Item):
    return {"answer": chain.invoke({"user_input": item.user_input}).content}




