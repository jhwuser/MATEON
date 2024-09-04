import openai
import config

client = openai.OpenAI(api_key=config.gptkey)
# hist = []

# while True:
#     msg = input()

#     hist.append({"role": "user", "content": msg})

#     completion = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=hist
#     )

#     print(completion.choices[0].message.content)

from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import pymysql
from datetime import datetime
import mate_ai

db = pymysql.connect(host="", database="", user="", password="", charset="utf8", use_unicode=True)
cur = db.cursor()

db.commit()

app = FastAPI()

class UserInfo(BaseModel):
    userid: str
    username: str | None = None
    email: str | None = None
    password: str | None = None

class RegisterInfo(BaseModel):
    userid: str
    username: str
    email: str
    password: str

class LoginInfo(BaseModel):
    userid: str
    password: str

class FriendInfo(BaseModel):
    userid: str
    name: str
    mbti: str

class ScheduleInfo(BaseModel):
    year: int
    month: int
    day: str
    userid: str
    h: int | None = None
    m: int | None = None
    name: str | None = None

class ChatInfo(BaseModel):
    userid: str
    name: str
    content: str

gpt = None
memory = {}

@app.post("/gptinit")
def gptinit(item: FriendInfo):
    global gpt
    global memory

    if memory.get(item.userid) == None:
        memory[item.userid] = {}

    if memory[item.userid].get(item.name) == None:
        memory[item.userid][item.name] = []

    gpt = mate_ai.friend(item.name, item.mbti.upper())

@app.post("/gptchat")
def gptchat(item: ChatInfo):
    global memory

    reply = gpt.fn_chat(item.content)

    print(reply)

    if reply.startswith("searchschedule"):
        print("search됏음")
        return PlainTextResponse(searchscheduleongpt(item.userid, reply.split("/")[1]))
    
    if reply.startswith("addschedule"):
        print("add도ㅒㅆ음")
        return PlainTextResponse(addscheduleongpt(item.userid, reply.split("/")[1], reply.split("/")[2]))

    memory[item.userid][item.name].append(item.content)
    print(memory)
    return PlainTextResponse(reply)

def searchscheduleongpt(userid, date):
    cur.execute("SET names utf8")
    cur.execute(f"SELECT * FROM MO_SCHEDULE WHERE DATE_FORMAT(start_date, '%Y-%m-%d') = '{date}' AND userid='{str.lower(userid)}'")

    fetch = cur.fetchall()

    schedulelist = []
    prompt = ""

    if fetch:
        for f in fetch:

            schedulelist.append((str(f[1].hour).zfill(2) ,str(f[1].minute).zfill(2), f[2]))

        for s in schedulelist:
            prompt += f"{s[0]}:{s[1]};{s[2]}/"

        return gpt.fn_chat(prompt)
    
    return gpt.fn_chat("noschedule")

def addscheduleongpt(userid, date, content):
    cur.execute("SET names utf8")
    cur.execute(f"SELECT userid FROM MO_SCHEDULE WHERE DATE_FORMAT(start_date, '%Y-%m-%d-%H%M') = '{date}' AND userid='{str.lower(userid)}' AND schedulename='{content}'")

    fetch = cur.fetchone()
    dt = datetime.strptime(date, '%Y-%m-%d-%H%M') #2024-01-31-1640

    if fetch:
        print("ss")
        return gpt.fn_chat("sameschedule")
    
    cur.execute(f"INSERT INTO MO_SCHEDULE VALUES('{str.lower(userid)}', '{dt}', '{content}')")

    return gpt.fn_chat(f"add/{date}/{content}/")

