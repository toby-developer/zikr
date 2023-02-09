from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from bs4 import BeautifulSoup
from datetime import datetime
import re
def mk_url(word,page):
    return quote( f'https://savollar.islom.uz/search?words={word.lower()}&page={page}', safe='/:=?&!')
def convert_to_datetime(dt_in_str):
    try:
        dt_in_str = dt_in_str.strip()
        time_part, date_part = dt_in_str.split(" / ")
        day, month = date_part.split(" ")
        month_mapping = {
            "январь": 1,
            "февраль": 2,
            "март": 3,
            "апрель": 4,
            "май": 5,
            "июнь": 6,
            "июль": 7,
            "август": 8,
            "сентябрь": 9,
            "октябрь": 10,
            "ноябрь": 11,
            "декабрь": 12,
        }
        month = month_mapping[month]
        datetime_string = f"{day} {month} {time_part}"
        dt = datetime.strptime(datetime_string, "%d %m %H:%M")
        return dt
    except ValueError as e:
        dt_in_str = dt_in_str.strip()
        time_part, date_part = dt_in_str.split(" / ")
        datetime_string = f"{date_part} {time_part}"
        dt = datetime.strptime(datetime_string, "%d.%m.%Y %H:%M")
        return dt
def to_dict_question(question):
    topic = question.find('span', {'class': 'time_question'}).get_text().split(
        "|")[-1].replace('\r\n', '').strip()
    author = question.find(
        'a', {'href': re.compile("^/muallif/")}).get_text().strip()
    author_url = 'https://savollar.islom.uz' + \
        question.find('a', {'href': re.compile(
            "^/muallif/")}).get('href').strip()
    title = question.find('a', {'href': re.compile(
        "^/s/[^oxshash]*$")}).get_text().strip()
    url = 'https://savollar.islom.uz' + \
        question.findAll('a', {'href': re.compile("^/s/")}
                         )[0].get('href').strip()
    short_text = question.find(
        "div", {"class": "text_question"}).get_text().replace('давоми...', '').replace('\r\n                          ', '').replace('Ассаламу алайкум!','').replace('Ассалому алайкум!','').replace('Валлоҳу аълам!','').strip()
    time = convert_to_datetime(question.find('span', {
        'class': 'time_question'}).get_text().split("|")[0].replace('\r\n', '').strip())
    return {"topic": topic, "title": title, "author": author, "author_url": author_url, "url": url, "short_text": short_text, "time": time}

def get_questions(url):
    try:
        html = urlopen(url)
        bsObj = BeautifulSoup(html.read(), "lxml")
        questions = [question for question in bsObj.findAll(
            'div', {'class': 'question'})]
        all_questions = [to_dict_question(question) for question in questions]
        if all_questions != []:
            return all_questions
        else:
            return ''
    except HTTPError as e:
        print(e)
        return None
    except URLError as e:
        print(e)
        return None
def get_question(url):
    html = urlopen(url)
    bsObj = BeautifulSoup(html.read(), "lxml")
    title= bsObj.find('h1').get_text().strip()
    time = convert_to_datetime(bsObj.find('div',{'class':'info_quesiton'}).get_text().split('|')[0].strip())
    author = bsObj.find('div',{'class':'info_quesiton'}).get_text().split('|')[1].strip()
    question= bsObj.find('div',{'class':'text_in_question'}).get_text().replace('Ассаламу алайкум!','').replace('Ассалому алайкум!','').strip()
    answer = bsObj.find('div',{'class':'answer_in_question'}).get_text().replace('– Ва алайкум ассалом!','').replace('Валлоҳу аълам!','').strip()
    return {'time':time,'author':author,'question':question,'answer':answer}