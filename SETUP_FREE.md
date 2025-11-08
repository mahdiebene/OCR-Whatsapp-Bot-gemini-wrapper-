# 🆓 FREE WhatsApp AI Bot Setup

## No OpenAI, No Payments Needed! 100% FREE!

This version uses:
- **Groq** - FREE Llama 3 & Whisper (faster than OpenAI!)
- **Twilio** - FREE sandbox for testing
- **No credit card** needed for Groq!

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Get FREE Groq API Key

1. Go to: **https://console.groq.com**
2. Click "Sign Up" (use Google/GitHub - instant!)
3. After login, click "API Keys" in sidebar
4. Click "Create API Key"
5. **Copy the key** (starts with `gsk_...`)

✅ **No credit card needed!**
✅ **Very generous free tier!**
✅ **Faster than OpenAI!**

---

### Step 2: Install Dependencies

```powershell
cd "f:\Agent Holder"
pip install -r requirements_free.txt
```

---

### Step 3: Configure

1. Copy the free config:
```powershell
copy .env.free .env
```

2. Edit `.env`:
```powershell
notepad .env
```

3. Add your Groq key:
```env
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=whatsapp:+14155238886
PORT=5000
```

4. Save (Ctrl+S)

---

### Step 4: Run the FREE Bot

```powershell
python whatsapp_bot_free.py
```

---

## ✨ What's FREE:

- ✅ **Text Chat** - Powered by Llama 3.3 70B (FREE!)
- ✅ **Voice Transcription** - Whisper Large V3 (FREE!)
- ✅ **Fast** - Groq is FASTER than OpenAI!
- ✅ **No Limits** - Generous free tier

---

## 🎯 Features:

| Feature | Free Version | Paid (OpenAI) |
|---------|--------------|---------------|
| Text Chat | ✅ Llama 3 | ✅ GPT-4 |
| Voice Notes | ✅ Whisper | ✅ Whisper |
| Images | 📝 Basic info | ✅ Full analysis |
| Cost | 🆓 FREE | 💰 ~$0.03/1K tokens |
| Speed | ⚡ Very Fast | 🐌 Slower |

---

## 📊 Groq Free Tier:

- **30 requests per minute**
- **Unlimited** daily usage
- **No expiration**
- **No credit card** required

Perfect for personal use!

---

## 🔄 Switching Between Versions:

**Use FREE version:**
```powershell
python whatsapp_bot_free.py
```

**Use OpenAI version:**
```powershell
python whatsapp_bot.py
```

---

## 🆘 Troubleshooting:

### "Module 'groq' not found"
```powershell
pip install groq
```

### "Invalid API key"
- Make sure you copied the full key from Groq console
- Key should start with `gsk_`
- No extra spaces in .env file

---

## 🎉 You're Done!

Your bot now runs 100% FREE with:
- Llama 3.3 for chat
- Whisper for voice
- No OpenAI costs!

**Test it now!** Send "Hello" to your WhatsApp bot! 🚀
