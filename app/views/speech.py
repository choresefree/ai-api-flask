import os
from flask import Blueprint, current_app, jsonify, make_response, send_from_directory, url_for
from flask_login import login_required
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename, redirect
from app.create_app import speech_recognizer


class SpeechWarehouse(Resource):
    def __init__(self):
        self.app = current_app
        self.logger = current_app.logger
        self.parser = RequestParser()
        self.dir = os.path.join(self.app.config['UPLOAD_FOLDER'], 'speech')
        self.parser.add_argument('file_name', type=str, help='Rate cannot be converted', location=['args'])
        self.parser.add_argument('speech', type=FileStorage, help='Rate cannot be converted', location='files')
        self.req = self.parser.parse_args()

    @login_required
    def get(self):
        file_name = self.req.file_name
        response = make_response(send_from_directory(self.dir, file_name, as_attachment=True))
        return response

    @login_required
    def post(self):
        self.logger.info("Speech upload")
        speech = self.req.speech
        file_name = secure_filename(speech.filename)
        if file_name.endswith('.mp3') or file_name.endswith('.wav'):
            if not os.path.exists(self.dir):
                os.makedirs(self.dir)
            speech.save(os.path.join(self.dir, file_name))
            return jsonify({'status': 1, 'msg': 'File upload success'})
        else:
            return jsonify({'status': 0, 'msg': 'File format is not supported'})

    @login_required
    def delete(self):
        file_name = self.req.file_name
        file_path = os.path.join(self.dir, file_name)
        if os.path.exists(file_path):
            os.remove(os.path.join(self.dir, file_name))
            return jsonify({'status': 1, 'msg': 'File delete success'})
        else:
            return jsonify({'status': 0, 'msg': 'File does not exist'})


class SpeechRecognizer(Resource):
    def __init__(self):
        self.app = current_app
        self.logger = current_app.logger
        self.parser = RequestParser()
        self.parser.add_argument('speech', type=FileStorage, help='Rate cannot be converted', location='files')
        self.req = self.parser.parse_args()

    @login_required
    def post(self):
        speech = self.req.speech
        file_name = secure_filename(speech.filename)
        if file_name.endswith('.mp3') or file_name.endswith('.wav'):
            return jsonify({'status': 1, 'msg': speech_recognizer.predict(speech)})
        else:
            return jsonify({'status': 0, 'msg': 'File format is not supported'})


bp = Blueprint('speech', __name__, url_prefix='/api/v1/speech')
api = Api(bp)
api.add_resource(SpeechWarehouse, '/warehouse', endpoint='speech_warehouse')
api.add_resource(SpeechRecognizer, '/recognizer', endpoint='speech_rec')