@app.post("/register")
def register(item: RegisterInfo):
    cur.execute("SET names utf8")
    cur.execute(f"SELECT EXISTS (SELECT * FROM MO_USER_INFO WHERE userid='{str.lower(item.userid)}')")
    if cur.fetchone()[0]:
        print("idA")
        return PlainTextResponse("idAlreadyExists")
    
    cur.execute(f"SELECT EXISTS (SELECT * FROM MO_USER_INFO WHERE email='{str.lower(item.email)}')")
    if cur.fetchone()[0]:
        print("emailA")
        return PlainTextResponse("emailAlreadyTaken")

    cur.execute(f"INSERT INTO MO_USER_INFO VALUES('{str.lower(item.userid)}', '{item.username}', '{str.lower(item.email)}', '{item.password}')")
    db.commit()

    return PlainTextResponse("successfullyRegistered")

@app.post("/login")
def register(item: LoginInfo):
    userid = str.lower(item.userid)

    cur.execute("SET names utf8")
    cur.execute(f"SELECT userid, password FROM MO_USER_INFO WHERE userid='{userid}'")

    fetch = cur.fetchone()

    if not fetch:
        print("idN")
        return PlainTextResponse("idDoesNotExist")
    
    if fetch[1] != item.password:
        print("pwN")
        return PlainTextResponse("passwordDoesNotMatch")
    
    return PlainTextResponse("successfullyLoggedIn")
    
@app.post("/showfriendlist")
def showfriendlist(item: UserInfo):
    cur.execute("SET names utf8")
    cur.execute(f"SELECT * FROM MO_FRIENDS WHERE userid='{str.lower(item.userid)}'")

    fetch = cur.fetchall()

    count = len(fetch)
    friendlist = []
    for f in fetch:
        friendlist.append((f[1], f[2]))

    return {"friends": friendlist, "count": count}

@app.post("/addfriend")
def addfriend(item: FriendInfo):
    cur.execute("SET names utf8")
    cur.execute(f"SELECT userid FROM MO_FRIENDS WHERE userid='{str.lower(item.userid)}' AND friendname='{str.lower(item.name)}'")

    fetch = cur.fetchone()

    print(fetch)

    if fetch:
        print("frnA")
        return PlainTextResponse("friendNameAlreadyUsed")
    
    cur.execute(f"INSERT INTO MO_FRIENDS VALUES('{str.lower(item.userid)}', '{item.name}', '{item.mbti}')")

@app.post("/removeallfriends")
def removeallfriend(item: UserInfo):
    cur.execute("SET names utf8")
    cur.execute(f"DELETE FROM MO_FRIENDS WHERE userid='{str.lower(item.userid)}'")

@app.post("/addschedule")
def addschedule(item: ScheduleInfo):
    cur.execute("SET names utf8")
    cur.execute(f"SELECT userid FROM MO_SCHEDULE WHERE userid='{str.lower(item.userid)}' AND schedulename='{item.name}'")

    fetch = cur.fetchone()
    print(f"{item.year}{str(item.month).zfill(2)}{str(item.day).zfill(2)}{str(item.h).zfill(2)}{str(item.m).zfill(2)}")
    dt = datetime.strptime(f"{item.year}{str(item.month).zfill(2)}{str(item.day).zfill(2)}{str(item.h).zfill(2)}{str(item.m).zfill(2)}",'%Y%m%d%H%M')

    if fetch:
        print("snA")
        return PlainTextResponse("scheduleNameAlreadyUsed")
    
    cur.execute(f"INSERT INTO MO_SCHEDULE VALUES('{str.lower(item.userid)}', '{dt}', '{item.name}')")

@app.post("/searchschedule")
def searchschedule(item: ScheduleInfo):
    cur.execute("SET names utf8")
    cur.execute(f"SELECT * FROM MO_SCHEDULE WHERE DATE_FORMAT(start_date, '%Y-%m-%d') = '{item.year}-{str(item.month).zfill(2)}-{item.day.zfill(2)}' AND userid='{str.lower(item.userid)}'")
    
    fetch = cur.fetchall()

    schedulelist = []

    if fetch:
        for f in fetch:

            schedulelist.append((str(f[1].hour).zfill(2) ,str(f[1].minute).zfill(2), f[2]))

        return {"list": schedulelist}
    
    return PlainTextResponse("scheduleDoesNotExist")