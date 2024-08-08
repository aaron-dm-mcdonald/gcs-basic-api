terraform {
  
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "5.25.0"
    }
  }

  backend "gcs" {
    bucket = "amcdonald-k8s-state"
    prefix = "terraform/state"
    credentials = "primary-sandbox-project-3ccca0fb815d.json"
  }

}

provider "google" {
  # Configuration options
  project = var.project
  region = "us-central1"
  zone = var.zone
  credentials = "primary-sandbox-project-3ccca0fb815d.json"
}


