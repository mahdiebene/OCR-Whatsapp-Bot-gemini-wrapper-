"""
Test script for WhatsApp Bot functionality
Run this to test without WhatsApp integration
"""

import os
from dotenv import load_dotenv
from whatsapp_bot import WhatsAppBot

# Load environment variables
load_dotenv()

def test_text_chat():
    """Test AI chat functionality"""
    print("\n=== Testing Text Chat ===")
    
    bot = WhatsAppBot(
        openai_api_key=os.getenv('OPENAI_API_KEY'),
        twilio_account_sid="dummy_sid",  # Not needed for local testing
        twilio_auth_token="dummy_token",
        twilio_phone_number="whatsapp:+1234567890"
    )
    
    test_messages = [
        "Hello! Who are you?",
        "What's 2+2?",
        "Tell me a joke"
    ]
    
    for message in test_messages:
        print(f"\nUser: {message}")
        response = bot.chat_with_ai(message)
        print(f"Bot: {response}")

def test_image_processing():
    """Test image processing with a sample image"""
    print("\n=== Testing Image Processing ===")
    print("Note: You'll need to have an image file to test this")
    
    bot = WhatsAppBot(
        openai_api_key=os.getenv('OPENAI_API_KEY'),
        twilio_account_sid="dummy_sid",
        twilio_auth_token="dummy_token",
        twilio_phone_number="whatsapp:+1234567890"
    )
    
    # You can add a test image here
    # with open('test_image.jpg', 'rb') as f:
    #     image_data = f.read()
    #     response = bot.process_image(image_data, "What's in this image?")
    #     print(f"Image Analysis: {response}")
    
    print("Skipping image test - no test image provided")

def test_audio_processing():
    """Test audio processing"""
    print("\n=== Testing Audio Processing ===")
    print("Note: You'll need to have an audio file to test this")
    
    bot = WhatsAppBot(
        openai_api_key=os.getenv('OPENAI_API_KEY'),
        twilio_account_sid="dummy_sid",
        twilio_auth_token="dummy_token",
        twilio_phone_number="whatsapp:+1234567890"
    )
    
    # You can add a test audio file here
    # with open('test_audio.mp3', 'rb') as f:
    #     audio_data = f.read()
    #     response = bot.process_audio(audio_data, 'mp3')
    #     print(f"Transcription: {response}")
    
    print("Skipping audio test - no test audio provided")

if __name__ == '__main__':
    print("WhatsApp Bot Test Suite")
    print("=" * 50)
    
    # Check if API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY not set in .env file")
        exit(1)
    
    test_text_chat()
    # Uncomment these when you have test files
    # test_image_processing()
    # test_audio_processing()
    
    print("\n" + "=" * 50)
    print("Tests completed!")
