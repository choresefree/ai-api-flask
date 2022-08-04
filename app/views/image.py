import os
import tarfile
from flask import request, Blueprint, current_app, url_for, make_response, send_from_directory, jsonify
from flask_login import login_required
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from app.create_app import character_recognizer


class ImageWarehouse(Resource):
    def __init__(self):
        self.logger = current_app.logger
        self.app = current_app
        self.parser = RequestParser()
        self.dir = os.path.join(self.app.config['UPLOAD_FOLDER'], 'speech')
        self.parser.add_argument('file_name', type=str, help='Rate cannot be converted', location=['args'])
        self.parser.add_argument('picture', type=FileStorage, help='Rate cannot be converted', location='files')
        self.req = self.parser.parse_args()

    @login_required
    def get(self):
        file_name = self.req.file_name
        response = make_response(send_from_directory(self.dir, file_name, as_attachment=True))
        return response

    @login_required
    def post(self):
        self.logger.info("Image upload")
        picture = self.req.picture
        file_name = secure_filename(picture.filename)
        if file_name.endswith('.png') or file_name.endswith('.jpeg') or file_name.endswith('.jpg'):
            if not os.path.exists(self.dir):
                os.makedirs(self.dir)
            picture.save(os.path.join(self.dir, file_name))
            return jsonify({'status': 1, 'msg': 'File upload success'})
        else:
            return jsonify({'status': 0, 'msg': 'File format is not supported'})


class ImageRecognise(Resource):
    def __init__(self):
        self.logger = current_app.logger
        self.app = current_app
        self.parser = RequestParser()
        self.parser.add_argument('picture', type=FileStorage, help='Rate cannot be converted', location='files')
        self.req = self.parser.parse_args()

    @login_required
    def post(self):
        self.logger.info("Image recognise")
        picture = self.req.picture
        file_name = secure_filename(picture.filename)
        if file_name.endswith('.png') or file_name.endswith('.jpeg') or file_name.endswith('.jpg'):
            category = character_recognizer.predict(picture)
            return jsonify({'status': 1, 'msg': category})
        else:
            return jsonify({'status': 0, 'msg': 'File format is not supported'})


bp = Blueprint('image', __name__, url_prefix='/api/v1/image')
api = Api(bp)
api.add_resource(ImageWarehouse, '/warehouse', endpoint='image_warehouse')
api.add_resource(ImageRecognise, '/recognizer', endpoint='image_rec')
