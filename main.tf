################################
# Create Storage Bucket - Main #
################################

locals {
  project_prefix   = var.environment != "prod" ? "${var.project_prefix}_${var.environment}" : var.project_prefix
  #project_prefix  = "${var.project_prefix}_${var.environment}"
  timestamp        = formatdate("YYMMDDhhmmss", timestamp())
  output_table     = var.environment != "prod" ? "${var.output_table}_${var.environment}" : var.output_table
}

# Create a GCS Bucket
resource "google_storage_bucket" "tf_bucket" {
  project       = var.gcp_project
  name          = local.project_prefix
  location      = var.gcp_region
  force_destroy = true
  storage_class = var.storage_class
  versioning {
    enabled = true
  }
}
#
### Code ###

# Compress source code
data "archive_file" "source" {
  type        = "zip"
  source_dir  = "pysrc"
  output_path = "/tmp/${var.project_prefix}-function-${local.timestamp}.zip"
  excludes    = [".ipynb_checkpoints", "__pycache__", "terraform", "venv", "tests", "scripts"]
}

# Add source code zip to bucket
resource "google_storage_bucket_object" "archive" {
  name   = "function_source.zip${local.timestamp}"
  bucket = google_storage_bucket.tf_bucket.name
  source = data.archive_file.source.output_path
}

resource "google_cloudfunctions_function" "function" {
  name          = "${local.project_prefix}"
  runtime       = "python37"
  service_account_email = var.gcf_sa_email

  available_memory_mb   = 512
  source_archive_bucket = google_storage_bucket.tf_bucket.name
  source_archive_object = google_storage_bucket_object.archive.name

  timeout       = 350
  entry_point   = "main"

  labels = {
    environment     = var.environment
    project_prefix  = local.project_prefix
  }

  environment_variables = {
    environment         = var.environment
    project_prefix      = local.project_prefix
    output_dataset      = var.output_dataset
    output_table        = local.output_table
    gcp_project         = var.gcp_project
  }

  trigger_http = true

}

