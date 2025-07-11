from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()

def get_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.on_event("startup")
def create_table():
    conn = get_connection()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)"
    )
    conn.commit()
    conn.close()

@app.get("/")
def root():
    return {"message": "Hello from FastAPI on Render!"}

@app.get("/users")
def get_users():
    conn = get_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return [dict(u) for u in users]

@app.post("/users")
def add_user(name: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return {"id": user_id, "name": name}
