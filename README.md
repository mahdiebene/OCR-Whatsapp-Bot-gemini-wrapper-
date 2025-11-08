# WhatsApp AI Bot (Twilio + OpenAI Whisper)

A powerful WhatsApp bot that can process images and audio messages using AI, powered by Twilio and OpenAI Whisper.

## Features

- 🎤 **Audio Processing**: Converts voice messages to text using OpenAI Whisper
- 🖼️ **Image Analysis**: Analyzes images using GPT-4 Vision
- 💬 **AI Chat**: Intelligent conversations using GPT-4 with context memory
- 🔄 **Multi-format Support**: Handles various audio and image formats
- 📱 **Easy Setup**: Simple Twilio integration (no complicated Meta approval needed)

## Prerequisites

1. **Twilio Account** (Much easier than Meta WhatsApp API!)
   - Sign up at [Twilio](https://www.twilio.com/try-twilio)
   - Get your Account SID and Auth Token
   - Activate the Twilio Sandbox for WhatsApp (free for testing)

2. **OpenAI API Key**
   - Sign up at [OpenAI](https://platform.openai.com/)
   - Generate an API key

3. **Python 3.8+**

## Installation

1. Clone or download this project

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install FFmpeg (required for audio processing):
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - **Linux**: `sudo apt-get install ffmpeg`
   - **macOS**: `brew install ffmpeg`

4. Create `.env` file:
```powershell
copy .env.example .env
```

5. Edit `.env` and add your credentials:
```env
OPENAI_API_KEY=sk-your-key-here
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=whatsapp:+14155238886
PORT=5000
```

## Setup Twilio WhatsApp Sandbox

1. **Activate Twilio Sandbox** (for testing):
   - Go to [Twilio Console](https://console.twilio.com/)
   - Navigate to Messaging > Try it out > Send a WhatsApp message
   - Follow instructions to connect your WhatsApp to the sandbox

2. **Configure Webhook**:
   
   For local development, use ngrok:
   ```powershell
   ngrok http 5000
   ```
   
   Then in Twilio Console:
   - Go to Messaging > Settings > WhatsApp Sandbox Settings
   - Set "When a message comes in" to: `https://your-ngrok-url.ngrok.io/webhook`
   - Save configuration

3. **For Production** (optional):
   - Request WhatsApp Business API access from Twilio
   - Use your own phone number

## Usage

1. Start the bot:
```powershell
python whatsapp_bot.py
```

2. Send message to your Twilio WhatsApp number:
   - For sandbox, send the join code first (e.g., "join <your-code>")
   - Then interact with the bot!

## Example Interactions

### Text Message
```
You: "Hello"
Bot: "👋 Hello! I'm your AI WhatsApp assistant!

Send me:
📝 Text - Chat with me
🎤 Audio - I'll transcribe and respond
🖼️ Image - I'll analyze it

Type /reset to clear conversation history"
```

### Conversation
```
You: "What's 2+2?"
Bot: "2 + 2 equals 4."

You: "What about multiplying that by 3?"
Bot: "4 multiplied by 3 equals 12." (remembers context!)
```

### Image
```
You: [sends image] "What's in this picture?"
Bot: "🖼️ Image Analysis:
This image shows a sunset over the ocean with vibrant orange and pink hues..."
```

### Audio
```
You: [sends voice message: "Tell me a joke"]
Bot: "🎤 Transcription:
Tell me a joke

💬 AI Response:
Why don't scientists trust atoms? Because they make up everything! 😄"
```

### Commands
- `/start` or `hello` - Show welcome message
- `/reset` - Clear conversation history

## Project Structure

```
.
├── whatsapp_bot.py      # Main bot application
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .env                 # Your configuration (create this)
├── downloads/           # Temporary media storage
└── README.md           # This file
```

## API Costs

- **Twilio Sandbox**: FREE for testing
- **Twilio WhatsApp**: ~$0.005 per message (production)
- **OpenAI Whisper**: ~$0.006 per minute of audio
- **GPT-4 Vision**: ~$0.01-0.03 per image
- **GPT-4 Chat**: ~$0.03 per 1K tokens

## Troubleshooting

### FFmpeg Not Found
Make sure FFmpeg is installed and added to your system PATH:
```powershell
# Check if FFmpeg is installed
ffmpeg -version
```

### Webhook Not Receiving Messages
- Make sure ngrok is running: `ngrok http 5000`
- Check webhook URL in Twilio Console matches ngrok URL
- Verify your bot is running: `python whatsapp_bot.py`
- Check logs for errors

### Twilio Authentication Issues
- Double-check your Account SID and Auth Token
- Make sure there are no extra spaces in `.env` file
- Verify you've activated the WhatsApp sandbox

### Audio Format Issues
Some audio formats may need conversion. The bot handles this automatically with pydub and FFmpeg.

## Security Notes

- Never commit `.env` file to version control
- Use environment variables for all sensitive data
- Implement rate limiting for production use
- Validate and sanitize all inputs

## Advanced Features (TODO)

- [ ] Conversation context memory
- [ ] Multi-language support
- [ ] Video processing
- [ ] Document analysis (PDF, DOCX)
- [ ] Custom AI personas
- [ ] Message scheduling
- [ ] Analytics dashboard

## License

MIT License - Feel free to use and modify!

## Contributing

Pull requests are welcome. For major changes, please open an issue first.

## Support

For issues and questions:
- OpenAI: [platform.openai.com](https://platform.openai.com/)
- WhatsApp Business API: [developers.facebook.com](https://developers.facebook.com/docs/whatsapp)
