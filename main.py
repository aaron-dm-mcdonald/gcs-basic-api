from google.cloud import storage
from flask import Flask, request, jsonify

# Initialize the Flask app
app = Flask(__name__)

# Initialize the Google Cloud Storage client
client = storage.Client()

# Name of the Google Cloud Storage bucket
bucket_name = 'sandbox-bucket-api'

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    blob = client.bucket(bucket_name).blob(file.filename)
    blob.upload_from_file(file)
    return jsonify({'message': f'File {file.filename} uploaded successfully.'}), 200

@app.route('/download', methods=['GET'])
def download_file():
    filename = request.args.get('filename')
    blob = client.bucket(bucket_name).blob(filename)
    content = blob.download_as_bytes()
    return content, 200, {'Content-Type': 'application/octet-stream'}

@app.route('/list', methods=['GET'])
def list_files():
    blobs = client.bucket(bucket_name).list_blobs()
    files = [blob.name for blob in blobs]
    return jsonify({'files': files}), 200

# Entry point for the Cloud Function
def main(request):
    return app.wsgi_app(request.environ, start_response)

# Helper function for WSGI
def start_response(status, response_headers, exc_info=None):
    return response_headers
