# How to Get a Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Start a chat with BotFather and use the `/newbot` command
3. Follow the instructions to create your bot:
   - Choose a name for your bot (e.g., "Lecture Transcriber Bot")
   - Choose a username for your bot (must end with "bot", e.g., "lecture_transcriber_bot")
4. After creating the bot, BotFather will provide you with an API token
5. Copy this token as you'll need it to run the bot

Example token format: `1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ`

# Creating the .env File

1. Create a file named `.env` in the root directory of the project
2. Add your token to the file in this format:
   ```
   TELEGRAM_BOT_TOKEN=your_token_here
   ```

Example `.env` file:
```
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ
```

# Running the Bot

After creating your `.env` file, run the bot using:
```
python bot.py
```

Or use the run script:
```
python run_bot.py
```