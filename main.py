# Import modules 
from google.cloud import storage
from flask import Flask, request, jsonify

# Initialize the Flask app 
app = Flask(__name__)

# Initialize the Google Cloud Storage client 
client = storage.Client()

# Name of the Google Cloud Storage bucket (Change this to preexisting bucket)
bucket_name = 'sandbox-bucket-api'

# End of application "boilerplate"



# First API Endpoint for uploading files
@app.route('/list', methods=['GET'])
def list_files():
    # List all objects (blobs/files) in the specified bucket
    blobs = client.bucket(bucket_name).list_blobs()
    # Create a list of file names
    files = [blob.name for blob in blobs]
    # Return the list of files as JSON
    return jsonify({'files': files}), 200



# Second API Endpoint for downloading files
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



# Third API Endpoint for uploading files
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



# Fourth API Endpoint for deleting files
@app.route('/delete', methods=['DELETE'])
def delete_file():
    # Get the filename from the request arguments
    filename = request.args.get('filename')
    # Create a blob object for the specified file in the bucket
    blob = client.bucket(bucket_name).blob(filename)
    # Delete the file from Google Cloud Storage
    blob.delete()
    # Return a success message
    return jsonify({'message': f'File {filename} deleted successfully.'}), 200



# Fifth API Endpoint for retrieving file metadata
@app.route('/metadata', methods=['GET'])
def get_metadata():
    # Get the filename from the request arguments
    filename = request.args.get('filename')
    # Create a blob object for the specified file in the bucket
    blob = client.bucket(bucket_name).blob(filename)
    # Retrieve the metadata of the file
    metadata = blob.metadata
    # Return the metadata as JSON
    return jsonify({'metadata': metadata}), 200




# Sixth API Endpoint for generating a signed URL
@app.route('/signed-url', methods=['GET'])
def generate_signed_url():
    # Get the filename from the request arguments
    filename = request.args.get('filename')
    # Create a blob object for the specified file in the bucket
    blob = client.bucket(bucket_name).blob(filename)
    # Generate a signed URL for the file with a 15-minute expiration
    url = blob.generate_signed_url(expiration=timedelta(minutes=15))
    # Return the signed URL as JSON
    return jsonify({'url': url}), 200




# Some final "boilerplate" for the python code to be wrapped by GCF function for invokations 


# Entry point for the Cloud Function
def main(request):
    # Pass the request to the Flask app
    return app.wsgi_app(request.environ, start_response)

# Helper function for WSGI
def start_response(status, response_headers, exc_info=None):
    # Return the response headers
    return response_headers