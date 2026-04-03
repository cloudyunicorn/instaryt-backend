from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import post
from app.routes import webhook

app = FastAPI(title="Instagram Posting Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)

app.include_router(webhook.router)

@app.get("/")
def root():
    return {"message": "Service is running 🚀"}