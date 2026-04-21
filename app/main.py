# app/main.py
from fastapi import FastAPI

# App ka instance banaya
app = FastAPI(title="SwiftCommerce API")

@app.get("/")
def read_root():
    return {"message": "Welcome to SwiftCommerce API - Speed and Scale!"}

