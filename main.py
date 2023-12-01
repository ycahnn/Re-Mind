import os
import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from openai import OpenAI

client = OpenAI(
    api_key="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",
)

def more_info(data):
    response = client.chat.completions.create(
        messages=[
            {
            "role": "assistant",

                "content": content
            },
            {
            "role": "user",
            "content": str(data)
            }
            
        ],
        model="gpt-4-1106-preview",
    )
    
    gpt3_Prescription_response = response.choices[0].message.content
    print(gpt3_Prescription_response) 
    return gpt3_Prescription_response

with open("./data/summarize.txt", "r", encoding='utf-8') as file:
    summarize = file.read().strip()
content = "요약본:" + summarize
with open("./data/wrong_answer.txt", "r", encoding='utf-8') as file:
    wrong_note = file.read().strip()

wrong_note = "오답노트:" + wrong_note + "\n"
instructions = ": Analyze the contents of the wrong answer note and the summary note and add information about the wrong answer to the summary if the wrong answer has something that isn't in the summary note. Prints added summaries."
content = content + wrong_note + instructions
print(content)
more_info(content)

app = FastAPI()

static_path = os.path.join(os.path.dirname(__file__), "static")
templates_path = os.path.join(os.path.dirname(__file__), "templates")

app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(directory=templates_path)

@app.get("/")
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

#if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=80)
