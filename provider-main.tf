
terraform {
  required_version = ">= 0.12"
  backend "gcs" {
    bucket = "terraform-datawarehouse"
    prefix = "sample_app"
  }
}

provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}
