import os
import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from openai import OpenAI
import json

app = FastAPI()

static_path = os.path.join(os.path.dirname(__file__), "static")
templates_path = os.path.join(os.path.dirname(__file__), "templates")

app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(directory=templates_path)

client = OpenAI(
    api_key="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",
)

with open("./data/summarize_english.txt", "r", encoding='utf-8') as file:
    summarize = file.read().strip()
content = "요약본:" + summarize
with open("./data/wrong_answer_english.txt", "r", encoding='utf-8') as file:
    wrong_note = file.read().strip()
with open("./data/instructions.txt", "r", encoding='utf-8') as file:
    instructions = file.read().strip()

wrong_note = "오답노트:" + wrong_note + "\n"
content = content + wrong_note + instructions

def parsing_question(wn):

    problems = [problem.strip() for problem in wn.split("문제 :")]

    # 첫 번째 요소는 빈 문자열이 될 수 있으므로 제외
    problems = problems[1:]

    # 결과 출력 또는 저장
    for problem in problems:
        print("문제 :", problem)
        print("-" * 50)  # 각 문제 사이에 구분선을 넣어 출력
    return problems
#parsing_question(wrong_note)

def more_info(data):
    response = client.chat.completions.create(
        messages=[
            {
            "role": "user",
            "content": str(data)
            }
            
        ],
        model="gpt-4-1106-preview",
    )
    
    gpt4_Prescription_response = response.choices[0].message.content
    return gpt4_Prescription_response

def SummarizeWrongAnswerKeyword(data):
    Answer = more_info(data)
    print(Answer)
    print("=====================================================================================================")
    # "Keyword:" 이전의 문자열 추출
    keyword_start = Answer.find("KEYWORD") if "KEYWORD" in Answer else Answer.find("키워드")
    pre_keyword_text = Answer[:keyword_start].strip()

    # "Keyword:" 이후의 문자열 추출
    keywords_start = keyword_start + len("KEYWORD") if "KEYWORD" in Answer else keyword_start + len("키워드")
    keywords_text = Answer[keywords_start:].strip()

    # "Keyword:" 이전의 데이터와 키워드를 각각의 변수에 저장
    pre_keyword_data = pre_keyword_text

    # 결과 출력 또는 저장
    print("Pre-Keyword Data:")
    print(pre_keyword_data)
    print("=====================================")
    print("\nKeywords:")

    resultDict = {}
    question = parsing_question(wrong_note)
    keywordList = keywords_text.splitlines()
    i = 0
    for keyword in keywordList:
        keyword1 = keyword[keyword.index("[") + 1: keyword.index(",")]
        keyword2 = keyword[keyword.index(",") + 2: keyword.index("]")]
        resultDict[question[i]] = [keyword1, keyword2]
        i += 1
    print(resultDict)
    return resultDict



@app.get("/")
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.post("/remind/")
async def add_note(request: Request):
    summarize2json = summarize
    #combine = SummarizeWrongAnswerKeyword(content)
    combine = {"What choice does the Greedy algorithm always make in a given problem situation:\nA. Worst choice\nB. Random choice\nC. Optimal choice\nD. First choice\nCorrect answer: C\nIncorrect answer: B": ['Greedy', 'optimal'], 'Dynamic programming is most effective for problems with which characteristics:\nA. Overlapping subproblems\nB. Non-overlapping subproblems\nC. Independent subproblems\nD. All subproblems\nCorrect answer: A\nIncorrect answer: B': ['Dynamic', 'subproblems'], 'In which way does the backtracking algorithm solve the problem:\nA. Bottom-up approach\nB. Top-down approach\nC. Both\nD. Neither\nCorrect Answer: B\nIncorrect Answer: A': ['transforming', 'simplification']}
    combine_json = json.dumps(combine)
    return templates.TemplateResponse("result.html", {"request": request, "sum" : summarize2json, "combine": combine_json}) 

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
