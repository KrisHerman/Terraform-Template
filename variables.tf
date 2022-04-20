#####################################
# Create Storage Bucket - Variables #
#####################################

variable "project_prefix" {
  type        = string
  description = "Short name for the project. Used in naming resources"
}

variable "environment" {
  type        = string
  description = "Development envioronment such as dev, staging, prod"
  default = "dev"
}

variable "storage_class" {
  type        = string
  description = "The storage class of the Google Storage Bucket to create"
}

variable "output_dataset" {
  type        = string
  description = "Dataset name of the output table."
}

variable "output_table" {
  type        = string
  description = "Output table name for pubsub messages."
}

variable "gcf_sa_email" {
  type        = string
  description = "Service account email for the google cloud function."
}

variable "pubsub_topic" {
  type        = string
  description = "Name of pubsub topic to listen on. The host project is set by var.gcp_project."
}

variable "pubsub_gcp_project" {
  type        = string
  description = "GCP project that hosts the pubsub topic"
}