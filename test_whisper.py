"""
Simple test script to verify Whisper functionality
"""
import whisper

# Load model
print("Loading Whisper model...")
model = whisper.load_model("base")  # Using base model for faster testing

# Test with a short audio (you can replace this with an actual audio file for full test)
print("Model loaded successfully!")
print("You can now run the Telegram bot using: python bot.py")
print("Remember to set your TELEGRAM_BOT_TOKEN environment variable first.")