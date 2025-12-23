#!/usr/bin/env python3
"""
Launcher script for Telegram Whisper Bot
"""

import os
import sys
import subprocess
import logging

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_ffmpeg():
    """Check if ffmpeg is installed"""
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL, 
                      check=True)
        logger.info("FFMPEG is installed and available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("FFMPEG is not installed or not available in PATH")
        logger.error("Please install FFMPEG from https://ffmpeg.org/download.html")
        return False

def check_token():
    """Check if Telegram bot token is set"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable is not set")
        logger.error("Please set it using: export TELEGRAM_BOT_TOKEN=your_token_here")
        return False
    return True

def main():
    logger.info("Starting Telegram Whisper Bot...")
    
    # Check dependencies
    if not check_ffmpeg():
        sys.exit(1)
    
    if not check_token():
        sys.exit(1)
    
    # Install requirements if not already installed
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, stdout=subprocess.DEVNULL)
        logger.info("Dependencies installed successfully")
    except subprocess.CalledProcessError:
        logger.error("Failed to install dependencies")
        sys.exit(1)
    
    # Run the bot
    try:
        from bot import main as bot_main
        logger.info("Starting bot...")
        bot_main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()