"""
WhatsApp Bot with Audio and Image Processing - FREE VERSION
Uses Twilio for WhatsApp and FREE AI models (Groq + HuggingFace)
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict
import asyncio
import base64
import io

# Twilio for WhatsApp
from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import requests

# Free AI alternatives
import groq  # Free LLM API
import google.generativeai as genai  # Google Gemini for images
from PIL import Image

# Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
UPLOAD_FOLDER = 'downloads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'ogg', 'opus', 'mpeg', 'amr'}

class WhatsAppBotFree:
    def __init__(self, groq_api_key: str, gemini_api_key: str, twilio_account_sid: str, twilio_auth_token: str, twilio_phone_number: str):
        """
        Initialize WhatsApp Bot with FREE AI alternatives
        
        Args:
            groq_api_key: Groq API key (free from groq.com)
            gemini_api_key: Google Gemini API key (free from aistudio.google.com)
            twilio_account_sid: Twilio Account SID
            twilio_auth_token: Twilio Auth Token
            twilio_phone_number: Twilio WhatsApp number
        """
        self.groq_client = groq.Groq(api_key=groq_api_key)
        
        # Initialize Gemini for image analysis
        genai.configure(api_key=gemini_api_key)
        self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
        
        self.twilio_client = Client(twilio_account_sid, twilio_auth_token)
        self.twilio_phone_number = twilio_phone_number
        
        # Create upload folder if it doesn't exist
        Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
        
        # Store conversation context (simple in-memory storage)
        self.conversation_contexts: Dict[str, list] = {}
        
        logger.info("WhatsApp Bot initialized with FREE AI models (Groq + Gemini)")
    
    def send_message(self, to: str, message: str) -> dict:
        """Send a text message via Twilio WhatsApp (splits if too long)"""
        try:
            # WhatsApp has 1600 character limit - split if needed
            MAX_LENGTH = 1600
            
            if len(message) <= MAX_LENGTH:
                # Send single message
                msg = self.twilio_client.messages.create(
                    from_=self.twilio_phone_number,
                    body=message,
                    to=to
                )
                logger.info(f"Message sent: {msg.sid}")
                return {"status": "sent", "sid": msg.sid}
            else:
                # Split into multiple messages
                parts = []
                while len(message) > 0:
                    if len(message) <= MAX_LENGTH:
                        parts.append(message)
                        break
                    else:
                        # Find last space before limit to avoid cutting words
                        split_at = message.rfind(' ', 0, MAX_LENGTH)
                        if split_at == -1:
                            split_at = MAX_LENGTH
                        parts.append(message[:split_at])
                        message = message[split_at:].strip()
                
                # Send all parts
                sids = []
                for i, part in enumerate(parts):
                    prefix = f"[Part {i+1}/{len(parts)}]\n" if len(parts) > 1 else ""
                    msg = self.twilio_client.messages.create(
                        from_=self.twilio_phone_number,
                        body=prefix + part,
                        to=to
                    )
                    sids.append(msg.sid)
                    logger.info(f"Message part {i+1}/{len(parts)} sent: {msg.sid}")
                
                return {"status": "sent", "sids": sids, "parts": len(parts)}
                
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return {"status": "error", "error": str(e)}
    
    def download_media(self, media_url: str) -> Optional[bytes]:
        """Download media from Twilio"""
        try:
            response = requests.get(
                media_url,
                auth=(self.twilio_client.username, self.twilio_client.password)
            )
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.error(f"Error downloading media: {e}")
            return None
    
    def process_audio_free(self, audio_data: bytes, audio_format: str = 'ogg') -> str:
        """
        Convert audio to text using Groq's Whisper (FREE!)
        
        Args:
            audio_data: Raw audio bytes
            audio_format: Audio format (ogg, mp3, wav, etc.)
        
        Returns:
            Transcribed text
        """
        try:
            # Save audio temporarily - Groq supports ogg, mp3, wav, m4a, flac directly
            temp_audio_path = f"{UPLOAD_FOLDER}/temp_audio.{audio_format}"
            with open(temp_audio_path, 'wb') as f:
                f.write(audio_data)
            
            # Use Groq's Whisper for transcription (FREE!)
            # Groq Whisper supports: flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, webm
            with open(temp_audio_path, 'rb') as audio_file:
                transcription = self.groq_client.audio.transcriptions.create(
                    file=(f"audio.{audio_format}", audio_file, f"audio/{audio_format}"),
                    model="whisper-large-v3",  # Free on Groq!
                    response_format="text"
                )
            
            # Clean up
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
            
            return transcription
        
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            return f"Error transcribing audio: {str(e)}"
    
    def process_image_free(self, image_data: bytes, user_query: str = "What's in this image?") -> str:
        """
        Analyze image using HuggingFace's FREE BLIP model (online, no local install)
        
        Args:
            image_data: Raw image bytes
            user_query: Question about the image
        
        Returns:
            Description of the image
        """
        try:
            # Get basic image info
            image = Image.open(io.BytesIO(image_data))
            width, height = image.size
            mode = image.mode
            format_name = image.format or "Unknown"
            
            # Use Google Gemini 2.5 Flash for image analysis (FREE!)
            try:
                # Create a focused prompt for concise output
                focused_prompt = (
                    "Extract ALL text from this image in a clear format. "
                    "Then provide ONE brief sentence describing what type of document/image this is. "
                    "Be concise and direct. No extra explanations."
                )
                
                # Gemini can work directly with PIL Image
                response = self.gemini_model.generate_content([focused_prompt, image])
                
                analysis = response.text
                
                return f"📄 *Text & Info:*\n\n{analysis}"
                    
            except Exception as vision_error:
                logger.warning(f"Image analysis error: {vision_error}")
                
                # Fallback: Basic info + error message
                return (
                    f"📸 *Image Received!*\n\n"
                    f"📏 Size: {width} x {height}\n"
                    f"📦 Format: {format_name}\n\n"
                    f"⚠️ Image analysis temporarily unavailable.\n"
                    f"Please try again in a moment."
                )
        
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            return f"Error analyzing image: {str(e)}"
    
    def chat_with_ai_free(self, message: str, user_number: str = None, context: list = None) -> str:
        """
        Chat using FREE Groq API (Llama 3 or Mixtral)
        
        Args:
            message: User message
            user_number: User's phone number for context tracking
            context: Previous conversation context
        
        Returns:
            AI response
        """
        try:
            # Get or create conversation context
            if context is None and user_number:
                context = self.conversation_contexts.get(user_number, [])
            elif context is None:
                context = []
            
            # Add system message if context is empty
            if not context:
                context = [{
                    "role": "system",
                    "content": "You are a professional AI assistant. Provide direct, concise answers focused on the task at hand. No unnecessary information about what models you use or being free. Just do the work."
                }]
            
            # Add user message
            messages = context + [{"role": "user", "content": message}]
            
            # Use Groq's FREE API with Llama 3
            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Free and fast!
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Update conversation context (keep last 10 messages)
            if user_number:
                new_context = messages + [{"role": "assistant", "content": ai_response}]
                self.conversation_contexts[user_number] = new_context[-10:]
            
            return ai_response
        
        except Exception as e:
            logger.error(f"Error in AI chat: {e}")
            return f"Error communicating with AI: {str(e)}"
    
    def handle_message(self, from_number: str, body: str = None, media_url: str = None, 
                       media_content_type: str = None, num_media: int = 0) -> str:
        """Handle incoming WhatsApp message from Twilio"""
        try:
            logger.info(f"Received message from {from_number}")
            
            # Handle text messages
            if body and num_media == 0:
                # Check for commands
                if body.lower() in ['/start', 'start', 'hello', 'hi']:
                    response = ("👋 Hello! I'm your AI assistant.\n\n"
                               "I can help you with:\n"
                               "📝 Text - Chat and answer questions\n"
                               "🎤 Audio - Transcribe voice messages\n"
                               "🖼️ Image - Extract text and analyze content\n\n"
                               "Type /reset to clear conversation history")
                    self.send_message(from_number, response)
                    return response
                
                elif body.lower() in ['/reset', 'reset']:
                    self.conversation_contexts[from_number] = []
                    response = "✅ Conversation history cleared!"
                    self.send_message(from_number, response)
                    return response
                
                else:
                    response = self.chat_with_ai_free(body, from_number)
                    self.send_message(from_number, response)
                    return response
            
            # Handle media messages
            elif num_media > 0 and media_url:
                # Download media
                media_data = self.download_media(media_url)
                
                if not media_data:
                    response = "❌ Sorry, couldn't download the media."
                    self.send_message(from_number, response)
                    return response
                
                # Handle audio
                if media_content_type and 'audio' in media_content_type:
                    audio_format = media_content_type.split('/')[-1]
                    if audio_format == 'mpeg':
                        audio_format = 'mp3'
                    
                    transcription = self.process_audio_free(media_data, audio_format)
                    
                    response = f"🎤 *Transcription:*\n{transcription}\n\n💬 *AI Response:*\n"
                    ai_response = self.chat_with_ai_free(transcription, from_number)
                    full_response = response + ai_response
                    
                    self.send_message(from_number, full_response)
                    return full_response
                
                # Handle images
                elif media_content_type and 'image' in media_content_type:
                    query = body if body else "What's in this image?"
                    description = self.process_image_free(media_data, query)
                    
                    self.send_message(from_number, description)
                    return description
                
                else:
                    response = f"❌ Unsupported media type: {media_content_type}"
                    self.send_message(from_number, response)
                    return response
            
            else:
                response = "❌ No message content received"
                self.send_message(from_number, response)
                return response
        
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            error_response = "❌ Sorry, an error occurred while processing your message."
            self.send_message(from_number, error_response)
            return error_response


# Flask app for Twilio webhook
app = Flask(__name__)
bot = None

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming WhatsApp messages from Twilio"""
    try:
        # Get message data from Twilio
        from_number = request.form.get('From')
        body = request.form.get('Body')
        num_media = int(request.form.get('NumMedia', 0))
        
        # Get media if present
        media_url = None
        media_content_type = None
        if num_media > 0:
            media_url = request.form.get('MediaUrl0')
            media_content_type = request.form.get('MediaContentType0')
        
        logger.info(f"Webhook received from {from_number}: {body} (Media: {num_media})")
        
        # Process message
        bot.handle_message(
            from_number=from_number,
            body=body,
            media_url=media_url,
            media_content_type=media_content_type,
            num_media=num_media
        )
        
        # Return empty response
        resp = MessagingResponse()
        return str(resp), 200
    
    except Exception as e:
        logger.error(f"Webhook error: {e}", exc_info=True)
        resp = MessagingResponse()
        resp.message(f"❌ Error: {str(e)[:100]}")  # Show first 100 chars of error
        return str(resp), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "whatsapp-bot-free"}, 200

