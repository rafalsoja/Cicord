# Cicord
![Static Badge](https://img.shields.io/badge/noob-coding-blue)
![Build](https://github.com/Cichaj/Cicord/actions/workflows/python-app.yml/badge.svg)


A simple Discord bot built with [discord.py](https://github.com/Rapptz/discord.py).

## Features

- 💬 AI-powered conversation: The bot can chat with users using AI-generated responses.
- 🎵 Music player (WIP): Streams audio from YouTube and other sources using `yt-dlp`. 
- ⏱️ Simple commands, easy setup.

## Getting Started

### Prerequisites

- TODO

## Installation

Follow these steps to set up the bot on your local machine:

1. **Clone the repository:**
   ```sh
   git clone https://github.com/Cichaj/Cicord.git
   cd Cicord
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Configure your environment** (choose one):
   - Create `.env` file:
     ```ini
     DISCORD_TOKEN=your-token
     OPENAI_API_KEY=your-key  # optional
     ```
   - **OR** edit directly in `config.py`:
     ```python
     TOKEN = "your-token"
     OPENAI_KEY = "your-key"  # optional
     ```

4. **Run the bot:**
   ```sh
   python bot.py
   ```

## Setting up verify cog:
1. **Choose a channel and enter this command:**
   ``` 
   !setupverify @rule password question
   ```
