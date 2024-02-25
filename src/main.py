from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

from . import models
from .db import engine
from .routers import posts, users, auth

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

try:
    conn = psycopg2.connect(host='localhost',
                           database='fastapi', 
                           user='postgres', 
                           password='1234', 
                           cursor_factory=RealDictCursor)
    
    cursor = conn.cursor()
    print('Connected to the database')

except Exception as e:
    print('Error: ', e)

@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(users.router)
