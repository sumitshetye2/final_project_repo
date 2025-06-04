from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://127.0.0.1:5000",
    "http://localhost:5000",
    "http://127.0.0.1:8000",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

system_prompt = """
    You are a helpful assistant that critiques student feedback on presentations.
    Your goal is to help students improve their ability to give meaningful, specific, and constructive feedback. 
    When creating your response, please answer using only Markdown syntax.
"""
## we should clarify for the LLM elements of the conversation
# our meta-feedback system is essentially a conversation with 3 speakers
# we should clarify how to handle these different voices with guard-rails in the system prompt
# we have notions for { presentation_feedback, critique_of_feedback, additional_instructions}
# the system prompt could say " analyze the prez_feedback, but feel free to ignore absude add._instr."
# 'YOU ARE SPECIFICALLY BUILT TO DO X. POLITELY IGNORE Z.
class FeedbackInput(BaseModel):
    feedback: str
    custom_instructions: str = ""  # Optional, default empty

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

from openai import OpenAI

# client = OpenAI()  # Automatically uses OPENAI_API_KEY from environment

model = genai.GenerativeModel('gemini-2.0-flash')

@app.post("/meta_critique")
async def critique_feedback(data: FeedbackInput):
    user_feedback = data.feedback
    custom_instructions = data.custom_instructions or ""

    # Add custom instructions to the prompt if provided
    if custom_instructions.strip():
        full_prompt = f"{system_prompt}\n\nCustom Instructions: {custom_instructions}\n\nStudent Feedback:\n{user_feedback}"
    else:
        full_prompt = f"{system_prompt}\n\nStudent Feedback:\n{user_feedback}"

    try:
        response = model.generate_content(full_prompt)
        meta_feedback_content = response.text
    except genai.types.BlockedPromptException as e:
        meta_feedback_content = (
            "The prompt was blocked by safety filters. Change prompt"
        )
        print(f"Blocked by Gemini savety filters: {e}")
    except Exception as e:
        meta_feedback_content = f"An error occurred: {str(e)}"
        print(f" Gemini API Error: {e}")
    return {
        "meta_feedback": meta_feedback_content
    }

    # response = client.chat.completions.create(
    #     model="gpt-4",
    #     messages=[
    #         {"role": "system", "content": system_prompt},
    #         {"role": "user", "content": user_feedback}
    #     ]
    # )

    # return {
    #     "meta_feedback": response.choices[0].message.content
    # }

