# 🛸 Quantum Research Terminal - AI Research Assistant

An alien spacecraft-themed web application that researches multiple websites using DuckDuckGo and generates clear, concise answers using Google's Gemini AI.

![Version](https://img.shields.io/badge/version-2.0-00fff9)
![Python](https://img.shields.io/badge/python-3.9+-0a1535)
![License](https://img.shields.io/badge/license-MIT-00fff9)

## ✨ Features

- 🔍 **Automated Web Research**: Searches DuckDuckGo for relevant information (no API key needed!)
- 📄 **Multi-Site Scraping**: Extracts content from multiple websites simultaneously
- 🤖 **AI-Powered Synthesis**: Uses Google Gemini 2.0 to generate clear, comprehensive answers
- 🛸 **Alien Spacecraft UI**: Futuristic interface with angular design and cyan glow aesthetic
- 📚 **Source Citations**: Shows all sources used with clickable links
- 🎨 **Static Starfield**: Beautiful background with 100 static stars
- ⚡ **Optimized Performance**: Smooth, lag-free experience

## 📸 Screenshots

### Main Interface
![Main Interface](screenshots/main-interface.png)
*Alien spacecraft control panel with search input and static starfield*

### Processing State
![Processing State](screenshots/processing.png)
*System processing with animated loading steps*

### Results Display
![Results Display](screenshots/results.png)
*AI-generated answer with source citations*

## 🎨 Design Philosophy

The interface is designed to look like an **alien spacecraft control panel**:
- ✅ Angular, geometric shapes (hexagonal cut corners)
- ✅ Deep blue space backgrounds
- ✅ Cyan/blue neon accents
- ✅ Tech grid overlays
- ✅ No animations (100% static for clarity)
- ✅ Sharp, futuristic aesthetic

## 📋 Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Internet connection

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/rszirpe/reaserch-ai.git
cd reaserch-ai
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

The Google Gemini API key is already configured in `app.py`. If you want to use your own:
1. Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Replace the API key in `app.py` line 18

## 🎮 Usage

### Start the Server

```bash
python app.py
```

The server will start on **http://localhost:8080**

### Access the Interface

Open your browser and navigate to: **http://localhost:8080**

### How to Use

1. Enter your research question in the search box
2. Click the **ENGAGE** button
3. Wait 10-30 seconds while the app:
   - Searches DuckDuckGo for relevant websites
   - Scrapes content from multiple sources
   - Generates a comprehensive answer using Gemini AI
4. Review the AI-generated answer and check the cited sources

## 📝 Example Queries

- "What are the latest developments in AI?"
- "How does quantum computing work?"
- "What is blockchain technology?"
- "Benefits of meditation"
- "Future of space exploration"

## 🛠️ Technology Stack

### Backend
- **Flask** - Web framework
- **BeautifulSoup4** - Web scraping
- **Requests** - HTTP library
- **DuckDuckGo HTML Search** - Free search (no API key needed)
- **Google Gemini 2.0 Flash** - AI text generation

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling (glassmorphism, angular design)
- **Vanilla JavaScript** - Interactivity
- **Canvas API** - Static starfield background

### Fonts
- **Orbitron** - Headers (futuristic sci-fi font)
- **Rajdhani** - Body text (clean tech font)

## 📁 Project Structure

```
reaserch-ai/
├── app.py              # Flask backend server
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── static/
│   ├── index.html     # Frontend interface
│   ├── style.css      # Alien spacecraft styling
│   └── script.js      # Frontend logic & starfield
└── venv/              # Virtual environment (not in repo)
```

## 🎨 UI Features

### Alien Spacecraft Design Elements
- **Angular Cards**: All panels have cut corners (clip-path polygons)
- **Cyan Glow**: Consistent #00fff9 color scheme throughout
- **Tech Borders**: 4px left borders on cards for emphasis
- **Grid Overlays**: Subtle tech grid patterns on background
- **Static Stars**: 100 non-moving stars for clean aesthetic
- **Glassmorphism**: Frosted glass effect with backdrop blur

### Color Palette
- **Primary Background**: `#0a1535` (Deep blue)
- **Starfield Gradient**: `#1a2f5c` → `#0a1535`
- **Accent Color**: `#00fff9` (Cyan)
- **Text**: `#ffffff` (White)
- **Glass Overlays**: `rgba(10, 21, 53, 0.9)`

## ⚙️ Configuration

### Change Port
If port 8080 is in use, modify `app.py` line 200:
```python
app.run(debug=True, port=YOUR_PORT)
```

Also update `static/script.js` line 2:
```javascript
const API_URL = 'http://localhost:YOUR_PORT';
```

### Adjust Search Results
Modify the number of websites scraped in `app.py` line 165:
```python
search_results = search_duckduckgo(query, max_results=8)  # Change 8 to your preferred number
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find and kill the process using port 8080
lsof -ti:8080 | xargs kill -9
```

### Module Not Found Errors
```bash
pip install -r requirements.txt
```

### Rate Limit from Gemini API
Wait 30-60 seconds between requests. The free tier has rate limits.

### Browser Shows Cached Version
- **Hard Refresh**: `Cmd/Ctrl + Shift + R`
- **Clear Cache**: Open DevTools → Network tab → Disable cache
- **Private Window**: Use incognito/private browsing

## 🔒 Security Notes

- The Gemini API key is included for demo purposes
- For production, use environment variables:
  ```python
  import os
  GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
  ```
- The app scrapes public websites responsibly with timeouts
- CORS is enabled for local development

## 📊 Performance

- **Stars**: 100 static particles (optimized for performance)
- **Search Results**: 8 websites scraped concurrently
- **Timeout**: 5 seconds per website
- **Response Time**: 10-30 seconds average
- **No Animations**: 100% static for zero lag

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Google Gemini AI** - For the AI text generation
- **DuckDuckGo** - For free, privacy-focused search
- **Flask Community** - For the excellent web framework
- **Google Fonts** - For Orbitron and Rajdhani fonts

## 📧 Contact

Created by Rishi - [@rszirpe](https://github.com/rszirpe)

---

**⚡ QUANTUM RESEARCH TERMINAL - OPERATIONAL ⚡**

*Navigate the web at the speed of thought* 🛸
