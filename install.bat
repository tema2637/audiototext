@echo off
echo Installing dependencies for Telegram Whisper Bot...
python -m pip install -r requirements.txt
if %ERRORLEVEL% == 0 (
    echo Dependencies installed successfully!
    echo.
    echo To run the bot:
    echo 1. Set your Telegram bot token as an environment variable:
    echo    set TELEGRAM_BOT_TOKEN=your_token_here
    echo 2. Run the bot:
    echo    python bot.py
) else (
    echo Failed to install dependencies
)
pause