from fastapi import FastAPI
from pydantic import BaseModel

from ml.model import load_model

model = None
app = FastAPI()


class SentimentResponse(BaseModel):
    text: str
    sentiment_label: str
    sentiment_score: float


# create a route
@app.get("/")
def index():
    return {"text": "Sentiment Analysis"}


@app.on_event("startup")
def startup_event():
    global model
    model = load_model()


@app.get("/predict")
def predict_sentiment(text: str):
    sentiment = model(text)

    response = SentimentResponse(
        text=text,
        sentiment_label=sentiment.label,
        sentiment_score=sentiment.score,
    )

    return response
