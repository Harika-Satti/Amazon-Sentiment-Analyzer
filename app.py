import os
from flask import Flask, render_template, request, flash
from core import get_amazon_reviews, analyze_with_groq

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "sent_analyzer_secret_88")


@app.route("/", methods=["GET", "POST"])
def index():
    analysis_result = None
    input_text = ""
    input_url = ""

    if request.method == "POST":
        input_url = request.form.get("url", "").strip()
        input_text = request.form.get("text", "").strip()

        target_text = ""
        product_title = "Product Analysis"

        if input_url:
            scraped_data = get_amazon_reviews(input_url)
            target_text = scraped_data.get("text") or ""
            product_title = scraped_data.get("title", product_title)

            # Surface scraping-specific errors to the user
            if scraped_data.get("error"):
                flash(f"Scraper notice: {scraped_data['error']}")

            if not target_text:
                flash(
                    "Could not extract reviews from that URL. "
                    "Amazon may have blocked the request — try pasting the review text manually."
                )
        else:
            target_text = input_text

        if not target_text:
            if request.method == "POST":
                flash("Please provide a URL or paste some review text to analyse.")
        else:
            analysis_result = analyze_with_groq(target_text)

            if "error" in analysis_result:
                flash(f"AI Engine Error: {analysis_result['error']}")
                analysis_result = None
            else:
                analysis_result["product_title"] = product_title

    return render_template(
        "index.html",
        result=analysis_result,
        input_text=input_text,
        input_url=input_url,
    )



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
