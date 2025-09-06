# app/main.py

"""
File: app/main.py
FastAPI entrypoint for IMA Service with detailed OpenAPI documentation.
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello World!"}
