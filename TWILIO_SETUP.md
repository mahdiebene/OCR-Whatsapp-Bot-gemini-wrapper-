# Twilio WhatsApp Setup Guide

## Quick Start (5 minutes!)

### 1. Create Twilio Account
1. Go to https://www.twilio.com/try-twilio
2. Sign up (free trial includes WhatsApp sandbox)
3. Verify your email and phone

### 2. Get Your Credentials

From [Twilio Console](https://console.twilio.com/):
- **Account SID**: Found on dashboard (starts with `AC...`)
- **Auth Token**: Click "Show" on dashboard

### 3. Activate WhatsApp Sandbox

1. In Twilio Console, go to: **Messaging → Try it out → Send a WhatsApp message**
2. You'll see instructions like:
   ```
   Send "join <your-code>" to +1 415 523 8886 on WhatsApp
   ```
3. Open WhatsApp and send that message
4. You'll get a confirmation: "You're all set!"

### 4. Configure Your Bot

1. Copy `.env.example` to `.env`:
   ```powershell
   copy .env.example .env
   ```

2. Edit `.env` with your credentials:
   ```env
   OPENAI_API_KEY=sk-proj-xxxxxxxx
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_PHONE_NUMBER=whatsapp:+14155238886
   PORT=5000
   ```

   **Note:** The sandbox phone number is usually `whatsapp:+14155238886`

### 5. Install Dependencies

```powershell
# Install Python packages
pip install -r requirements.txt

# Install FFmpeg (for audio processing)
# Download from: https://ffmpeg.org/download.html
# Add to PATH
```

### 6. Setup Webhook with ngrok

1. **Install ngrok** (if not installed):
   - Download from https://ngrok.com/download
   - Or use: `choco install ngrok` (if you have Chocolatey)

2. **Start ngrok**:
   ```powershell
   ngrok http 5000
   ```
   
   You'll see output like:
   ```
   Forwarding    https://abc123.ngrok.io -> http://localhost:5000
   ```

3. **Configure Twilio Webhook**:
   - Go to [Twilio Console → Messaging → Settings → WhatsApp Sandbox Settings](https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox)
   - In "When a message comes in" field, enter:
     ```
     https://abc123.ngrok.io/webhook
     ```
   - Set HTTP method to: `POST`
   - Click **Save**

### 7. Run Your Bot

```powershell
python whatsapp_bot.py
```

You should see:
```
INFO:__main__:WhatsApp Bot initialized with Twilio
INFO:__main__:Bot initialized successfully!
INFO:__main__:Starting server on port 5000
```

### 8. Test It!

Open WhatsApp and send to `+1 415 523 8886`:

1. **Text**: "Hello"
2. **Voice Note**: Record and send
3. **Image**: Send any image

## Troubleshooting

### "No module named 'twilio'"
```powershell
pip install twilio
```

### "FFmpeg not found"
Download FFmpeg and add to system PATH:
1. Download: https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to PATH
4. Restart PowerShell

### Webhook not receiving messages
1. Check ngrok is running: Look for "Forwarding" URL
2. Verify webhook URL in Twilio matches ngrok URL
3. Make sure bot is running: `python whatsapp_bot.py`
4. Check Twilio logs: https://console.twilio.com/us1/monitor/logs/errors

### Authentication failed
1. Verify Account SID and Auth Token in `.env`
2. No extra spaces or quotes
3. Check you copied the full token (click "Show" in console)

## Twilio Sandbox Limitations

- **Free** for testing
- **Resets after 3 days** of inactivity (need to rejoin)
- **Limited to** your registered phone numbers
- **24-hour window** per conversation

## Production Setup (Optional)

For production with your own number:

1. **Apply for WhatsApp Business API** in Twilio Console
2. **Verify your business**
3. **Get approved** (takes 1-3 days)
4. **Update** `TWILIO_PHONE_NUMBER` in `.env`

Costs: ~$0.005 per message

## OpenAI API Setup

1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy and save (you won't see it again!)
4. Add to `.env` as `OPENAI_API_KEY`

**Pricing:**
- Whisper (audio): $0.006/minute
- GPT-4 Vision (images): $0.01-0.03/image
- GPT-4 Chat: $0.03/1K tokens

## Testing Without WhatsApp

Run the test script:
```powershell
python test_bot.py
```

This tests AI chat without needing Twilio setup.

## Next Steps

- Add database for persistent conversation history
- Implement user authentication
- Add more AI features (document analysis, etc.)
- Deploy to cloud (Heroku, Railway, Azure, etc.)

## Support

- **Twilio Docs**: https://www.twilio.com/docs/whatsapp
- **OpenAI Docs**: https://platform.openai.com/docs
- **This Bot's README**: See `README.md`
