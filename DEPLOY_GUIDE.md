# 🚀 Deploy WhatsApp Bot to Render.com (FREE)

## Step-by-Step Guide

### 1️⃣ Create GitHub Repository
```bash
# Initialize git (if not already done)
cd "f:\Agent Holder"
git init

# Add all files
git add .

# Commit
git commit -m "WhatsApp Bot with FREE AI - Ready for deployment"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 2️⃣ Deploy on Render.com

1. **Sign up**: Go to https://render.com and create FREE account

2. **Create Web Service**:
   - Click **"New +"** button
   - Select **"Web Service"**
   - Connect your GitHub account
   - Select your repository

3. **Configure Service**:
   ```
   Name: whatsapp-bot-free
   Region: Choose closest to you
   Branch: main
   Root Directory: (leave empty)
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn whatsapp_bot_free:app --bind 0.0.0.0:$PORT
   ```

4. **Select Plan**: 
   - Choose **"Free"** ($0/month)
   - ⚠️ Note: Sleeps after 15 min inactivity

### 3️⃣ Add Environment Variables

In Render dashboard, go to **"Environment"** tab and add:

```
GROQ_API_KEY = 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
GEMINI_API_KEY = AIzaSyDQAFqGLpA92gP1a7JH0ymOX5Rw8mLoFIE
TWILIO_ACCOUNT_SID = ACb13de664849583db7933403908612a46
TWILIO_AUTH_TOKEN = f7eb7a69c553b33c851d25a9a1add1eb
TWILIO_PHONE_NUMBER = whatsapp:+14155238886
```

### 4️⃣ Deploy!
- Click **"Create Web Service"**
- Wait 2-3 minutes for deployment
- Copy your Render URL (e.g., `https://whatsapp-bot-free.onrender.com`)

### 5️⃣ Update Twilio Webhook

1. Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
2. Scroll to **"Sandbox Configuration"**
3. Update **"When a message comes in"** to:
   ```
   https://YOUR-APP-NAME.onrender.com/webhook
   ```
4. Save!

### 6️⃣ Test Your Bot! 🎉

Send a message to: **+1 (415) 523-8886**

---

## ⚠️ Important Notes

- **Free Plan Limitations**:
  - Sleeps after 15 minutes of inactivity
  - Takes ~30 seconds to wake up on first request
  - 750 hours/month free (enough for most use)

- **Keep Bot Awake** (Optional):
  - Use a service like UptimeRobot (free) to ping your bot every 14 minutes
  - Or upgrade to Render Starter ($7/month) for always-on

## 🎯 Success!

Your bot is now:
- ✅ Running 24/7 online (with sleep)
- ✅ Completely FREE
- ✅ No local computer needed
- ✅ Auto-restarts on errors

---

## 🆘 Troubleshooting

**Bot not responding?**
1. Check Render logs for errors
2. Verify environment variables are set
3. Make sure Twilio webhook URL is correct
4. If sleeping, send a message and wait 30 seconds

**Still not working?**
- Check Render dashboard for deployment status
- Look at logs for error messages
- Verify all API keys are valid

---

Made with ❤️ - 100% FREE AI
