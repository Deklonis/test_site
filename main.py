import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import hashlib

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все origins (для разработки)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class baza:
    def __init__(self):
        self.db = sqlite3.connect('jsdb.db', check_same_thread=False)
        self.cur = self.db.cursor()

d = baza()
db = d.db
cur = d.cur


class User(BaseModel):
    name: str
    surname: str
    email: str
    password: str

@app.post('/register/')
def user_register(user: User):
    t = cur.execute("SELECT email from peopledb WHERE email = ?", (user.email,))
    if len(t.fetchall()) != 0:
        raise HTTPException(status_code=400, detail="Такой email уже существует")
    hpass = hashlib.sha256(user.password.encode('utf-8')).hexdigest()
    cur.execute("INSERT INTO peopledb VALUES (?, ?, ?, ?)", (user.name, user.surname, user.email, hpass))
    db.commit()
    return {"message": "User registered successfully"}



class UserLogin(BaseModel):
    loginemail1: str
    loginpass1: str

@app.post('/login/')
def user_login(login: UserLogin):
    t = cur.execute("SELECT email, password from peopledb WHERE email = ?", (login.loginemail1,)).fetchall()
    if len(t) == 0:
        raise HTTPException(status_code=400, detail="Такого пользователя не существует. Создайте аккаунт")
    else:
        curpass = hashlib.sha256(login.loginpass1.encode('utf-8')).hexdigest()
        if t[0][1] == curpass:
            return {"message": "User login successfully"}
        else:
            raise HTTPException(status_code=400, detail="Неверный пароль или логин")