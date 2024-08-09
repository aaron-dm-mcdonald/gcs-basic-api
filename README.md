# gcs-basic-api

## Overview
This is a simple HTTP REST API written in Python, designed to interact with a Google Cloud Storage (GCS) bucket. The API is stateless and implemented using a lightweight Flask application. It features three endpoints that utilize the GCS client library to perform operations on a GCS bucket. The API is wrapped in a Cloud Functions entrypoint function, enabling it to be triggered by Google Cloud Functions (GCF). GCF is an event-driven, serverless compute service that allows for lightweight code execution in response to events occurring within the Google Cloud Platform (GCP). WSGI (Web Server Gateway Interface) acts as a bridge between the web server and the Flask application, ensuring seamless request and response handling within the serverless environment.

## Features:

The HTTP server 
/upload 
This endpoint allows a file of the users choice to be uploaded to the bucket.

/download
This endpoint allows a file to be downloaded from the bucket and saved on the local machine. 

/list
This endpoint allows a user to list all objects in the bucket. 

## What is actually happening:
Assume we are using the /list endpoint as it is the most straightforward.

1) HTTP Request: When you run curl, it sends an HTTP GET request to the specified URL (https://YOUR_FUNCTION_URL/list).

2) Cloud Function Trigger: The request triggers the Cloud Function associated with this URL. Google Cloud Functions handles the incoming request and routes it to the appropriate function.

3) Flask App Handling: The Cloud Function’s entry point (main) passes the request to the Flask application using WSGI. The Flask app then processes the request.

4) Endpoint Execution: The Flask app routes the request to the /list endpoint:
   - **List Files**: The `list_files` function is called. It uses the Google Cloud Storage client to list all objects (blobs) in the specified bucket.
   - **Create File List**: It creates a list of file names from the blobs.
   - **Return Response**: The list of file names is returned as a JSON response with a status code of 200 (OK).

5) Response Handling: The WSGI interface translates the Flask app’s response into an HTTP response that the Cloud Function sends back to the client.

6) Output: curl receives the HTTP response and displays the JSON file (containing the list of objects from the bucket) in the terminal.


## cURL Commands:

### Basics

As this is an API, essenitally middleware with no front end, interaction has to be limited to CLI utilities like curl or wget, or alternatively, an API development/testing utility like Postman could be used. 

If you are not familar, curl can be used to interact with servers using protocols like HTTP or FTP. It can send and recieve data. 

You write it like this:
curl -X <REST_METHOD> https://YOUR_URL/endpoint 

This would use whatever REST method you want like GET or POST to invoke an API endpoint (or whatever is at the end of URL)

Another flag we will use is 
-F : This indicates a file is involved and specifies it path in the argument
-F 'file=@path/to/your/file' (this is how you would add this flag to curl)

Finally, if we want to pass a query to the API we need to do two things:
1) append the query seperator (the question mark in the URL) and query information
2) use the output flag (-o) to specify the path of the file (to be downloaded in this case)

### curl commands
The simplest call to execute would be:
curl -X GET https://YOUR_FUNCTION_URL/list 

In addition the following two calls are available: 

curl -X POST -F 'file=@path/to/your/file' https://YOUR_FUNCTION_URL/upload

curl -X GET 'https://YOUR_FUNCTION_URL/download?filename=yourfile.txt' -o yourfile.txt

unless you specify the file path remember it most be in the present working directory of the CLI that you are executing curl from. 



## Deployment:

**Step 1:**

Clone Repo

git clone https://github.com/aaron-dm-mcdonald/gcs-basic-api.git


Open this in VS Code

**Step 2:**

initalize gcloud 

**Step 3:**

Edit code to include a preexisting bucket in main.py on line 11. 

**Step 4:**

Deploy it using one the following methods:

### 1) local build (not reccomended):

gcloud auth configure-docker

docker build -t gcr.io/YOUR_PROJECT_ID/my-function .

docker push gcr.io/YOUR_PROJECT_ID/my-function

gcloud functions deploy my-function \
    --entry-point main \
    --runtime python39 \
    --trigger-http \
    --allow-unauthenticated \
    --source gcr.io/YOUR_PROJECT_ID/my-function


### 2) buildpack (easier):

gcloud functions deploy my-function --runtime python39 --trigger-http --allow-unauthenticated --entry-point main


## Features to build
1) Abstract hardcoded bucket name with env vars or secret manager 
2) add basic API key 
3) Finish terraform deployment, package source code as ZIP for automated deployment 
