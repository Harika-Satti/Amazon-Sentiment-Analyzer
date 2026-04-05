import os
import json
import requests
from bs4 import BeautifulSoup
from groq import Groq
from dotenv import load_dotenv

# Setup environment
load_dotenv()

# Groq Setup
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


def get_amazon_reviews(url):
    """Scrape top reviews from an Amazon product URL."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;"
            "q=0.9,image/avif,image/webp,*/*;q=0.8"
        ),
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "lxml")

        # Primary selector for review bodies
        reviews = soup.find_all("span", {"data-hook": "review-body"})
        review_texts = [r.get_text(strip=True) for r in reviews[:8]]

        if not review_texts:
            # Fallback selectors for different Amazon layouts
            alt_reviews = soup.select(".review-text-content span, .review-text")
            review_texts = [r.get_text(strip=True) for r in alt_reviews[:8]]

        review_text = " ".join(review_texts).strip()

        # Get product title
        title_element = soup.find(id="productTitle")
        title = title_element.get_text(strip=True) if title_element else "Amazon Product"

        return {
            "text": review_text if review_text else None,
            "title": title,
        }
    except requests.exceptions.Timeout:
        return {"text": None, "title": "Unknown Product", "error": "Request timed out."}
    except requests.exceptions.HTTPError as e:
        return {"text": None, "title": "Unknown Product", "error": f"HTTP error: {e}"}
    except Exception as e:
        print(f"Scraping error: {e}")
        return {"text": None, "title": "Unknown Product", "error": str(e)}


def analyze_with_groq(text):
    """Call Groq Llama-3 to analyze the sentiment and return detailed results."""
    if not client:
        return {"error": "GROQ_API_KEY not configured. Please add it to your .env file."}

    # Truncate very long texts to stay within token limits
    max_chars = 4000
    if len(text) > max_chars:
        text = text[:max_chars] + "..."

    try:
        prompt = f"""
        Act as an expert Amazon Product Review Analyst. Analyze the following review text.
        Return ONLY a valid JSON object with the following structure (no extra keys, no markdown):
        {{
            "sentiment": "Positive" | "Negative" | "Neutral",
            "confidence": <float between 0.0 and 1.0>,
            "pros": ["pro1", "pro2", ...],
            "cons": ["con1", "con2", ...],
            "recommendation": "Buy Now" | "Avoid" | "Wait for Sale" | "Research Further",
            "explanation": "<Clear 1-2 sentence explanation>",
            "top_keywords": ["keyword1", "keyword2", ...]
        }}

        Review Text: "{text}"
        """

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a precise JSON-only output analyst. Never output markdown or prose.",
                },
                {"role": "user", "content": prompt},
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
            temperature=0.2,
        )

        raw = response.choices[0].message.content
        data = json.loads(raw)

        # Validate and sanitise required fields
        data.setdefault("sentiment", "Neutral")
        data.setdefault("confidence", 0.5)
        data.setdefault("pros", [])
        data.setdefault("cons", [])
        data.setdefault("recommendation", "Research Further")
        data.setdefault("explanation", "No explanation provided.")
        data.setdefault("top_keywords", [])

        # Clamp confidence to [0, 1]
        try:
            data["confidence"] = max(0.0, min(1.0, float(data["confidence"])))
        except (TypeError, ValueError):
            data["confidence"] = 0.5

        # Helper for progress-bar width (avoids inline style linting issues in templates)
        conf_val = int(data["confidence"] * 100)
        data["meter_style"] = f"width: {conf_val}%"
        data["confidence_pct"] = conf_val

        return data

    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON from AI model: {e}"}
    except Exception as e:
        return {"error": str(e)}