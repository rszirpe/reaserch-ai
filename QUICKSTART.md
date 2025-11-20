# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies

```bash
cd "/Users/rishi/reserch ai"
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python app.py
```

The server will start on **http://localhost:8080**

### 3. Open in Browser

Navigate to: **http://localhost:8080**

## 📝 How to Use

1. Enter any question in the search box
2. Click "Research" 
3. Wait 10-30 seconds while the app:
   - Searches DuckDuckGo for relevant websites
   - Scrapes content from 5-8 sources
   - Generates a comprehensive answer using Gemini AI
4. Read the AI-generated answer and check sources

## 🔧 Troubleshooting

**Port Already in Use?**
- On macOS, port 5000 is used by AirPlay
- This app uses port 8080 instead
- If 8080 is busy, change the port in `app.py` line 170 and `static/script.js` line 2

**Rate Limit Error from Gemini?**
- Wait 30-60 seconds between requests
- This is a free API with rate limits

**No Search Results?**
- Check your internet connection
- Some websites may block scraping (app will continue with other sources)

## ✨ Features Working

- ✅ DuckDuckGo HTML search (no API key needed)
- ✅ Concurrent website scraping (up to 8 sites)
- ✅ Gemini 2.0 Flash AI integration [[memory:7241785]]
- ✅ Beautiful, responsive UI
- ✅ Real-time loading indicators
- ✅ Source citations with links

Enjoy researching! 🔍🤖

