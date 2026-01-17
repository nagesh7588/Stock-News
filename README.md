# Stock/Share Market News Flask App

A Flask web app that fetches and filters stock/share market news from the last 24 hours using NewsAPI.org, with deployment support for Azure Web App.

## Features
- Fetches news from NewsAPI.org (free tier)
- Filters news by keywords: stock, stocks, share market, sensex, nifty, market, earnings, quarter results
- Displays title, date, source, description, and link
- Responsive UI with simple CSS
- Ready for Azure deployment (Gunicorn)

## Local Development

1. **Clone the repo** (if not already):
   ```powershell
   git clone <your-repo-url>
   cd "New folder"
   ```
2. **Create and activate a virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
4. **Set NewsAPI key:**
   - Get a free API key from [NewsAPI.org](https://newsapi.org/)
   - Set environment variable:
     ```powershell
     $env:NEWS_API_KEY="your_api_key_here"
     ```
5. **Run Flask app:**
   ```powershell
   flask run
   ```
   - Visit [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Azure Deployment (App Service)

### Option 1: VS Code Azure Extension
1. Install [Azure App Service extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azureappservice)
2. Sign in to Azure, create a Web App (Python 3.10+)
3. Deploy folder using extension
4. In Azure Portal, set `NEWS_API_KEY` in Application Settings
5. Set startup command:
   ```
   python -m gunicorn app:app --bind=0.0.0.0 --workers=4
   ```

### Option 2: GitHub Actions
1. Fork repo to GitHub
2. In Azure Portal, create Web App and configure GitHub Actions deployment
3. Add `NEWS_API_KEY` to Azure App Service Application Settings
4. Set startup command as above

## Notes
- Free NewsAPI.org tier may have request limits.
- For production, consider error handling and logging improvements.

---

**Replace all placeholder values (API key, repo URL) with your own.**
