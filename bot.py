import os
import tempfile
import logging
import subprocess
from pathlib import Path

from dotenv import load_dotenv
import whisper
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

from config import WHISPER_MODEL, AUDIO_SAMPLE_RATE, AUDIO_CHANNELS, MAX_MESSAGE_LENGTH

# Load environment variables from .env file
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load Whisper model
logger.info(f"Loading Whisper model ({WHISPER_MODEL})...")
model = whisper.load_model(WHISPER_MODEL)
logger.info("Whisper model loaded successfully!")


async def transcribe_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle audio messages and transcribe them using Whisper
    """
    user = update.effective_user
    message = update.message
    
    logger.info(f"Received audio message from {user.first_name} ({user.id})")
    
    # Inform user that processing has started
    await message.reply_text("Начинаю расшифровку аудио... Это может занять несколько минут.")
    
    try:
        # Get the file from Telegram
        file = await context.bot.get_file(message.voice.file_id if message.voice else message.audio.file_id)
        
        # Create a temporary file to store the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.ogg' if message.voice else '.mp3') as temp_audio:
            await file.download_to_memory(temp_audio)
            temp_audio_path = temp_audio.name
        
        # Convert audio to WAV format if needed (Whisper works best with WAV)
        import subprocess
        wav_path = temp_audio_path.replace('.ogg', '.wav').replace('.mp3', '.wav')
        
        # Use ffmpeg to convert to WAV format
        subprocess.run([
            'ffmpeg', '-i', temp_audio_path,
            '-ar', str(AUDIO_SAMPLE_RATE),  # Set sample rate
            '-ac', str(AUDIO_CHANNELS),     # Set number of channels
            '-c:a', 'pcm_s16le',            # Use PCM codec
            wav_path
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Transcribe the audio using Whisper
        logger.info(f"Starting transcription for {user.first_name}")
        result = model.transcribe(wav_path)
        
        # Extract the transcribed text
        transcribed_text = result['text'].strip()
        
        if transcribed_text:
            # Split the text into chunks according to Telegram message limits
            if len(transcribed_text) <= MAX_MESSAGE_LENGTH:
                await message.reply_text(f"Расшифровка:\n\n{transcribed_text}")
            else:
                # Split into chunks and send them one by one
                chunks = []
                current_chunk = ""

                for sentence in transcribed_text.split('. '):
                    if len(current_chunk + sentence + '. ') <= MAX_MESSAGE_LENGTH:
                        current_chunk += sentence + '. '
                    else:
                        chunks.append(current_chunk.strip())
                        current_chunk = sentence + '. '

                if current_chunk:
                    chunks.append(current_chunk.strip())

                for i, chunk in enumerate(chunks, 1):
                    await message.reply_text(f"Часть {i}/{len(chunks)}:\n\n{chunk}")
        else:
            await message.reply_text("Не удалось расшифровать аудио. Возможно, в нем нет речи.")
            
    except Exception as e:
        logger.error(f"Error processing audio: {e}")
        await message.reply_text(f"Произошла ошибка при расшифровке аудио: {str(e)}")
    finally:
        # Clean up temporary files
        try:
            if 'temp_audio_path' in locals():
                os.remove(temp_audio_path)
            if 'wav_path' in locals() and os.path.exists(wav_path):
                os.remove(wav_path)
        except Exception as cleanup_error:
            logger.error(f"Error cleaning up temporary files: {cleanup_error}")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        print("Please set the TELEGRAM_BOT_TOKEN environment variable.")
        return
    
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    # Handle both voice messages and audio files
    application.add_handler(MessageHandler(filters.VOICE & ~filters.COMMAND, transcribe_audio))
    application.add_handler(MessageHandler(filters.AUDIO & ~filters.COMMAND, transcribe_audio))

    # Start the Bot
    application.run_polling()


if __name__ == '__main__':
    main()