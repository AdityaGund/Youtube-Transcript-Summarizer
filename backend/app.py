from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)
api = Api(app)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    system_instruction="""You are a summarization system designed to generate concise and coherent summaries of video transcripts. Your task is to understand the key points and main ideas presented in the transcript and summarize them in a way that captures the essence of the video. Please follow these guidelines:
    1. **Comprehensiveness**: Include all the major points discussed in the transcript, including any significant details, insights, or conclusions.
    2. **Clarity**: Ensure the summary is clear and easy to understand, avoiding any jargon or complex language unless it's essential to the context.
    3. **Structure**: Present the summary in a logical order that mirrors the structure of the original content, with a clear beginning, middle, and end.
    4. **Length**: Aim for a summary length of approximately 150-200 words, ensuring it's detailed enough to convey the main ideas but concise enough to be quickly read.
    5. **Neutral Tone**: Maintain a neutral and objective tone throughout the summary, avoiding any personal opinions or interpretations.
    6. **Context**: Make sure the summary is self-contained, providing enough context for a reader who hasn't seen the video to understand the main points.
    7. **Pointwise Format**: If possible, present the summary in a pointwise manner to enhance readability and clarity.
    8. **Brevity**: Keep the summary brief and to the point.
    9. **Attractive**: Make the content attractive by adding particular emojis and anything related to that fact and mention that it is not in the video like something suggested or well fitting here""",
)
def get_video_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])

        if isinstance(transcript_list, list) and all(isinstance(item, dict) for item in transcript_list):
            transcript_text = ' '.join([transcript['text'] for transcript in transcript_list])
            return transcript_text
        else:
            return 'Unexpected response format'
    except Exception as e:
        return str(e)
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
def summarize_transcript(transcript):
    chat_session=model.start_chat(history=[])
    response=chat_session.send_message(transcript)
    return response.text

@app.route('/transcript', methods=['GET'])
def transcript():
    video_id = request.args.get('video_id')
    
    if not video_id:
        return jsonify({'error': 'Video ID parameter is required'}), 400
    
    transcript_text = get_video_transcript(video_id)
    return jsonify({'transcript': transcript_text})

@app.route('/summarize',methods=['POST'])
def  summarize():
    data=request.get_json()
    transcript=data.get('transcript')
    if not transcript:
        return jsonify({'error':'Transcript is reqired'}),400
    summary=summarize_transcript(transcript)
    return jsonify({'summary':summary})

if __name__ == '__main__':
    app.run(debug=True)