@app.route('/', methods=['GET'])
def home():
    """Homepage with status"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>WhatsApp AI Bot</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 40px;
                max-width: 600px;
                width: 100%;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 {
                color: #333;
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            .status {
                display: inline-block;
                background: #10b981;
                color: white;
                padding: 8px 20px;
                border-radius: 20px;
                font-weight: 600;
                margin-bottom: 30px;
            }
            .status::before {
                content: "●";
                margin-right: 8px;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            .info {
                background: #f3f4f6;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
            }
            .info h2 {
                color: #667eea;
                font-size: 1.2em;
                margin-bottom: 15px;
            }
            .feature {
                display: flex;
                align-items: center;
                margin: 10px 0;
                color: #555;
            }
            .feature::before {
                content: "✓";
                color: #10b981;
                font-weight: bold;
                margin-right: 10px;
                font-size: 1.2em;
            }
            .phone {
                background: #667eea;
                color: white;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                font-size: 1.3em;
                font-weight: 600;
                margin-top: 20px;
            }
            .footer {
                text-align: center;
                color: #999;
                margin-top: 30px;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 WhatsApp AI Bot</h1>
            <div class="status">ONLINE</div>
            
            <div class="info">
                <h2>Capabilities</h2>
                <div class="feature">Text conversation & questions</div>
                <div class="feature">Voice message transcription</div>
                <div class="feature">Image OCR & analysis</div>
            </div>
            
            <div class="phone">
                📱 +1 (415) 523-8886
            </div>
            
            <div class="footer">
                Powered by AI • Always Ready
            </div>
        </div>
    </body>
    </html>
    """
    return html, 200


# Initialize bot on module load (for gunicorn)
from dotenv import load_dotenv
load_dotenv()

# Load configuration from environment variables
groq_api_key = os.getenv('GROQ_API_KEY')
gemini_api_key = os.getenv('GEMINI_API_KEY')
twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')

if not all([groq_api_key, gemini_api_key, twilio_account_sid, twilio_auth_token, twilio_phone_number]):
    raise ValueError("Missing required environment variables. Check your .env file.")

# Initialize bot
bot = WhatsAppBotFree(
    groq_api_key=groq_api_key,
    gemini_api_key=gemini_api_key,
    twilio_account_sid=twilio_account_sid,
    twilio_auth_token=twilio_auth_token,
    twilio_phone_number=twilio_phone_number
)

logger.info("FREE Bot initialized successfully!")


def main():
    """Run Flask app directly (for local testing)"""
    port = int(os.getenv('PORT', 5000))
    logger.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)


if __name__ == '__main__':
    main()
