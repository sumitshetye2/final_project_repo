from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

system_prompt = """
    You are a helpful assistant that critiques student feedback on presentations.
    Your goal is to help students improve their ability to give meaningful, specific, and constructive feedback.
"""

class FeedbackInput(BaseModel):
    feedback: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

from openai import OpenAI

client = OpenAI()  # Automatically uses OPENAI_API_KEY from environment

@app.post("/meta_critique")
async def critique_feedback(data: FeedbackInput):
    user_feedback = data.feedback

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_feedback}
        ]
    )

    return {
        "meta_feedback": response.choices[0].message.content
    }

