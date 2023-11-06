# app2.py
import os
from flask import Flask, request, render_template, jsonify
from ytchat_refactored import download_youtube_video, convert_mp4_to_mp3, transcribe_audio_to_text, chat_with_bot, create_chatbot_context

OPENAI_API_KEY = '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'

app = Flask(__name__)

# Global variable to store conversation context
conversation_context = []

@app.route('/')
def index():
    return render_template('index.html')  # Make sure to create an 'index.html' template with the UI elements specified

@app.route('/transcribe', methods=['POST'])
def transcribe_video():
    # Get YouTube URL from the user input
    video_url = request.form.get('youtube_url')
    
    # Download YouTube video
    video_path, error = download_youtube_video(video_url)
    if error:
        return jsonify({'error': error})
    
    # Convert video to audio
    audio_path, error = convert_mp4_to_mp3(video_path, 'temp_audio.mp3')
    if error:
        return jsonify({'error': error})
    
    # Transcribe audio to text
    transcribed_text, error = transcribe_audio_to_text(audio_path)  # Removed the OPENAI_API_KEY parameter
    if error:
        return jsonify({'error': error})
    
    # Create initial chatbot context
    global conversation_context
    conversation_context = create_chatbot_context(transcribed_text)
    
    # Inform the user that transcription is complete
    return jsonify({'message': 'Transcription complete. You can now chat with the bot.'})

@app.route('/chat', methods=['POST'])
def chat():
    # Get the user's message from the input
    user_message = request.form.get('user_message')
    
    # Chat with the bot using the global conversation context
    global conversation_context
    try:
        bot_response = chat_with_bot(conversation_context, user_message, OPENAI_API_KEY)
        return jsonify({'bot_response': bot_response})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
