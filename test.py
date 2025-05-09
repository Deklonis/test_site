import sqlite3
import hashlib
from pydantic import BaseModel
conn = sqlite3.connect('jsdb.db')
print(conn.execute("SELECT email, password from peopledb WHERE email = ?", ('2',)).fetchall())