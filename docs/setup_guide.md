# 🛠️ Game Claim Bot Setup Guide

## 📋 Prerequisites
- Python 3.11+ [Download](https://www.python.org/downloads/)
- Google Chrome installed
- Discord developer account [Create Bot](https://discord.com/developers/applications)
- Google Gemini API key [Get Key](https://aistudio.google.com)

## 🚀 Installation

1. **Clone Repository**
```bash
git clone https://github.com/yznx4/game-claim-bot.git
cd game-claim-bot
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Environment**
```bash
# Create environment file from template
cp .env.example .env
```

## 🔧 Configuration

1. **Edit `.env` File**
```env
DISCORD_BOT_TOKEN=your_discord_token_here
GEMINI_API_KEY=your_gemini_key_here
EPIC_EMAIL=your@epic.email
EPIC_PASSWORD=your_epic_password
STEAM_USER=steam_username
STEAM_PASSWORD=steam_password
```

2. **Chrome Profile Setup**  
Edit `src/steam.py` line 15:
```python
# Windows Example
options.add_argument(r"--user-data-dir=C:\Users\YOUR_USERNAME\AppData\Local\Google\Chrome\User Data")
```

3. **Install ChromeDriver**
```bash
pip install webdriver-manager
```

## ▶️ Running the Bot
```bash
python src/bot.py
```

## 🚨 Troubleshooting

**Common Issues**  
**Login Fails**:
- Delete cookie files (`*.pkl`) and retry
- Disable 2FA temporarily during setup
- Check credentials in `.env`

**ChromeDriver Errors**:
```bash
# Reinstall drivers
pip install --force-reinstall webdriver-manager
```

**Missing Dependencies**:
```bash
pip install -r requirements.txt --upgrade
```

## 🔒 Security Best Practices
1. Never commit:
   - `.env` files
   - `.pkl` cookie files
   - Chrome profile data
2. Use disposable accounts for bot operations
3. Enable 2FA after initial setup

## 🖥️ Command Cheat Sheet
```bash
# Start fresh (delete cookies)
rm *.pkl

# Update dependencies
pip freeze > requirements.txt

# Check bot status
python src/bot.py --test
```

> ⚠️ **Warning**: This bot requires access to your gaming accounts. Use at your own risk!

📜 [License](LICENSE) | 🐛 [Report Issues](https://github.com/yznx4/game-claim-bot/issues)
