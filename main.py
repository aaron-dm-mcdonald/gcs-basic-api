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
    # Get the file from the request
    file = request.files['file']
    # Create a blob object for the file in the specified bucket
    blob = client.bucket(bucket_name).blob(file.filename)
    # Upload the file to Google Cloud Storage
    blob.upload_from_file(file)
    # Return a success message
    return jsonify({'message': f'File {file.filename} uploaded successfully.'}), 200

@app.route('/download', methods=['GET'])
def download_file():
    # Get the filename from the request arguments
    filename = request.args.get('filename')
    # Create a blob object for the specified file in the bucket
    blob = client.bucket(bucket_name).blob(filename)
    # Download the file content as bytes
    content = blob.download_as_bytes()
    # Return the file content with appropriate headers
    return content, 200, {'Content-Type': 'application/octet-stream'}

@app.route('/list', methods=['GET'])
def list_files():
    # List all blobs (files) in the specified bucket
    blobs = client.bucket(bucket_name).list_blobs()
    # Create a list of file names
    files = [blob.name for blob in blobs]
    # Return the list of files as a JSON response
    return jsonify({'files': files}), 200

# Entry point for the Cloud Function
def main(request):
    # Pass the request to the Flask app
    return app.wsgi_app(request.environ, start_response)

# Helper function for WSGI
def start_response(status, response_headers, exc_info=None):
    # Return the response headers
    return response_headers
