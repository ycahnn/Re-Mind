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

with open("./data/summarize.txt", "r", encoding='utf-8') as file:
    summarize = file.read().strip()
content = "요약본:" + summarize
with open("./data/wrong_answer.txt", "r", encoding='utf-8') as file:
    wrong_note = file.read().strip()
with open("./data/instructions.txt", "r", encoding='utf-8') as file:
    instructions = file.read().strip()
wrong_note = "오답노트:" + wrong_note + "\n"
content = content + wrong_note + instructions

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
    return gpt3_Prescription_response

def SummarizeWrongAnswerKeyword(data):
    Answer = more_info(data)

    # "Keyword:" 이전의 문자열 추출
    keyword_start = Answer.find("Keyword:") if "Keyword:" in Answer else Answer.find("키워드:")
    pre_keyword_text = Answer[:keyword_start].strip()

    # "Keyword:" 이후의 문자열 추출
    keywords_start = keyword_start + len("Keyword:") if "Keyword:" in Answer else keyword_start + len("키워드:")
    keywords_text = Answer[keywords_start:].strip()

    # "Keyword:" 이전의 데이터와 키워드를 각각의 변수에 저장
    pre_keyword_data = pre_keyword_text
    keywords_list = [keyword.strip() for keyword in keywords_text.split(",")]

    # 결과 출력 또는 저장
    print("Pre-Keyword Data:")
    print(pre_keyword_data)
    print("=====================================")
    print("\nKeywords:")
    for keyword in keywords_list:
        print(keyword)

SummarizeWrongAnswerKeyword(content)
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
