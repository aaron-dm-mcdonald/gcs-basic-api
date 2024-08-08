# gcs-basic-api

## Overview
This is a simple HTTP REST API written in Python. It is a lightweight Flask App with 3 endpoints that use the GCS client library to access a bucket in GCS. The API is wrapped in the Cloud functions entrypoint function to allow calls from the trigger by Cloud Functions. 

## Features:

/upload 
This endpoint allows a file of the users choice to be uploaded to the bucket.

/download
This endpoint allows a file to be downloaded from the bucket and saved on the local machine. 

/list
This endpoint allows a user to list all objects in the bucket. 




## CURL Examples:


curl -X POST -F 'file=@path/to/your/file' https://YOUR_FUNCTION_URL/upload

curl -X GET 'https://YOUR_FUNCTION_URL/download?filename=yourfile.txt' -o yourfile.txt

curl -X GET https://YOUR_FUNCTION_URL/list

## Deployment:

Step 1: 

Clone Repo

git clone https://github.com/YOUR_USERNAME/gcs-basic-api.git
cd gcs-basic-api 

You should open the directory in VS Code.

Step 2: 

initalize gcloud 

Step 3:

Edit code to include a preexisting bucket in main.py. 

Step 4:

Deploy it using the following:

### local build:

gcloud auth configure-docker

docker build -t gcr.io/YOUR_PROJECT_ID/my-function .

docker push gcr.io/YOUR_PROJECT_ID/my-function

gcloud functions deploy my-function \
    --entry-point main \
    --runtime python39 \
    --trigger-http \
    --allow-unauthenticated \
    --source gcr.io/YOUR_PROJECT_ID/my-function


### buildpack (easier):

gcloud functions deploy my-function --runtime python39 --trigger-http --allow-unauthenticated --entry-point main


## Features to build
1) Abstract hardcoded bucket name with env vars or secret manager 
2) add basic API key 
