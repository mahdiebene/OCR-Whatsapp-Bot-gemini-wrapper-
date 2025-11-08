# 🎯 Quick Start - Deploy Your WhatsApp Bot

## ✅ Files Ready for Deployment:
- ✅ `whatsapp_bot_free.py` - Main bot code
- ✅ `requirements.txt` - Dependencies
- ✅ `Procfile` - Render configuration
- ✅ `runtime.txt` - Python version
- ✅ `.gitignore` - Git ignore rules

## 🚀 Deploy in 3 Steps:

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "WhatsApp Bot - FREE AI"
```
Then create a repo on GitHub and push:
```bash
git remote add origin YOUR_GITHUB_URL
git push -u origin main
```

### Step 2: Deploy on Render
1. Go to https://render.com (sign up FREE)
2. Click **New +** → **Web Service**
3. Connect GitHub repo
4. Settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn whatsapp_bot_free:app`
   - **Plan**: FREE

### Step 3: Add Environment Variables
In Render, add these variables:
```
GROQ_API_KEY = your_groq_api_key_here
GEMINI_API_KEY = your_gemini_api_key_here
TWILIO_ACCOUNT_SID = your_twilio_account_sid
TWILIO_AUTH_TOKEN = your_twilio_auth_token
TWILIO_PHONE_NUMBER = whatsapp:+14155238886
```

### Step 4: Update Twilio
Copy your Render URL and update Twilio webhook to:
`https://YOUR-APP.onrender.com/webhook`

## ✅ DONE! 
Your bot is now online 24/7! 🎉

---

**Need help?** Check `DEPLOY_GUIDE.md` for detailed instructions.
