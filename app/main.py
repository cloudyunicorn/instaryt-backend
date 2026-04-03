from fastapi import FastAPI
from app.routes import post
from app.routes import webhook

app = FastAPI(title="Instagram Posting Service")

app.include_router(post.router)

app.include_router(webhook.router)

@app.get("/")
def root():
    return {"message": "Service is running 🚀"}