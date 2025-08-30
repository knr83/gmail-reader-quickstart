## Gmail Reader

A Python script that authenticates via OAuth 2.0, retrieves the latest Gmail messages (subject, from, date, id, snippet), and saves them to a JSON file (e.g., `emails.json`). The access token is cached locally in `token.json`.

### Features
- OAuth 2.0 authorization (token cached in `token.json`)
- Read-only scope: https://www.googleapis.com/auth/gmail.readonly
- Fetches the latest 5 messages (adjust in code if needed)

### Requirements
- Python 3.10+ (3.13 recommended)
- Dependencies from `requirements.txt`
- `credentials.json` (OAuth 2.0 client) in the project root

### Installation
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### Google Cloud Console setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project (or select an existing one).
3. Enable Gmail API: "APIs & Services" → "Library" → search "Gmail API" → "Enable".
4. Open "APIs & Services" → "Credentials".
5. Click "Create credentials" → "OAuth client ID".
6. If prompted, configure the OAuth consent screen (minimum: app name and email).
7. Choose application type: "Desktop application" (for local script).
8. Download the JSON and save it as `credentials.json`.
9. Place `credentials.json` in the project root (next to `main.py`).

### Run
```bash
python main.py
```
On the first run, a browser window will open for authorization. After successful authorization, a token will be saved to `token.json`.

### Output
The script saves the latest messages to `emails.json` in JSON format with fields: `subject`, `from`, `date`, `id`, `snippet`.
