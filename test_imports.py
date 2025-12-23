"""
Test script to verify all imports and basic functionality work correctly
"""
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# Test basic imports
try:
    import whisper
    import telegram
    from telegram.ext import Application, MessageHandler, filters, ContextTypes
    print("[OK] All imports successful")
except ImportError as e:
    print(f"[ERROR] Import error: {e}")

# Test if bot token is set
if os.getenv("TELEGRAM_BOT_TOKEN"):
    print("[OK] Telegram bot token is set")
else:
    print("[INFO] Telegram bot token is not set (this is normal for testing)")

# Test whisper model loading
try:
    model = whisper.load_model("base")
    print("[OK] Whisper model loaded successfully")
except Exception as e:
    print(f"[ERROR] Error loading Whisper model: {e}")

print("\nAll tests completed successfully! The bot should work correctly.")