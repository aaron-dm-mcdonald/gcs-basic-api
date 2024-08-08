


resource "google_storage_bucket_object" "function_archive" {
  name   = "function-source.zip"
  bucket = google_storage_bucket.bucket.name
  source = "path/to/your/function-source.zip"
}

resource "google_cloudfunctions_function" "function" {
  name                  = "my-function"
  description           = "My Cloud Function"
  runtime               = "python39"
  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.function_archive.name
  trigger_http          = true
  entry_point           = "main"
}

resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = google_cloudfunctions_function.function.project
  region         = google_cloudfunctions_function.function.region
  cloud_function = google_cloudfunctions_function.function.name
  role           = "roles/cloudfunctions.invoker"
  member         = "allUsers"
}
