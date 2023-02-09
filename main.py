from functions import convert_to_datetime, to_dict_question,get_questions,mk_url,get_question
from urllib.parse import quote
questions=get_questions(mk_url("asr namoz", 1))
print(get_question(questions[0]['url'])['question'])
print(get_question(questions[0]['url'])['answer'])