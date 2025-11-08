"""
WhatsApp Bot with Audio and Image Processing
Uses Twilio for WhatsApp and OpenAI Whisper for AI interactions
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict
import asyncio

# Twilio for WhatsApp
from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import requests

# AI and processing libraries
from openai import OpenAI
from pydub import AudioSegment
from PIL import Image
import io
import base64

# Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
UPLOAD_FOLDER = 'downloads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'ogg', 'opus', 'mpeg', 'amr'}

class WhatsAppBot:
    def __init__(self, openai_api_key: str, twilio_account_sid: str, twilio_auth_token: str, twilio_phone_number: str):
        """
        Initialize WhatsApp Bot with Twilio and AI capabilities
        
        Args:
            openai_api_key: OpenAI API key for AI processing
            twilio_account_sid: Twilio Account SID
            twilio_auth_token: Twilio Auth Token
            twilio_phone_number: Twilio WhatsApp number (e.g., whatsapp:+14155238886)
        """
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.twilio_client = Client(twilio_account_sid, twilio_auth_token)
        self.twilio_phone_number = twilio_phone_number
        
        # Create upload folder if it doesn't exist
        Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
        
        # Store conversation context (simple in-memory storage)
        self.conversation_contexts: Dict[str, list] = {}
        
        logger.info("WhatsApp Bot initialized with Twilio")
    
    def send_message(self, to: str, message: str) -> dict:
        """Send a text message via Twilio WhatsApp"""
        try:
            message = self.twilio_client.messages.create(
                from_=self.twilio_phone_number,
                body=message,
                to=to
            )
            logger.info(f"Message sent: {message.sid}")
            return {"status": "sent", "sid": message.sid}
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return {"status": "error", "error": str(e)}
    
    def download_media(self, media_url: str) -> Optional[bytes]:
        """Download media from Twilio"""
        try:
            # Twilio media URLs require authentication
            response = requests.get(
                media_url,
                auth=(self.twilio_client.username, self.twilio_client.password)
            )
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.error(f"Error downloading media: {e}")
            return None
    
    def process_audio(self, audio_data: bytes, audio_format: str = 'ogg') -> str:
        """
        Convert audio to text using speech recognition
        
        Args:
            audio_data: Raw audio bytes
            audio_format: Audio format (ogg, mp3, wav, etc.)
        
        Returns:
            Transcribed text
        """
        try:
            # Save audio temporarily
            temp_audio_path = f"{UPLOAD_FOLDER}/temp_audio.{audio_format}"
            with open(temp_audio_path, 'wb') as f:
                f.write(audio_data)
            
            # Convert to WAV if needed
            if audio_format != 'wav':
                audio = AudioSegment.from_file(temp_audio_path, format=audio_format)
                wav_path = f"{UPLOAD_FOLDER}/temp_audio.wav"
                audio.export(wav_path, format='wav')
                temp_audio_path = wav_path
            
            # Use OpenAI Whisper for transcription (more accurate)
            with open(temp_audio_path, 'rb') as audio_file:
                transcript = self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en"  # Remove this to auto-detect language
                )
            
            # Clean up
            os.remove(temp_audio_path)
            if audio_format != 'wav' and os.path.exists(f"{UPLOAD_FOLDER}/temp_audio.wav"):
                os.remove(f"{UPLOAD_FOLDER}/temp_audio.wav")
            
            return transcript.text
        
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            return f"Error transcribing audio: {str(e)}"
    
    def process_image(self, image_data: bytes, user_query: str = "What's in this image?") -> str:
        """
        Analyze image using OpenAI Vision
        
        Args:
            image_data: Raw image bytes
            user_query: Question about the image
        
        Returns:
            AI description of the image
        """
        try:
            # Encode image to base64
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            # Use GPT-4 Vision
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",  # or "gpt-4-vision-preview"
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_query},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            return f"Error analyzing image: {str(e)}"
    
    def chat_with_ai(self, message: str, user_number: str = None, context: list = None) -> str:
        """
        Have a conversation with AI
        
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
                    "content": "You are a helpful AI assistant in a WhatsApp bot. Be concise, friendly, and helpful. Keep responses brief since this is a messaging platform."
                }]
            
            # Add user message
            messages = context + [{"role": "user", "content": message}]
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
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
        """
        Handle incoming WhatsApp message from Twilio
        
        Args:
            from_number: Sender's WhatsApp number
            body: Text message body
            media_url: URL of media attachment
            media_content_type: MIME type of media
            num_media: Number of media attachments
        
        Returns:
            Response message
        """
        try:
            logger.info(f"Received message from {from_number}")
            
            # Handle text messages
            if body and num_media == 0:
                # Check for commands
                if body.lower() in ['/start', 'start', 'hello', 'hi']:
                    response = ("👋 Hello! I'm your AI WhatsApp assistant!\n\n"
                               "Send me:\n"
                               "📝 Text - Chat with me\n"
                               "🎤 Audio - I'll transcribe and respond\n"
                               "🖼️ Image - I'll analyze it\n\n"
                               "Type /reset to clear conversation history")
                    self.send_message(from_number, response)
                    return response
                
                elif body.lower() in ['/reset', 'reset']:
                    self.conversation_contexts[from_number] = []
                    response = "✅ Conversation history cleared!"
                    self.send_message(from_number, response)
                    return response
                
                else:
                    response = self.chat_with_ai(body, from_number)
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
                    # Determine audio format
                    audio_format = media_content_type.split('/')[-1]
                    if audio_format == 'mpeg':
                        audio_format = 'mp3'
                    
                    transcription = self.process_audio(media_data, audio_format)
                    
                    response = f"🎤 *Transcription:*\n{transcription}\n\n💬 *AI Response:*\n"
                    ai_response = self.chat_with_ai(transcription, from_number)
                    full_response = response + ai_response
                    
                    self.send_message(from_number, full_response)
                    return full_response
                
                # Handle images
                elif media_content_type and 'image' in media_content_type:
                    query = body if body else "Describe this image in detail"
                    description = self.process_image(media_data, query)
                    
                    response = f"🖼️ *Image Analysis:*\n{description}"
                    self.send_message(from_number, response)
                    return response
                
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
        
        # Process message (bot will send response itself)
        bot.handle_message(
            from_number=from_number,
            body=body,
            media_url=media_url,
            media_content_type=media_content_type,
            num_media=num_media
        )
        
        # Return empty response (message already sent)
        resp = MessagingResponse()
        return str(resp), 200
    
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        resp = MessagingResponse()
        resp.message("❌ Sorry, an error occurred.")
        return str(resp), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "whatsapp-bot"}, 200


def main():
    """Initialize and run the bot"""
    global bot
    
    # Load environment variables from .env file
    from dotenv import load_dotenv
    load_dotenv()
    
    # Load configuration from environment variables
    openai_api_key = os.getenv('OPENAI_API_KEY')
    twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
    
    if not all([openai_api_key, twilio_account_sid, twilio_auth_token, twilio_phone_number]):
        raise ValueError("Missing required environment variables. Check your .env file.")
    
    # Initialize bot
    bot = WhatsAppBot(
        openai_api_key=openai_api_key,
        twilio_account_sid=twilio_account_sid,
        twilio_auth_token=twilio_auth_token,
        twilio_phone_number=twilio_phone_number
    )
    
    logger.info("Bot initialized successfully!")
    
    # Run Flask app
    port = int(os.getenv('PORT', 5000))
    logger.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)


if __name__ == '__main__':
    main()
