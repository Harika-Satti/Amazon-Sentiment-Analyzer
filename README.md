# 🛒 Amazon Sentiment & Review Analyzer (Pro)

![GitHub last commit](https://img.shields.io/github/last-commit/yourusername/amazon-sentiment-pro?style=flat-square)
![Core](https://img.shields.io/badge/Stack-Flask--FastAPI--Groq-6366f1?style=flat-square)
![UI](https://img.shields.io/badge/UI-Advanced--Modern--Dashboard-18181b?style=flat-square)

An advanced, professional-grade dashboard for extracting real-time insights from Amazon reviews. Powered by **Groq Llama-3-70B**, this application performs deep sentiment analysis, pros/cons extraction, and provides a professional buying recommendation.

---

## 🌟 Key Features

*   **⚡ Dual-Engine Architecture**: Support for both **Flask (SSR)** for quick browsing and **FastAPI** for high-performance API access.
*   **🌐 Live Amazon Scraper**: Built-in scraper fetches top reviews directly from any Amazon product URL with automatic fallback logic.
*   **🤖 Groq AI Engine**: Direct integration with Llama-3-70B for near-human level reasoning and sentiment detection.
*   **🛍️ Intelligence Hub**: Extracts specific "Pros" and "Cons" and provides a "Verdict" (Buy Now/Avoid/Wait/Research).
*   **🎨 Advanced UI**: Modern, premium dashboard using CSS-grid, glassmorphism, and a sleek sidebar navigation.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.10+, [Flask](https://flask.palletsprojects.com/) (SSR) & [FastAPI](https://fastapi.tiangolo.com/) (JSON API)
- **AI Core**: [Groq Cloud](https://groq.com/) (Llama-3-70B-Versatile)
- **Scraper**: [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) + Requests (LXML)
- **UI/UX**: HTML5, Modern CSS (Space Grotesk typography)

---

## 🚀 Installation & Local Setup

### 1. Prerequisites
Ensure you have Python 3.10+ installed and a **Groq API Key** from the [Groq Console](https://console.groq.com/).

### 2. Environment Configuration
Create a `.env` file in the root directory:
```bash
GROQ_API_KEY=your_actual_key_here
```

### 3. Choose your Engine

#### Option A: Run the Flask Web Dashboard
Ideal for humans browsing the analytics.
```bash
python app.py
```
Visit: **`http://127.0.0.1:5000`**

#### Option B: Run the FastAPI Backend
Ideal for developers or automated tools.
```bash
python main.py
```
Docs: **`http://127.0.0.1:8000/docs`**

---

## 📂 Project Roadmap

- [x] Initial Sentiment Logic (Streamlit)
- [x] High-Performance API (FastAPI)
- [x] Specialized Amazon AI Prompting
- [x] Live Product Scraping
- [x] Zero-JS SSR Migration
- [x] Dual-Core Implementation (Flask + FastAPI)
- [ ] Multiple Product Comparison
- [ ] Export Sentiment Reports as PDF

---

## 🤝 Contributing
Feel free to fork this project and submit pull requests for any features or bug fixes.

---

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.

---

### *Refined with ❤️ for professional open-source standards.*
