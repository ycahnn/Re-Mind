import re

resultDict = {}
keywordText = "1. 그리디 알고리즘[최적의 선택, 최적화 문제]\n2. 다이나믹 프로그래밍[하위 문제, 중복]\n3. 백트래킹 알고리즘[되돌아가기, 하향식]"
keywordList = keywordText.splitlines()
i = 1
for keyword in keywordList:
    keyword1 = keyword[keyword.index("[") + 1: keyword.index(",")]
    keyword2 = keyword[keyword.index(",") + 2: keyword.index("]")]
    if "question" + str(i) not in resultDict: resultDict["question" + str(i)] = [keyword1, keyword2]
    i += 1
print(resultDict)