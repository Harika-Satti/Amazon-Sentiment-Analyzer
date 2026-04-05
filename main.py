import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from core import get_amazon_reviews, analyze_with_groq

app = FastAPI(
    title="Amazon Product Sentiment Analysis",
    version="2.0.0",
    description="Deep sentiment analysis for Amazon product reviews powered by Groq Llama-3.",
)

# CORS — restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalysisRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None  # plain str; HttpUrl validation too strict for Amazon URLs


class AnalysisResponse(BaseModel):
    sentiment: str
    confidence: float
    confidence_pct: int
    pros: List[str]
    cons: List[str]
    recommendation: str
    explanation: str
    top_keywords: Optional[List[str]] = []
    product_title: Optional[str] = "Product"


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "FastAPI is running."}


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_sentiment(payload: AnalysisRequest):
    if not payload.text and not payload.url:
        raise HTTPException(
            status_code=400, detail="Provide either 'text' or 'url' in the request body."
        )

    target_text = payload.text or ""
    product_title = "Product"

    if payload.url:
        scraped_data = get_amazon_reviews(payload.url)
        target_text = scraped_data.get("text") or ""
        product_title = scraped_data.get("title", product_title)

        if not target_text:
            raise HTTPException(
                status_code=422,
                detail=(
                    scraped_data.get("error")
                    or "Could not extract review content from the URL provided."
                ),
            )

    result = analyze_with_groq(target_text)

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    result["product_title"] = product_title
    # Remove template-only helper key before returning JSON
    result.pop("meter_style", None)
    return result


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)