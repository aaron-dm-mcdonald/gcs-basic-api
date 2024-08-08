# gcs-basic-api

This is a simple HTTP REST API written in Python. It is a lightweight Flask App with 3 endpoints that use the GCS client library to access a bucket in GCS. The API is wrapped in the Cloud functions entrypoint function to allow calls from the trigger by Cloud Functions. 

Features:

/upload 
This endpoint allows a file of the users choice to be uploaded to the bucket.

/download
This endpoint allows a file to be downloaded from the bucket and saved on the local machine. 

/list
This endpoint allows a user to list all objects in the bucket. 




CURL Examples:


curl -X POST -F 'file=@path/to/your/file' https://YOUR_FUNCTION_URL/upload

curl -X GET 'https://YOUR_FUNCTION_URL/download?filename=yourfile.txt' -o yourfile.txt

curl -X GET https://YOUR_FUNCTION_URL/list


----- local build:

docker build -t gcr.io/YOUR_PROJECT_ID/my-function .
docker push gcr.io/YOUR_PROJECT_ID/my-function

---- OR buildpack (easier):

gcloud functions deploy my-function --runtime python39 --trigger-http --allow-unauthenticated --entry-point main
