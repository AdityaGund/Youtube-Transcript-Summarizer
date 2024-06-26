from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

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

@app.route('/transcript', methods=['GET'])
def transcript():
    video_id = request.args.get('video_id')
    
    if not video_id:
        return jsonify({'error': 'Video ID parameter is required'}), 400
    
    transcript_text = get_video_transcript(video_id)
    return jsonify({'transcript': transcript_text})

if __name__ == '__main__':
    app.run(debug=True)
