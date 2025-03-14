from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from econocast.interface.main import pred

app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def root():
    return { 'greeting': 'Hello EconoCast' }

@app.get("/predict/")
def predict(steps: int = 24):
    return pred(steps)
